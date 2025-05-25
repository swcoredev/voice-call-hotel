import pytest
from flask import Flask
from voice_call_handler.tts import tts_bp

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(tts_bp)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_tts_synthesize(client):
    response = client.post('/api/v1/tts/synthesize', json={"text": "Привет, это тест"})
    assert response.status_code == 200
    assert response.json["result"] == "Speech synthesized" 