from fastapi import APIRouter
from pydantic import BaseModel
from voice_call_handler.logic import handle_voice_text

router = APIRouter()

class VoiceRequest(BaseModel):
    text: str

@router.post("/process-voice/")
def process_voice(data: VoiceRequest):
    response = handle_voice_text(data.text)
    return {"response": response}
