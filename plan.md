# Bella — Full Project Plan, Architecture, Folder Structure, and Implementation Guide

> Comprehensive, copy-paste–ready Markdown blueprint for **Bella** — a personal Discord assistant bot (Python) with a TypeScript/React web control panel and MongoDB as the single source of truth. Designed for you and your friends (no payments).

---

## Table of contents

1. Project Overview
2. Goals & Non-goals
3. High-level Architecture
4. Tech Stack
5. Deployment Targets
6. Detailed Folder Structure (copyable)
7. File and Module Descriptions (what to put in each file)
8. MongoDB Schemas (example documents & collections)
9. Discord Bot Design (Python)
10. Web Dashboard Design (TypeScript / React)
11. WebSocket / API Contract
12. Background Workers & Concurrency
13. Music & Voice System (design using Lavalink or pure-Python fallback)
14. AI, Memory & Behavior Learning
15. Image Generation Flow
16. Permissions & Security Model
17. Logging, Observability & Metrics
18. Testing & CI/CD
19. Railway Deployment Guide
20. Milestones & Roadmap (MVP → Advanced)
21. Example env files & secrets
22. Operation & Maintenance Notes
23. Appendices: Helpful code snippets, best practices, and quickstarts

---

## 1. Project Overview

**Bella** is a personal Discord assistant designed to run on Railway and be controlled via a web panel. The bot core is **100% Python** (async), and the web control panel and admin UI are built in **TypeScript / React** (Next.js or Create React App). **MongoDB** is the single database for everything: settings, memories, behavior stats, audio metadata, logs, embeddings, and image history.

Bella will:

* Join voice channels and play music, with queues and filters
* Talk naturally (AI chat + short-term context)
* Remember people, their behavior, favorite words, moods, and relationships
* Generate images from prompts
* Moderate (kick, ban, timeout) with audit logs
* Provide a web-based dashboard for full control
* Be private (only for you and friends) — no payments, no subscriptions

---

## 2. Goals & Non-goals

### Goals

* Reliable Python bot capable of voice & music
* Rich memory system stored in MongoDB
* Full web control panel: status, queues, persona editing, logs
* Scalable background job design for heavy tasks (image gen, long AI calls)
* Easy to deploy on Railway (single project or multi-service)

### Non-goals

* No payment/billing features
* Not intended as a public commercial product (privacy-first, friend-only)

---

## 3. High-level Architecture

```
+------------------+          +----------------+          +-------------+
| Discord Clients  | <------> | Bella (Python) | <----->  | MongoDB     |
| (Users)          |          | - bot core     |          | (Atlas/URI) |
+------------------+          | - FastAPI API  |          +-------------+
                              | - WebSocket    |
                              +----------------+
                                      |
                    +-----------------+----------------+
                    |                                  |
            +---------------+                  +----------------+
            | Workers (BG)  |                  | Web UI (TS/React)|
            | - image-gen   |                  | - Dashboard      |
            | - ai workers  |                  | - Controls       |
            +---------------+                  +----------------+
```

Notes:

* The Python bot exposes an internal FastAPI (or socket) used by the TS web UI for control and WebSocket real-time updates.
* Heavy work goes to background workers (in-process threads or separate worker processes). Use Redis for multi-worker locking and queues if you scale beyond one instance.

---

## 4. Tech Stack

**Bot (Python)**

* `discord.py` or `py-cord` (async discord library)
* `motor` (async MongoDB driver)
* `fastapi` (for web endpoints and WebSocket if desired)
* `pydantic` (models & validation)
* `youtube-dl` / `yt-dlp` or Lavalink client wrapper for music
* `gtts` or other TTS library (optional)
* `whisper` or an API for STT (if needed)
* `concurrent.futures` / `asyncio` for background tasks

**Web Dashboard (TypeScript)**

* Next.js (recommended) or React + Vite
* React, TypeScript
* TailwindCSS (optional) or plain CSS
* WebSocket client for real-time updates

**Database & Background**

* MongoDB (Atlas recommended)
* Redis (optional; recommended if you use Bull/BullMQ or need distributed locks)

**Hosting**

* Railway for Python bot and web UI
* Cloud object storage (optional) for images — Railway volume or small S3-like service

---

## 5. Deployment Targets

* **Railway**: host Python bot, FastAPI endpoints, and Next.js app. You can create multiple services in one Railway project (bot service + web service). Use environment variables in Railway for tokens and Mongo URI.
* **Local development**: `docker-compose` recommended (bot, mongo, redis, lavalink (optional), web)

