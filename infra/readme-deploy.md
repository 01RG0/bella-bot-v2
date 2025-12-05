# Deployment Instructions

## Prerequisites
- Docker and Docker Compose installed (for Bot, Workers, Web, Mongo)
- Redis installed locally (for message broker)
- Java 11+ installed (for Lavalink)
- .env file with required variables

## Local Setup (Recommended)
1. Install Redis: `choco install redis-64` (Windows) or `brew install redis` (macOS)
2. Download Lavalink.jar from https://github.com/lavalink-devs/Lavalink/releases and place in `infra/` directory
3. Copy .env.example to .env and fill in values (uses localhost for Redis/Lavalink)
4. Run `./scripts/run.sh` (Linux/Mac) or `./scripts/run.bat` (Windows)
5. Access web UI at http://localhost:3000

## Docker-Only Setup (Alternative)
1. Copy .env.example to .env and update Redis/Lavalink to use Docker services
2. Run `docker-compose up --build` from infra directory
3. Access web UI at http://localhost:3000

## Services
- Bot: Discord bot (Docker)
- Workers: Background task processing (Docker)
- Web: Frontend dashboard (Docker)
- Mongo: Database (Docker)
- Redis: Message broker (Local or Docker)
- Lavalink: Audio server for music playback (Local or Docker)