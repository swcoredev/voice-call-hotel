from fastapi import FastAPI
from voice_call_handler.router import router as voice_router

app = FastAPI()

app.include_router(voice_router, prefix="/voice")

@app.get("/")
def read_root():
    return {"message": "VoiceCall Hotel API is running"}
