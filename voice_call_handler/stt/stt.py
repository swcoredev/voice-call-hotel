import whisper
import logging

logger = logging.getLogger(__name__)

model = whisper.load_model("base")

def transcribe_audio(path: str) -> str:
    logger.info("Начало распознавания файла: %s", path)
    result = model.transcribe(path)
    return result["text"]
