import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    LAVALINK_HOST = os.getenv('LAVALINK_HOST', 'localhost')
    LAVALINK_PORT = int(os.getenv('LAVALINK_PORT', 2333))
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    # Add other env vars as needed

config = Config()