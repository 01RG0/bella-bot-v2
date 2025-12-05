# Deployment Instructions

## Prerequisites
- Docker and Docker Compose installed
- .env file with required variables

## Steps
1. Copy .env.example to .env and fill in values
2. Run `docker-compose up --build` from infra directory
3. Access web UI at http://localhost:3000

## Services
- Bot: Discord bot
- Workers: Background task processing
- Web: Frontend dashboard
- Mongo: Database
- Redis: Message broker