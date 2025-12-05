import openai
from ..config import config

class AIService:
    def __init__(self):
        openai.api_key = config.OPENAI_API_KEY

    async def generate_response(self, message):
        # TODO: Implement AI response generation
        return f"AI response to: {message}"