# STT (Speech-to-Text)
Микромодуль для загрузки аудиофайлов и преобразования речи в текст.

## Назначение
Распознавание речи (Speech-to-Text) для голосовых вызовов. Использует OpenAI Whisper API.

## Основные файлы
- stt.py — основная логика STT
- test_stt.py — тесты для STT 

## API
- POST `/api/v1/stt/process` — принимает аудиофайл (multipart/form-data), возвращает JSON с распознанным текстом.

## Пример запроса

```bash
curl -X POST \
  http://localhost:8000/api/v1/stt/process \
  -F "audio_file=@/path/to/your/audio.wav"
```

- Замените `/path/to/your/audio.wav` на путь к вашему аудиофайлу.
- Ответ будет содержать JSON с распознанным текстом или ошибкой. 

## Тесты

- Папка `tests/` содержит автотесты для STT.
- Для быстрого теста используйте bash-скрипт `test_stt_script.sh`. 