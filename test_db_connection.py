from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://adminvoice:SecurePass123@100.111.172.61:5432/voice_hotel_db_test"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Успешное подключение! Результат:", result.fetchone())
except Exception as e:
    print("Ошибка подключения:", e) 