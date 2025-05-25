# Модуль lang (Language Analysis)

Микромодуль для анализа текста (intent detection) и сохранения результатов в базу PostgreSQL.

## Маршруты
- POST `/api/v1/lang/analyze` — принимает JSON {"text": "..."}, возвращает {"intent": ..., "entities": ...}. Результат автоматически сохраняется в базу.

## Пример запроса

```bash
curl -X POST \
  http://localhost:8001/api/v1/lang/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Хочу забронировать номер"}'
```

## Структура таблицы intents

```sql
CREATE TABLE intents (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    intent TEXT NOT NULL,
    entities JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Подключение к PostgreSQL
Используются переменные окружения (пароли не публикуйте в открытом доступе):
- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD=Secu.......3

### Пример заполнения .env:

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=voice_hotel_db
POSTGRES_USER=adm......e
POSTGRES_PASSWORD=Secu.......3 