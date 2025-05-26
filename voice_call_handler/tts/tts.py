import os
import requests
import logging
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv

def speak_text(text: str):
    load_dotenv()
    api_key = os.getenv('ELEVENLABS_API_KEY')
    voice_id = os.getenv('ELEVENLABS_VOICE_ID')
    speed = float(os.getenv('ELEVENLABS_SPEED', '1.0'))
    if not api_key or not voice_id:
        logging.error('ELEVENLABS_API_KEY or ELEVENLABS_VOICE_ID not set')
        return {"error": "TTS API key or voice ID not set"}
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5, "speed": speed}
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        audio = AudioSegment.from_file("output.mp3", format="mp3")
        play(audio)
        return {"result": "Speech synthesized"}
    except Exception as e:
        logging.error(f"ElevenLabs TTS error: {e}")
        return {"error": f"Speech synthesis error: {str(e)}"}