---

## 6. Detailed Folder Structure (COPYABLE)

```
/bella
├─ /bot
│  ├─ Dockerfile
│  ├─ pyproject.toml (or requirements.txt)
│  ├─ /bella_bot
│  │  ├─ __main__.py
│  │  ├─ bot.py                 # entry: connect to Discord
│  │  ├─ config.py              # loads env vars
│  │  ├─ commands/              # command modules (slash + prefix)
│  │  │  ├─ __init__.py
│  │  │  ├─ music.py
│  │  │  ├─ mod.py
│  │  │  ├─ ai_chat.py
│  │  ├─ events/                # event handlers
│  │  │  ├─ on_message.py
│  │  │  ├─ on_voice_state.py
│  │  ├─ services/
│  │  │  ├─ music_service.py    # queue management & lavalink client
│  │  │  ├─ ai_service.py       # call LLMs or provider
│  │  │  ├─ image_service.py    # image generation orchestration
│  │  │  ├─ memory_service.py   # short+long term memory API
│  │  ├─ models/                # pydantic models
│  │  ├─ db/                    # mongo models + helpers
│  │  ├─ utils/                 # helpers, utils, logging
│  │  ├─ api_server.py          # FastAPI app for web UI & webhook
│  │  └─ ws.py                  # WebSocket manager
│  └─ docker-compose.override.yml
├─ /workers
│  ├─ Dockerfile
│  ├─ requirements.txt
│  ├─ worker.py                 # worker entry for heavy tasks
│  └─ tasks/
│     ├─ image_task.py
│     └─ ai_task.py
├─ /web
│  ├─ Dockerfile
│  ├─ package.json
│  ├─ /src
│  │  ├─ pages/                 # if Next.js
│  │  ├─ components/
│  │  ├─ hooks/
│  │  └─ styles/
│  └─ next.config.js
├─ /infra
│  ├─ docker-compose.yml
│  └─ readme-deploy.md
├─ .env.example
└─ README.md
```

---

## 7. File and Module Descriptions (Short)

