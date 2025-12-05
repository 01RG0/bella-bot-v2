#!/bin/bash

# Bella Bot - Manual Run Script
# This script helps run the project locally using Docker Compose

set -e

echo "🚀 Starting Bella Bot project..."

# Check if .env exists
if [ ! -f "../.env" ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Check if docker and docker-compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Start local services
echo "🏗️  Starting local services..."

# Start Redis
if command -v redis-server &> /dev/null; then
    echo "Starting Redis..."
    redis-server --daemonize yes
else
    echo "❌ Redis not installed. Please install Redis first."
    exit 1
fi

# Start Lavalink
cd ../infra
if [ -f "Lavalink.jar" ]; then
    echo "Starting Lavalink..."
    java -jar Lavalink.jar &
else
    echo "❌ Lavalink.jar not found. Please download it from https://github.com/lavalink-devs/Lavalink/releases"
    exit 1
fi

# Start Docker services (Bot, Workers, Web, Mongo)
echo "Starting Docker services..."
docker-compose up --build -d bot workers web mongo

echo "✅ Services started successfully!"
echo ""
echo "🌐 Web UI: http://localhost:3000"
echo "📊 MongoDB: localhost:27017"
echo "🔄 Redis: localhost:6379"
echo "🎵 Lavalink: localhost:2333"
echo ""
echo "To view Docker logs: docker-compose logs -f"
echo "To stop: docker-compose down && pkill redis-server && pkill java"