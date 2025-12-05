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

# Build and start services
echo "🏗️  Building and starting services..."
cd ../infra
docker-compose up --build -d

echo "✅ Services started successfully!"
echo ""
echo "🌐 Web UI: http://localhost:3000"
echo "📊 MongoDB: localhost:27017"
echo "🔄 Redis: localhost:6379"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"