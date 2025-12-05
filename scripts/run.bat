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

REM Start local services
echo 🏗️  Starting local services...

REM Start Redis
redis-server --daemonize yes
if errorlevel 1 (
    echo ❌ Redis not installed or failed to start. Please install Redis first.
    pause
    exit /b 1
)

REM Start Lavalink
cd ..\infra
if exist "Lavalink.jar" (
    echo Starting Lavalink...
    start /B java -jar Lavalink.jar
) else (
    echo ❌ Lavalink.jar not found. Please download it from https://github.com/lavalink-devs/Lavalink/releases
    pause
    exit /b 1
)

REM Start Docker services (Bot, Workers, Web, Mongo)
echo Starting Docker services...
docker-compose up --build -d bot workers web mongo

echo ✅ Services started successfully!
echo.
echo 🌐 Web UI: http://localhost:3000
echo 📊 MongoDB: localhost:27017
echo 🔄 Redis: localhost:6379
echo 🎵 Lavalink: localhost:2333
echo.
echo To view Docker logs: docker-compose logs -f
echo To stop: docker-compose down && taskkill /F /IM redis-server.exe && taskkill /F /IM java.exe
pause