#!/bin/bash

# Скрипт для запуска Cloudflare Tunnel и FastAPI-приложения
# 1. Активация виртуального окружения
# 2. Запуск Cloudflare Tunnel в фоне
# 3. Запуск FastAPI через uvicorn

# Этап 1: Активация виртуального окружения
echo "🚀 [1/3] Активируем виртуальное окружение .venv..."
source .venv/bin/activate

# Этап 2: Запуск Cloudflare Tunnel (cloudflared tunnel run hotel1) в фоне
# Логи cloudflared пишем в отдельный файл cloudflared.log

echo "🌐 [2/3] Запускаем Cloudflare Tunnel (cloudflared tunnel run hotel1)..."
cloudflared tunnel run hotel1 > cloudflared.log 2>&1 &
CLOUDFLARED_PID=$!
echo "   Cloudflared запущен с PID $CLOUDFLARED_PID (логи: cloudflared.log)"
echo "📍 Туннель запущен на $(hostname) в $(date)" > tunnel_status.log

# Этап 3: Запуск FastAPI через uvicorn

echo "🦄 [3/3] Запускаем FastAPI (uvicorn main:app --host 0.0.0.0 --port 8000 --reload)..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# После завершения uvicorn останавливаем cloudflared
trap 'if kill -0 "$CLOUDFLARED_PID" 2>/dev/null; then kill "$CLOUDFLARED_PID"; echo "⛔ Cloudflare остановлен"; else echo "ℹ️  Cloudflare уже остановлен"; fi' EXIT 