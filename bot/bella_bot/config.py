import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
# Calculate path from bot/bella_bot/config.py -> root
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    POLLINATIONS_TOKEN = os.getenv("POLLINATIONS_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    
    # Lavalink / Music
    LAVALINK_HOST = os.getenv("LAVALINK_HOST", "localhost")
    LAVALINK_PORT = int(os.getenv("LAVALINK_PORT", 2333))
    LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD", "youshallnotpass")
    LAVALINK_SECURE = os.getenv("LAVALINK_SECURE", "false").lower() == "true"

config = Config()
