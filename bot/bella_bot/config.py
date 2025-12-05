import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    LAVALINK_HOST = os.getenv('LAVALINK_HOST', 'localhost')
    LAVALINK_PORT = int(os.getenv('LAVALINK_PORT', 2333))
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCS3aIGspuSCZVI6-H6qd6HyatzWCnH9Q4')
    # Add other env vars as needed

config = Config()