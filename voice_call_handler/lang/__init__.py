from fastapi import APIRouter, HTTPException
from .logic import analyze_text, save_intent_to_db
from .schemas import TextIn, AnalyzeOut
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter(prefix="/api/v1/lang")

load_dotenv()

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'voice_hotel_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'adminvoice')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'SecurePass123')

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise HTTPException(status_code=500, detail="OPENAI_API_KEY не найден в переменных окружения!")
client = OpenAI(api_key=OPENAI_API_KEY)

class TextInput(BaseModel):
    text: str

@router.post("/analyze")
async def analyze(text_in: TextIn):
    if not text_in.text:
        raise HTTPException(status_code=400, detail="Missing text")
    
    result = analyze_text(text_in.text)
    # Сохраняем результат в базу
    try:
        save_intent_to_db(engine, text_in.text, result['intent'], result['entities'])
    except Exception as e:
        import logging
        logging.exception('❌ Ошибка при записи интента в базу:')
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")
    
    return AnalyzeOut(**result)

@router.post("/process")
async def process_text(text_in: TextInput):
    try:
        print(">> Отправка в OpenAI:", text_in.text)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты голосовой ассистент гостиницы. Отвечай кратко, вежливо и по делу."},
                {"role": "user", "content": text_in.text}
            ]
        )
        answer = response.choices[0].message.content.strip()
        return {"response": answer}
    except Exception as e:
        print("❌ Ошибка LANG:", e)
        raise HTTPException(status_code=500, detail={"error": str(e)})

if __name__ == "__main__":
    from fastapi import FastAPI
    app = FastAPI(__name__)
    app.include_router(router)
    app.run(host="0.0.0.0", port=8002) 