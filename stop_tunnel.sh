#!/bin/bash

# Скрипт для остановки только Cloudflare Tunnel (cloudflared)
# Локальный сервер (uvicorn) не трогаем!

CLOUDFLARED_PID=$(pgrep -f 'cloudflared tunnel run')

if [ -n "$CLOUDFLARED_PID" ]; then
  kill $CLOUDFLARED_PID
  echo "🛑 Cloudflare Tunnel остановлен"
else
  echo "❌ Cloudflare Tunnel уже не работает (или был выбит)"
fi

# Проверяем, работает ли uvicorn
UVICORN_PID=$(pgrep -f 'uvicorn')
if [ -n "$UVICORN_PID" ]; then
  echo "🟢 Локальный сервер (uvicorn) продолжает работать!"
else
  echo "⚠️  Внимание: локальный сервер (uvicorn) не найден или остановлен."
fi 