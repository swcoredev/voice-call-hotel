import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
ELEVENLABS_SPEED = float(os.getenv("ELEVENLABS_SPEED", 1.0))

url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": ELEVENLABS_API_KEY
}

data = {
    "text": "Привет, это тест синтеза речи!",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.7,
        "style": 0.0,
        "use_speaker_boost": True,
        "speed": ELEVENLABS_SPEED
    }
}

response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    with open("tts/test_output.mp3", "wb") as f:
        f.write(response.content)
    print("Успешно: файл сохранён как test_output.mp3")
else:
    print(f"Ошибка: {response.status_code} — {response.text}") 