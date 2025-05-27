import os
import io
import logging
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import requests
from dotenv import load_dotenv
import openai

from voice_call_handler.lang import router as lang_router
from voice_call_handler.stt import router as stt_router
from voice_call_handler.tts import router as tts_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY не найден в переменных окружения! Проверь .env и запуск.")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
ELEVENLABS_SPEED = float(os.getenv("ELEVENLABS_SPEED", 1.0))

app = FastAPI()
app.include_router(lang_router)
app.include_router(stt_router)
app.include_router(tts_router)

@app.post("/api/v1/dialog")
async def dialog(audio_file: UploadFile = File(...), first: bool = Form(False)):
    try:
        # 1. Получаем аудиофайл из запроса
        audio_bytes = io.BytesIO(await audio_file.read())
        audio_bytes.seek(0)
        logger.info(f"Получен аудиофайл: {audio_file.filename}, размер: {audio_bytes.getbuffer().nbytes} байт")

        # 2. Speech-to-Text (STT) через OpenAI Whisper API
        stt_url = "https://api.openai.com/v1/audio/transcriptions"
        stt_headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        stt_files = {
            'file': (audio_file.filename, audio_bytes, audio_file.content_type),
            'model': (None, 'whisper-1')
        }
        stt_data = {'model': 'whisper-1'}
        stt_resp = requests.post(stt_url, headers=stt_headers, files={'file': (audio_file.filename, audio_bytes, audio_file.content_type)}, data=stt_data)
        if stt_resp.status_code != 200:
            logger.error(f"STT error: {stt_resp.text}")
            return {"error": "STT failed", "details": stt_resp.text}
        user_text = stt_resp.json().get('text', '')
        logger.info(f"Распознанный текст: {user_text}")

        # 3. Определяем, первый ли это запрос
        is_first = not user_text.strip() or first
        if is_first:
            prompt = "Клиент подключился к голосовому помощнику отеля. Представься и предложи помощь."
            gpt_url = "https://api.openai.com/v1/chat/completions"
            gpt_headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
            gpt_data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": prompt}
                ]
            }
            gpt_resp = requests.post(gpt_url, headers=gpt_headers, json=gpt_data)
            if gpt_resp.status_code != 200:
                logger.error(f"GPT error: {gpt_resp.text}")
                return {"error": "GPT failed", "details": gpt_resp.text}
            reply_text = gpt_resp.json()['choices'][0]['message']['content']
            logger.info(f"GPT приветствие: {reply_text}")
        else:
            # 4. Intent detection через lang-модуль
            lang_url = "http://localhost:8002/api/v1/lang/analyze"
            lang_resp = requests.post(lang_url, json={"text": user_text})
            if lang_resp.status_code != 200:
                logger.error(f"Lang error: {lang_resp.text}")
                return {"error": "Lang failed", "details": lang_resp.text}
            lang_data = lang_resp.json()
            reply_text = lang_data.get('response') or lang_data.get('intent', 'Извините, я не понял ваш запрос.')
            logger.info(f"Ответ lang-модуля: {reply_text}")

        # 5. Text-to-Speech (TTS) через ElevenLabs
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        tts_headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        tts_payload = {
            "text": reply_text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.7,
                "style": 0.0,
                "use_speaker_boost": True,
                "speed": ELEVENLABS_SPEED
            }
        }
        tts_resp = requests.post(tts_url, headers=tts_headers, json=tts_payload)
        if tts_resp.status_code != 200:
            logger.error(f"TTS error: {tts_resp.text}")
            return {"error": "TTS failed", "details": tts_resp.text}
        logger.info(f"TTS аудио успешно получено, размер: {len(tts_resp.content)} байт")
        audio_stream = io.BytesIO(tts_resp.content)
        audio_stream.seek(0)

        # 6. Возвращаем аудиопоток клиенту
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=response.mp3"}
        )
    except Exception as e:
        logger.exception(f"Ошибка в /api/v1/dialog: {e}")
        return {"error": str(e)}

@app.get("/")
async def index():
    return "VoiceCall Hotel API is running"

# Пример curl-запроса:
# curl -X POST http://localhost:8001/api/v1/dialog \
#   -F "audio_file=@example.wav" \
#   -H "Accept: audio/mpeg" --output response.mp3
