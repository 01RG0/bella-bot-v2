#!/usr/bin/env bash
# Stop local dev services (POSIX)

set -e

echo "Stopping Bella Bot dev processes..."

# Kill uvicorn (API)
pkill -f uvicorn || true

# Kill bot process (python -m bot.bella_bot)
pkill -f "python.*bot.bella_bot" || true

# Kill frontend (vite / npm run dev)
pkill -f vite || true
pkill -f "npm run dev" || true

# Kill Lavalink if present
pkill -f Lavalink.jar || true

echo "Removing pid files if any..."
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
if [ -d "$ROOT_DIR/pids" ]; then
  rm -f "$ROOT_DIR/pids"/*.pid || true
fi

echo "Stop complete. Verify with ps aux | egrep 'uvicorn|bot.bella_bot|vite'"
