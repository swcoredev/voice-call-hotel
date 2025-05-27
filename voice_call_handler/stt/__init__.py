from fastapi import APIRouter, HTTPException, File, UploadFile
from .stt import transcribe_audio
import os
import io
import requests
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

router = APIRouter(prefix="/api/v1/stt")

@router.post("/transcribe")
async def transcribe(audio_file: UploadFile = File(...)):
    if not audio_file:
        raise HTTPException(status_code=400, detail="No audio file provided")
    
    try:
        result = await transcribe_audio(audio_file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process")
async def transcribe(audio_file: UploadFile = File(...)):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY is not set")
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
        raise HTTPException(status_code=500, detail=f"STT failed: {stt_resp.text}")
    return stt_resp.json() 