# Модуль tts

## Назначение
Синтез речи (Text-to-Speech) для голосовых вызовов.

## Основные файлы
- tts.py — основная логика TTS
- test_tts.py — тесты для TTS
- schemas.py — схема запроса

## API
- POST `/api/v1/tts/synthesize` — принимает JSON {"text": "..."}, синтезирует речь (локально через pyttsx3)

### Пример curl-запроса
```bash
curl -X POST http://127.0.0.1:8001/api/v1/tts/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Привет, это тест"}'
```

### Структура запроса
```json
{
  "text": "Привет, это тест"
}
```

### Структура ответа
```json
{
  "result": "Speech synthesized"
}
``` 