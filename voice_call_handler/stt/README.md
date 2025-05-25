# STT (Speech-to-Text)
Микромодуль для загрузки аудиофайлов и преобразования речи в текст.
Работает на Flask, маршруты:
- `GET /upload` — HTML-форма для загрузки файла
- `POST /api/v1/voice/process` — обработка текста
Развёрнут через Cloudflare Tunnel на домене `https://stt.servis.work`.

# Модуль stt

## Назначение
Распознавание речи (Speech-to-Text) для голосовых вызовов.

## Основные файлы
- stt.py — основная логика STT
- test_stt.py — тесты для STT 

## Пример запроса

```bash
curl -X POST \
  http://localhost:5000/api/v1/stt/process \
  -F "audio=@/path/to/your/audio.wav"
```

- Замените `/path/to/your/audio.wav` на путь к вашему аудиофайлу.
- Ответ будет содержать JSON с распознанным текстом или ошибкой. 