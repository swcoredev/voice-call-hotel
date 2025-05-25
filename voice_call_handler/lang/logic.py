from sqlalchemy import Table, Column, Integer, String, Text, JSON, TIMESTAMP, MetaData
from sqlalchemy.sql import func

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
    metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(intents.insert().values(text=text, intent=intent, entities=entities)) 