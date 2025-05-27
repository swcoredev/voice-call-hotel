from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from .tts import generate_speech
import io

router = APIRouter(prefix="/api/v1/tts")

@router.post("/speak")
async def speak(text: str):
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    try:
        audio_content = await generate_speech(text)
        audio_stream = io.BytesIO(audio_content)
        audio_stream.seek(0)
        
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=response.mp3"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 