# Модуль lang (Language Analysis)

Микромодуль для анализа текста (intent detection), генерации диалоговых ответов и сохранения результатов в базу PostgreSQL.

## Основные функции

### detect_intent(text: str) -> dict
Извлекает намерение пользователя (intent), номер комнаты, время и уверенность из текста с помощью OpenAI GPT-4o.

**Поддерживаемые интенты:**
- `room_cleaning` — уборка номера
- `late_checkout` — поздний выезд
- `room_booking` — бронирование номера
- `unknown` — не удалось распознать

**Пример:**
```python
from voice_call_handler.lang.logic import detect_intent
result = detect_intent("Здравствуйте, я хочу забронировать номер с 5 по 7 июня на двоих.")
print(result)
# {
#   "intent": "room_booking",
#   "room_number": null,
#   "time": null,
#   "confidence": 0.95
# }
```

### handle_dialog(text: str) -> str
Генерирует вежливый ответ для голосового ассистента на основе результата detect_intent.

**Примеры:**
- `room_cleaning`: "Пожалуйста, уберите в номере 305 сегодня вечером." → _"Уборка будет выполнена в номере 305 сегодня вечером."_
- `late_checkout`: "Можно ли выехать чуть позже завтра?" → _"Поздний выезд возможен. Я отмечу это в системе."_
- `room_booking`: "Здравствуйте, я хочу забронировать номер с 5 по 7 июня на двоих." → _"Конечно! Я помогу вам с бронированием. Уточните, пожалуйста, даты и количество гостей."_
- `unknown`: "А можно фиолетовый дракон?" → _"Извините, я не совсем понял. Повторите, пожалуйста."_

## API-маршруты
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

## Тесты

Папка `tests/` содержит автотесты для detect_intent и handle_dialog. 