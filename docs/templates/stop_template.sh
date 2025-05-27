#!/bin/bash

# Скрипт для остановки cloudflared и uvicorn
# 1. Находит и останавливает cloudflared
# 2. Находит и останавливает uvicorn
# 3. Выводит статусы с иконками

# Останавливаем cloudflared
CLOUDFLARED_PID=$(pgrep -f 'cloudflared( |$)')
if [ -n "$CLOUDFLARED_PID" ]; then
  kill $CLOUDFLARED_PID
  echo '• 🔴 Cloudflare Tunnel остановлен'
else
  echo '• Cloudflare Tunnel не найден (уже остановлен)'
fi

# Останавливаем uvicorn
UVICORN_PID=$(pgrep -f 'uvicorn( |$)')
if [ -n "$UVICORN_PID" ]; then
  kill $UVICORN_PID
  echo '• 🦄 Uvicorn остановлен'
else
  echo '• Uvicorn не найден (уже остановлен)'
fi

# Финальный статус
if [ -z "$CLOUDFLARED_PID" ] && [ -z "$UVICORN_PID" ]; then
  echo '✅ Всё выключено (ничего не было запущено)'
else
  echo '✅ Всё выключено'
fi

echo "🧹 Удаляем лог tunnel_status.log..."
rm -f tunnel_status.log 