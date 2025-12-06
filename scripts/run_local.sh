#!/usr/bin/env bash
# Run API, bot, and frontend in background (POSIX)

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "Repository root: $ROOT_DIR"

echo "Starting API (uvicorn)..."
cd "$ROOT_DIR/bot"
mkdir -p "$ROOT_DIR/logs"
nohup uvicorn bot.bella_bot.api_server:app --reload --host 0.0.0.0 --port 8000 > "$ROOT_DIR/logs/api.log" 2>&1 &
API_PID=$!
echo "API PID: $API_PID"

echo "Starting Bot..."
cd "$ROOT_DIR/bot"
nohup python -m bot.bella_bot > "$ROOT_DIR/logs/bot.log" 2>&1 &
BOT_PID=$!
echo "Bot PID: $BOT_PID"

echo "Starting Frontend..."
cd "$ROOT_DIR/web"
nohup npm run dev > "$ROOT_DIR/logs/web.log" 2>&1 &
WEB_PID=$!
echo "Web PID: $WEB_PID"

echo "Launched services. Logs: $ROOT_DIR/logs"
