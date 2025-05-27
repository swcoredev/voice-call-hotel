import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from voice_call_handler.tts.tts import generate_speech
import pytest

@pytest.mark.asyncio
def test_generate_speech():
    text = "Здравствуйте! Ваш номер успешно забронирован."
    audio = pytest.run(generate_speech(text))
    assert isinstance(audio, bytes)
    assert len(audio) > 0