* **bot/**main**.py**: starts the bot (loads config, connects to Discord, registers commands)
* **bot/bot.py**: the `discord.Client` or `commands.Bot` object and extensions loader
* **bot/config.py**: load env and defaults (`DISCORD_TOKEN`, `MONGODB_URI`, `API_KEY_IMAGE`, etc.)
* **bot/commands/**: modular commands; each file registers slash commands
* **bot/events/**: event listeners (on_ready, on_message, on_voice_state_update)
* **bot/services/music_service.py**: track/queue management and lavalink client wrapper
* **bot/services/memory_service.py**: API to write/read memories from Mongo
* **bot/api_server.py**: FastAPI app that the web dashboard uses (or you can call via WebSocket)
* **workers/**: separate worker process for long-running jobs
* **web/**: React frontend to control Bella

---

## 8. MongoDB Schemas (Example JSON / Pydantic)

### `guilds` collection

```json
{
  "_id": "<guildId>",
  "name": "My Server",
  "prefix": "!",
  "djRoleId": "",
  "modRoleId": "",
  "settings": {
    "allowImageGen": true,
    "allowMusic": true,
    "memoryLevel": "full"
  },
  "createdAt": "ISODate"
}
```

### `users` collection

```json
{
  "_id": "<userId>",
  "username": "Ahmed#1234",
  "globalPrefs": { "ttsVoice": "bella-v1" },
  "stats": { "messages": 1200, "voiceMinutes": 540 },
  "behaviorSummary": {
    "favoriteWords": ["lol","wallahi"],
    "moodCounts": { "happy": 60, "angry": 5 }
  }
}
```

### `bella_memory` collection (core memory store)

```json
{
  "_id": ObjectId(),
  "userId": "<userId>|null",
  "guildId": "<guildId>|null",
  "type": "note|fact|reminder|trend",
  "content": "Bella remembers Ali likes lo-fi and hates spam.",
  "embeddingId": "<optional embedding ref>",
  "meta": { "source": "message|manual|web" },
  "createdAt": "ISODate",
  "expiresAt": null
}
```

### `music_queues` collection

```json
{
  "_id": "<guildId>",
  "queue": [ { "title": "Song", "url": "..", "addedBy": "userId" } ],
  "nowPlaying": { ... }
}
```

### `audit_logs`

```json
{
  "_id": ObjectId(),
  "guildId": "<guildId>",
  "actorId": "<userId>",
  "action": "kick|ban|timeout|command",
  "target": "<id or target>",
  "reason": ""
}
```

---

## 9. Discord Bot Design (Python) — Key Patterns

### Entrypoint

* Use an async entrypoint `python -m bella_bot` in `__main__`.
* Load env, initialize Mongo (motor), register command tree, and connect.

### Command System

* Use `discord.ext.commands.Bot` or `discord.Bot` (slash commands).
* Commands grouped: `music`, `mod`, `ai`, `image`, `memory`, `admin`.
* Each command file exports a `setup(bot)` function for cogs/extensions.

### Event Handling

* `on_ready`: load caches, prefetch guild settings
* `on_message`: run auto-detection for name mention, learning pipeline, react if needed
* `on_voice_state_update`: detect joins/leaves; auto-join if requested

### Memory Pipeline (message -> memory)

1. On message, run quick filters (length, mentions, blacklists)
2. Extract candidate facts ("I love lo-fi", "I'm bored")
3. Save short-term memory (channel-scoped) and optionally long-term after thresholds (repeated behavior)
4. Update user behavior counters and favorite words
5. Optionally compute & update embeddings (for semantic search)

---

## 10. Web Dashboard Design (TypeScript / React)

### Pages & Components

* **Login / OAuth** — Discord OAuth to authenticate and present guilds.
* **Dashboard** — overall status, bot uptime, quick actions.
* **Guild Settings** — toggle features, set roles, change prefix.
* **Music Page** — view & reorder queue, seek, volume.
* **AI Page** — conversation window, persona sliders, memory editor.
* **Logs Page** — audit logs, command usage.
* **Memory Explorer** — browse Bella's saved memories.

### Architecture

* Next.js API routes (or call FastAPI) for server-side needs.
* WebSockets to receive real-time updates (now playing, logs).
* Use the bot's API or a lightweight FastAPI server for actions (prefer secure token-based auth between web and bot).

---

## 11. WebSocket / API Contract (Example)

### WebSocket messages (JSON)

* `event: now_playing` — payload: {guildId, track, position}
* `event: queue_update` — payload: {guildId, queue}
* `event: audit_log` — payload: {entry}
* `event: memory_update` — payload: {id, summary}

### REST endpoints (FastAPI)

* `POST /api/guilds/{guildId}/music/play` — body: {url|string}
* `GET  /api/guilds/{guildId}/queue`
* `POST /api/image/gen` — body: {prompt, style}
* `GET  /api/memories?guildId=&userId=`

Security: require a signed JWT issued by the web UI, or use a shared secret between services.

---

## 12. Background Workers & Concurrency

### Design choices

* Avoid blocking `asyncio` event loop.
* Offload heavy CPU-bound tasks to `concurrent.futures.ProcessPoolExecutor` or separate worker processes.
* Use Redis and a lightweight queue (RQ / custom) if you expect >1 worker.

### Worker responsibilities

* Image generation
* Long-form AI queries (those that could time out)
* Audio transcoding & caching
* Periodic tasks (cleanup, expire memories)

---

## 13. Music & Voice System

Two approaches:

### A. Recommended: Lavalink (stable)

* Run a Lavalink node (Docker) to handle audio streaming.
* Python bot uses a Lavalink client (wavelink or lavalink.py) to control playback.
* Pros: stable, scalable, supports multiple nodes.
* Cons: additional infra service.

### B. Pure-Python fallback

* Use `yt-dlp` to fetch audio streams and feed them into `discord.VoiceClient`.
* Manage buffer and transcoding locally. Use `ffmpeg`.
* Pros: simpler infra.
* Cons: more CPU and reliability concerns.

Features to implement:

* Per-guild queue persisted to MongoDB
* Now-playing with progress and elapsed time
* Seek, repeat, shuffle, remove
* Volume & filters
* Auto-resume after restarts via persisted state

---

## 14. AI, Memory & Behavior Learning

### Memory levels

* **None** - no memory
* **Short** - session-level only (clears on restart or after expiry)
* **Full** - persistent long-term memory in `bella_memory`

### Embeddings & semantic memory (optional)

* Compute embeddings for saved memory entries and store them (embedding provider).
* Use vector similarity to retrieve relevant memories before responding.

### Behavior detection: pipeline

1. Tokenize each message and update `word_statistics`.
2. Update `user_behavior` counters and mood triggers (using simple rules or tiny classifier).
3. If repeated facts found (N times), promote to `bella_memory` long-term.

### Using memory in chat

* Retrieve top-N relevant memories for user & channel using embeddings or keyword matching.
* Provide those to LLM with system prompt to create contextual answers.

---

## 15. Image Generation Flow

1. User requests image in Discord or Web UI with a prompt and style.
2. Bot enqueues `image_task` with job id.
3. Worker picks it up, calls the chosen image model (OpenAI, Stability, or local diffusion run).
4. Worker uploads final image to object storage and stores metadata in `media_files` collection.
5. Worker notifies via WebSocket and Discord message with the image link.

Storage: store images on Railway volumes (dev), or optionally use AWS S3 / Backblaze for stability.

---

## 16. Permissions & Security Model

### Role mapping

Map Discord roles to Bella permissions in `guilds.settings.roles`:

* ADMIN — full control
* MOD — moderation commands
* DJ — music control
* USER — regular usage

### Checks

* Each command checks: guild-level enable, role mapping, rate-limit, blacklist
* Admin-only web endpoints require JWT token signed by web server and validated by bot

### Secrets

* Keep `DISCORD_TOKEN`, `MONGO_URI`, `IMAGE_API_KEY`, `JWT_SECRET` in env vars on Railway

---

## 17. Logging, Observability & Metrics

* Use structured logging (JSON) with `loguru` or `structlog`.
* Send critical errors to Sentry or similar.
* Use collection `metrics` in MongoDB or use Railway metrics for quick overviews.
* Track: commands usage, voice minutes, API errors, image generation time.

---

## 18. Testing & CI/CD

* Unit tests for command parsing & services
* Integration tests hitting a test MongoDB and a test Discord bot (use a dev server)
* GitHub Actions (or Railway CI) to run linting and tests
* Docker images for bot & workers, deploy to Railway via GitHub integration

---

## 19. Railway Deployment Guide (short)

1. Create a Railway project.
2. Add a new service for `bot` (Python). Set `DISCORD_TOKEN` and `MONGO_URI` in environment.
3. Add a new service for `web` (Next.js). Set `BOT_API_URL`, `JWT_SECRET`.
4. (Optional) Add `workers` service and `redis` plugin.
5. Use Railway volumes or external S3 for media files.

---

## 20. Milestones & Roadmap (Suggested)

### MVP (1-2 weeks)

* Bot connects to Discord
* Slash commands + help
* Play basic music (join/play/skip) using yt-dlp
* Simple memory save & fetch
* Web UI login + dashboard page

### Phase 2 (2-4 weeks)

* Integrate Lavalink
* Image generation worker
* More advanced memory (promotion rules)
* Web UI: music queue, memory explorer

### Phase 3 (4+ weeks)

* Embeddings & semantic memory
* Auto-moderation & analytics
* Advanced persona editing & TTS
* Multi-worker scaling (Redis)

---

## 21. Example `.env.example`

```
DISCORD_TOKEN=your_discord_bot_token
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/bella
BOT_PUBLIC_URL=https://your-railway-bot.example
JWT_SECRET=supersecretjwt
IMAGE_API_KEY=your-image-api-key
LAVALINK_URL=ws://lavalink:2333
LAVALINK_PASSWORD=lavalink-password
```

---

## 22. Operation & Maintenance Notes

* Make regular database backups (MongoDB Atlas backups)
* Rotate API keys periodically
* Respect privacy: clear audio recordings after X days unless explicitly saved
* Implement a "clear memory" web action to remove long-term memories for a guild or user

---

## 23. Appendices: Useful snippets & quickstarts

### Basic bot entry (`__main__.py`)

```py
import asyncio
from bella_bot.bot import create_bot

async def main():
    bot = create_bot()
    await bot.start()

if __name__ == '__main__':
    asyncio.run(main())
```

### Sample `config.py`

```py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    discord_token: str
    mongo_uri: str
    jwt_secret: str = 'please-change'

    class Config:
        env_file = '.env'

settings = Settings()
```

### Sample FastAPI endpoint to play music (in `api_server.py`)

```py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class PlayBody(BaseModel):
    guildId: str
    query: str

@app.post('/guilds/{guildId}/music/play')
async def play_music(guildId: str, body: PlayBody):
    # enqueue job to the bot memory/music queue
    # validate permission
    return {'status': 'queued'}
```

---

## Final notes & next steps

* This document is intentionally comprehensive. Use it as a single-source blueprint. You can copy-paste folder structure and files as starting point.
* If you want, I can now generate any of these artifacts for you: full `requirements.txt` + `pyproject.toml`, starter `bot.py` scaffolding, Mongoose models (or Pydantic models), or a Next.js starter with OAuth.

Good luck — Bella is going to be awesome. ❤️
