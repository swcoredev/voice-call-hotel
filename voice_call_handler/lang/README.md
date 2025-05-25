# Модуль lang (Language Analysis)

Микромодуль для анализа текста (intent detection).

## Маршруты
- POST `/api/v1/lang/analyze` — принимает JSON {"text": "..."}, возвращает {"intent": ..., "entities": ...}

## Пример запроса

```bash
curl -X POST \
  http://localhost:8001/api/v1/lang/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Хочу забронировать номер"}'
```

## Подключение к PostgreSQL
Используются переменные окружения:
- POSTGRES_HOST=localhost
- POSTGRES_PORT=5432
- POSTGRES_DB=voice_hotel_db
- POSTGRES_USER=adminvoice
- POSTGRES_PASSWORD=SecurePass123 