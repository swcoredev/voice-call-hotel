#!/bin/bash
echo "🎙️ Тестируем модуль STT с локального аудиофайла"
curl -X POST http://localhost:8000/api/v1/stt/process \
  -F "audio_file=@./static/client_request.m4a" 