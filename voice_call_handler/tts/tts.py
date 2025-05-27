import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

default_voice_settings = {
    "stability": 0.5,
    "similarity_boost": 0.5,
}

async def generate_speech(text: str) -> bytes:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    voice_id = os.getenv('ELEVENLABS_VOICE_ID')
    speed = float(os.getenv('ELEVENLABS_SPEED', '1.0'))
    if not api_key or not voice_id:
        logging.error('ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID not set')
        raise Exception("TTS API key or voice ID not set")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {**default_voice_settings, "speed": speed}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.content
    except Exception as e:
        logging.error(f"ElevenLabs TTS error: {e}")
        raise Exception(f"Speech synthesis error: {str(e)}")
