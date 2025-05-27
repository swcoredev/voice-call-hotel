#!/bin/bash

# Скрипт для теста цепочки STT -> LANG
# Использование: ./scripts/test_lang_script.sh static/client_request.m4a

if [ -z "$1" ]; then
  echo "❌ Укажите путь к аудиофайлу (например, static/client_request.m4a)"
  exit 1
fi
AUDIO_FILE="$1"

# 1. Отправляем аудиофайл на STT
STT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/stt/process \
  -F "audio_file=@$AUDIO_FILE")

RECOGNIZED_TEXT=$(echo "$STT_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['text'])")

# 2. Отправляем text на LANG
LANG_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/lang/process \
  -H "Content-Type: application/json" \
  -d '{"text": "'$RECOGNIZED_TEXT'"}')

ASSISTANT_RESPONSE=$(echo "$LANG_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('response', '💭 Нет ответа от ассистента'))")

# 3. Выводим результат
printf '\n🎙️  Распознанный текст: %s\n' "$RECOGNIZED_TEXT"
printf '🤖 Ответ ассистента: %s\n' "$ASSISTANT_RESPONSE" 