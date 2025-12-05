import google.generativeai as genai
from ..config import config

class AIService:
    def __init__(self):
        genai.configure(api_key=config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_response(self, message):
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"