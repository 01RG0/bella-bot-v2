# Bella Bot v2

A comprehensive Discord bot with music, AI chat, moderation, and web dashboard.

## Features

- Music playback with Lavalink
- AI-powered chat (using Google Gemini)
- Image generation
- Moderation commands
- Web UI for management
- Background task processing

## Architecture

- **Bot**: Discord bot core with commands and events
- **Workers**: Celery workers for heavy tasks
- **Web**: Next.js dashboard
- **Infra**: Docker Compose setup with MongoDB and Redis

## Quick Start (Local Development)

**Windows (PowerShell):**
```powershell
# One command to setup and run everything
.\setup-and-run.ps1
```

This script will:
- ✅ Check Python and Node.js availability
- ✅ Install Python dependencies (`pip install -e .`)
- ✅ Install Node dependencies (`npm install`)
- ✅ Create `.env` from `.env.example` if missing
- ✅ Validate required environment variables
- ✅ Launch API (uvicorn), Discord bot, and frontend in separate windows

**Required environment variables** (set in `.env`):
- `DISCORD_TOKEN` — your Discord bot token
- `VITE_DISCORD_CLIENT_ID` — Discord OAuth app client ID
- `VITE_DISCORD_REDIRECT_URI` — Discord OAuth redirect URL (e.g., `http://localhost:5173/auth/discord/callback`)
- `VITE_DISCORD_CLIENT_SECRET` — Discord OAuth app client secret

**After startup:**
- 🌐 Dashboard: http://localhost:5173
- 🔧 API: http://localhost:8000
- 🤖 Bot: running in background

**To stop all services:**
```powershell
.\stop.ps1
```

**Skip installation (if already installed):**
```powershell
.\setup-and-run.ps1 -SkipInstall
```

## Deploy to Railway (Production)

### Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### Manual Deployment

1. **Create Railway Project:**
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub repo

2. **Configure Environment Variables:**
   
   Add these to Railway's environment variables:
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   MONGO_URI=mongodb+srv://root:root@cluster0.aswllnf.mongodb.net/?appName=Cluster0
   GEMINI_API_KEY=your_google_api_key
   IMAGE_MODEL=flux
   POLLINATIONS_TOKEN=dNn7GcmToUBrlJFY
   VITE_DISCORD_CLIENT_ID=your_discord_client_id
   VITE_DISCORD_CLIENT_SECRET=your_discord_client_secret
   VITE_DISCORD_REDIRECT_URI=https://your-app.railway.app/auth/discord/callback
   VITE_API_ALLOW_ORIGIN=https://your-app.railway.app
   BOT_PUBLIC_URL=https://your-app.railway.app
   JWT_SECRET=your-secret-jwt-key-change-this
   PORT=8000
   ```


3. **Deploy:**
   - Railway will auto-detect and build using `nixpacks.toml`
   - Bot and API will start automatically
   - Access your dashboard at: `https://your-app.railway.app`

### Deploy Frontend Separately (Optional)

For better performance, deploy the frontend as a separate service:

1. Create a new Railway service
2. Set build command: `cd web && npm run build`
3. Set start command: `cd web && npm run preview -- --port $PORT`
4. Update `VITE_API_BASE_URL` to point to your API service


## Manual Setup (Advanced)

If you prefer to run services manually:

### 1. Install Dependencies

```powershell
# Install Python dependencies
cd bot
pip install -e .

# Install Node dependencies
cd ../web
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env` and set your tokens:
- `DISCORD_TOKEN` — your Discord bot token
- `VITE_DISCORD_CLIENT_ID` — Discord OAuth client ID
- `VITE_DISCORD_CLIENT_SECRET` — Discord OAuth client secret
- `VITE_DISCORD_REDIRECT_URI` — OAuth redirect (e.g., `http://localhost:5173/auth/discord/callback`)

### 3. Start Services

**Terminal 1 - API Server:**
```powershell
cd bot
uvicorn bella_bot.api_server:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Discord Bot:**
```powershell
cd bot
python -m bella_bot
```

**Terminal 3 - Frontend:**
```powershell
cd web
npm run dev
```

The frontend will be available at http://localhost:5173 and the API at http://localhost:8000.