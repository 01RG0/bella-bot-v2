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

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your tokens
3. Run `docker-compose up --build` from the `infra` directory

## Development

See individual directories for setup instructions.
