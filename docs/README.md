# Voice Call Hotel — Модули и API

## Описание модулей

- **tts** — синтез речи (Text-to-Speech). Генерирует аудиофайлы на основе текста, поддерживает ElevenLabs API.
- **stt** — распознавание речи (Speech-to-Text). Принимает аудиофайлы, конвертирует их в нужный формат и отправляет в Whisper/OpenAI для транскрипции.
- **lang** — определение намерения (Intent Detection). Анализирует текстовые запросы пользователя и определяет их смысл.

## Примеры API-запросов

- `GET  /api/v1/tts/welcome` — получить приветственное аудиосообщение (отдаёт файл из static, например, ElevenLabs_Untitled_Project.wav)
- `POST /api/v1/stt/process` — отправить аудиофайл для распознавания речи (multipart/form-data)
- `POST /api/v1/lang/analyze` — анализ текста для определения намерения

## Особенности работы stt

Модуль **stt** автоматически конвертирует любые аудиоформаты (mp3, wav, m4a и др.), поддерживаемые ffmpeg, в формат WAV 16kHz mono перед отправкой на распознавание. Это обеспечивает совместимость с большинством аудиофайлов.

---

## 🧪 Тестирование модуля STT
Для быстрого теста распознавания речи:

```bash
bash test_stt_script.sh
```

Этот скрипт отправляет файл `client_request.m4a` из папки `static/` на эндпоинт:

POST http://localhost:8000/api/v1/stt/process

После запуска сервер должен вернуть распознанный текст.

---

## 🧠 Диалог на основе STT + LANG

Запуск скрипта:
```bash
./scripts/test_lang_script.sh static/client_request.m4a
```

Пример вывода:

🎙️  Распознанный текст: Здравствуйте, мне нужна уборка в номере 217 сегодня вечером. Спасибо.
💭 Ответ ассистента: Конечно, уборка будет выполнена сегодня вечером в номере 217. Если потребуется что-то ещё, пожалуйста, дайте знать!

Скрипт отправляет аудиофайл на STT, затем результат — на LANG, и выводит оба результата.

---

## Изменения в TTS
- Добавлен эндпоинт `/api/v1/tts/welcome`, который отдаёт статический аудиофайл из папки `static` (например, ElevenLabs_Untitled_Project.wav).
- Для тестирования синтеза речи через ElevenLabs добавлен скрипт `test_tts.py` (см. папку `voice_call_handler/tts/`).
- Вся чувствительная информация (API-ключи, voice_id и т.д.) хранится в `.env`.

---

## 🧠 Intent Detection (определение намерения)

Модуль LANG использует OpenAI (gpt-4o) для извлечения намерения пользователя, номера комнаты, времени и уверенности из текстового запроса.

- Функция `detect_intent(text: str) -> dict` возвращает JSON с полями:
  - `intent`: например, "room_cleaning", "food_order", "late_checkout", "unknown"
  - `room_number`: если найден (например, "217")
  - `time`: если найдено (например, "evening", "tomorrow")
  - `confidence`: от 0 до 1

Модель всегда возвращает строго JSON-ответ, устойчивый к markdown-обёртке.

### Пример автотеста

```python
from voice_call_handler.lang.logic import detect_intent

def test_room_cleaning():
    result = detect_intent("Пожалуйста, уберите в номере 305 сегодня вечером.")
    assert result["intent"] == "room_cleaning"
    assert str(result["room_number"]) == "305"
    assert result["confidence"] > 0.5
```

Тесты запускаются командой:
```bash
pytest voice_call_handler/tests/test_detect_intent.py
```

--- 