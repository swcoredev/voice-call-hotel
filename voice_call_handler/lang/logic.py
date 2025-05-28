from sqlalchemy import Table, Column, Integer, String, Text, JSON, TIMESTAMP, MetaData
from sqlalchemy.sql import func
import logging
from openai import OpenAI
import os
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_text(text: str):
    text_lower = text.lower()
    if any(word in text_lower for word in ['book', 'reserve', 'бронировать', 'заказать']):
        intent = 'booking'
    elif any(word in text_lower for word in ['cancel', 'отмена', 'отменить']):
        intent = 'cancel'
    elif any(word in text_lower for word in ['info', 'инфо', 'справка', 'узнать']):
        intent = 'info'
    else:
        intent = 'unknown'
    # entities можно расширить позже
    return {'intent': intent, 'entities': []}

# --- Сохранение в базу ---
def save_intent_to_db(engine, text, intent, entities):
    metadata = MetaData()
    intents = Table(
        'intents', metadata,
        Column('id', Integer, primary_key=True),
        Column('text', Text, nullable=False),
        Column('intent', String, nullable=False),
        Column('entities', JSON),
        Column('created_at', TIMESTAMP, server_default=func.now())
    )
    # metadata.create_all(engine)  # отключено для тестовой базы
    with engine.begin() as conn:
        conn.execute(intents.insert().values(text=text, intent=intent, entities=entities))
        logging.info("✅ Интент успешно записан в test-базу")

def detect_intent(text: str) -> dict:
    system_prompt = (
        "Ты агент для извлечения намерения клиента отеля. "
        "Отвечай строго в формате JSON с полями: intent (один из 'room_cleaning', 'late_checkout', 'room_booking', 'food_order', 'wake_up_call', 'complaint', 'unknown'), "
        "room_number (если есть), time (если есть), confidence (от 0 до 1, насколько уверен в разметке). "
        "Примеры фраз для интентов:\n"
        "room_booking: 'Я хочу забронировать номер', 'Нам нужен номер с 5 по 7 июня на двоих', 'Я бы хотел снять комнату на троих'.\n"
        "room_cleaning: 'Пожалуйста, уберите в номере 305', 'Мне нужна уборка в комнате сегодня вечером'.\n"
        "late_checkout: 'Можно ли выехать чуть позже?', 'Я хотел бы задержаться до 2 часов'.\n"
        "food_order: 'Хочу заказать еду в номер', 'Можно мне ужин в 8 вечера'.\n"
        "wake_up_call: 'Разбудите меня в 6 утра', 'Мне нужен wake-up call в 7:30'.\n"
        "complaint: 'У меня жалоба', 'В комнате шумно', 'Очень грязно, уберите пожалуйста'.\n"
        "Если неясно, что хочет клиент — intent должен быть 'unknown', остальные поля null или пустые."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.0,
            max_tokens=256
        )
        import json
        content = response.choices[0].message.content.strip()
        print(">> Ответ OpenAI:", repr(content))
        # Удаляем markdown-обёртку
        content = re.sub(r"^```json|^```|```$", "", content.strip(), flags=re.MULTILINE).strip()
        return json.loads(content)
    except Exception as e:
        return {
            "intent": "unknown",
            "room_number": None,
            "time": None,
            "confidence": 0.0,
            "error": str(e)
        } 