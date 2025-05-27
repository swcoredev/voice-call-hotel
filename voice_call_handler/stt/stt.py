import os
import io
import logging
from fastapi import UploadFile
import requests
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def transcribe_audio(audio_file: UploadFile) -> dict:
    try:
        audio_bytes = io.BytesIO(await audio_file.read())
        audio_bytes.seek(0)
        stt_url = "https://api.openai.com/v1/audio/transcriptions"
        stt_headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        stt_data = {'model': 'whisper-1'}
        stt_resp = requests.post(
            stt_url,
            headers=stt_headers,
            files={'file': (audio_file.filename, audio_bytes, audio_file.content_type)},
            data=stt_data
        )
        if stt_resp.status_code != 200:
            logger.error(f"STT error: {stt_resp.text}")
            raise Exception(f"STT failed: {stt_resp.text}")
        return stt_resp.json()
    except Exception as e:
        logger.exception(f"Error in transcribe_audio: {e}")
        raise
