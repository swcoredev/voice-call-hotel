# Модуль voice

## Назначение
Обработка голосовых звонков через Twilio. Интеграция цепочки STT → LANG → Dialog → TTS для автоматизации голосового обслуживания.

## Blueprint
Blueprint подключается в `__init__.py` этого модуля.

## Роуты
- **GET /api/v1/** — проверка статуса
- **GET /api/v1/voice** — тест API
- **POST /api/v1/voice** — отдаёт TwiML XML

## Запуск
```bash
gunicorn main:app
```

## Пример запроса
```bash
curl -X POST https://voice.servis.work/api/v1/voice
``` 