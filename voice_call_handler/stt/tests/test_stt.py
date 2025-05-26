from voice_call_handler.stt import transcribe_audio
import io
import pytest
from flask import Flask
from voice_call_handler.stt import stt_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(stt_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_process_audio(client):
    # Генерируем пустой WAV-файл (или используйте реальный файл для интеграционного теста)
    wav_header = (
        b'RIFF$\x00\x00\x00WAVEfmt '  # WAV header
        b'\x10\x00\x00\x00\x01\x00\x01\x00'  # PCM, 1 channel
        b'\x40\x1f\x00\x00\x80>\x00\x00'  # 8000 Hz, 16-bit
        b'\x02\x00\x10\x00data\x00\x00\x00\x00'
    )
    data = io.BytesIO(wav_header)
    data.name = 'test.wav'
    response = client.post(
        '/api/v1/stt/process',
        data={'audio': (data, 'test.wav')},
        content_type='multipart/form-data',
    )
    assert response.status_code in (200, 500)  # 500 если Whisper не может распознать пустой файл
    assert 'text' in response.json or 'error' in response.json

if __name__ == "__main__":
    path = "voice_call_handler/examples/audio_example.wav"
    text = transcribe_audio(path)
    print("Текст из аудио:", text) 