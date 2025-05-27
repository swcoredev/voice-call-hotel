#!/bin/bash

echo "==============================="
echo "🌐 Проверка статуса Cloudflare Tunnel"
echo "==============================="

# Проверка PID cloudflared
pid=$(pgrep -f "cloudflared")

if [ -n "$pid" ]; then
    echo "✅ Туннель ЗАПУЩЕН (PID: $pid)"
    if [ -f tunnel_status.log ]; then
        cat tunnel_status.log
    fi
else
    echo "❌ Туннель НЕ запущен"
    # Проверяем, работает ли uvicorn
    UVICORN_PID=$(pgrep -f 'uvicorn')
    if [ -n "$UVICORN_PID" ]; then
      echo "🟢 Локальный сервер (uvicorn) продолжает работать!"
    fi
fi 