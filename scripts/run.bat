@echo off
REM Bella Bot - Manual Run Script for Windows
REM This script helps run the project locally using Docker Compose

echo 🚀 Starting Bella Bot project...

REM Check if .env exists
if not exist "..\.env" (
    echo ❌ .env file not found. Please create it from .env.example
    pause
    exit /b 1
)

REM Check if docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    exit /b 1
)

REM Check if docker-compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Build and start services
echo 🏗️  Building and starting services...
cd ..\infra
docker-compose up --build -d

echo ✅ Services started successfully!
echo.
echo 🌐 Web UI: http://localhost:3000
echo 📊 MongoDB: localhost:27017
echo 🔄 Redis: localhost:6379
echo.
echo To view logs: docker-compose logs -f
echo To stop: docker-compose down
pause