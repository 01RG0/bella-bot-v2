import os
from google import genai
from google.genai import types
from bot.bella_bot.config import config

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model = "gemini-flash-lite-latest"
        self.tools = [
            types.Tool(url_context=types.UrlContext()),
            types.Tool(code_execution=types.ToolCodeExecution),
            types.Tool(googleSearch=types.GoogleSearch()),
        ]
        # Create config - thinkingConfig will be set via kwargs if supported
        config_kwargs = {
            "temperature": 1.3,
            "tools": self.tools,
        }
        # Try to add thinkingConfig if the API supports it
        # The user's example had thinkingConfig with thinkingBudget, but syntax was incorrect
        # We'll try to set it properly based on the actual API
        try:
            # Attempt to create with thinkingConfig as a dict
            config_kwargs["thinkingConfig"] = {"thinkingBudget": 0}
        except Exception:
            pass
        
        self.config = types.GenerateContentConfig(**config_kwargs)

    async def generate_response(self, message: str, conversation_history: list = None) -> str:
        """
        Generate a response from Gemini.
        
        Args:
            message: The user's message
            conversation_history: Optional list of previous messages for context
            
        Returns:
            The generated response text
        """
        try:
            contents = []
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history:
                    contents.append(
                        types.Content(
                            role=msg.get("role", "user"),
                            parts=[types.Part.from_text(text=msg.get("content", ""))],
                        )
                    )
            
            # Add current message
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=message)],
                )
            )
            
            # Collect streaming response
            full_response = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                
                part = chunk.candidates[0].content.parts[0]
                if part.text:
                    full_response += part.text
                if part.executable_code:
                    # Handle code execution if needed
                    full_response += f"\n[Code: {part.executable_code}]\n"
                if part.code_execution_result:
                    full_response += f"\n[Result: {part.code_execution_result}]\n"
            
            return full_response.strip() if full_response.strip() else "I'm sorry, I couldn't generate a response."
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

    async def generate_response_stream(self, message: str, conversation_history: list = None):
        """
        Generate a streaming response from Gemini (for real-time updates).
        
        Yields:
            Text chunks as they are generated
        """
        try:
            contents = []
            
            if conversation_history:
                for msg in conversation_history:
                    contents.append(
                        types.Content(
                            role=msg.get("role", "user"),
                            parts=[types.Part.from_text(text=msg.get("content", ""))],
                        )
                    )
            
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=message)],
                )
            )
            
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=self.config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                
                part = chunk.candidates[0].content.parts[0]
                if part.text:
                    yield part.text
                    
        except Exception as e:
            yield f"Error: {str(e)}"