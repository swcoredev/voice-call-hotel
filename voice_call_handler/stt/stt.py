import logging
from flask import request, jsonify
from . import stt_bp
import tempfile
import os
import subprocess
import openai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def transcribe_audio_openai(path: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY is not set!")
        raise RuntimeError("OPENAI_API_KEY is not set!")
    client = openai.OpenAI(api_key=api_key)
    with open(path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

@stt_bp.route('/process', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        logger.warning('No audio file part in the request')
        return jsonify({'error': 'No audio file provided'}), 400
    audio_file = request.files['audio']
    if audio_file.filename == '':
        logger.warning('No selected file')
        return jsonify({'error': 'No selected file'}), 400
    # Сохраняем исходный файл во временный
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.filename)[-1]) as tmp_in:
        audio_file.save(tmp_in.name)
        input_path = tmp_in.name
    logger.info(f'Загрузка: {audio_file.filename} сохранён как {input_path}')
    # Конвертируем во временный .wav (16kHz, mono)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_out:
        output_path = tmp_out.name
    try:
        logger.info(f'Конвертация: {input_path} -> {output_path}')
        cmd = [
            'ffmpeg', '-y', '-i', input_path,
            '-ar', '16000', '-ac', '1', output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f'Конвертация завершена: {output_path}')
        # Распознаём через OpenAI Whisper API
        logger.info(f'Распознавание: {output_path}')
        text = transcribe_audio_openai(output_path)
        logger.info(f'Распознавание завершено: {text}')
        return jsonify({'text': text})
    except Exception as e:
        logger.error(f'Ошибка: {e}')
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
