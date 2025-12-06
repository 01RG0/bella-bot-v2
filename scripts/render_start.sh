#!/bin/bash
set -ne

# Start Uvicorn in the background
echo "Starting API Server..."
cd /app/bot
uvicorn bella_bot.api_server:app --host 0.0.0.0 --port $PORT &

# Start the bot in the foreground
echo "Starting Discord Bot..."
# The bot wrapper should run in foreground, or we wait for both.
# If we just run python -m bella_bot, it blocks.
# If uvicorn crashes, we might want to exit. 
# But for simplicity, we background uvicorn and foreground python.
python -m bella_bot
