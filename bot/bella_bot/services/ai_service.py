import os
from google import genai
from google.genai import types
from ..config import config

class AIService:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self.model = "gemini-flash-lite-latest"
        self.tools = [
            types.Tool(url_context=types.UrlContext()),
            types.Tool(code_execution=types.ToolCodeExecution),
            types.Tool(googleSearch=types.GoogleSearch()),
        ]

    def _create_config(self, system_instruction: str = None):
        config_kwargs = {
            "temperature": 1.3,
            "tools": self.tools,
        }
        try:
            config_kwargs["thinkingConfig"] = {"thinkingBudget": 0}
        except Exception:
            pass
        
        conf = types.GenerateContentConfig(**config_kwargs)
        
        if system_instruction:
            conf.system_instruction = types.Part.from_text(text=system_instruction)
            
        return conf

    async def generate_response(self, message: str, conversation_history: list = None, user_context: str = None, system_instruction: str = None) -> tuple[str, list[str]]:
        """
        Generate a response from Gemini.
        """
        # Prepare System Instruction
        base_instruction = system_instruction or ""
        full_instruction = base_instruction
        if user_context:
            full_instruction = f"{base_instruction}\n\nCONTEXT:\n{user_context}".strip()
            
        full_instruction += "\n\nSYSTEM: If you learn a new IMPORTANT fact about the user, specifically likes, dislikes, names, or key details, save it by adding [MEMORY: the fact] at the end of your response."

        # Create Config for this request
        req_config = self._create_config(full_instruction)

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
            
            full_response = ""
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=req_config,
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
                    full_response += f"\n[Code: {part.executable_code}]\n"
                if part.code_execution_result:
                    full_response += f"\n[Result: {part.code_execution_result}]\n"
            
            final_text = full_response.strip() if full_response.strip() else "I'm sorry, I couldn't generate a response."
            
            memory_updates = []
            if "[MEMORY:" in final_text:
                import re
                matches = re.findall(r'\[MEMORY: (.*?)\]', final_text, re.IGNORECASE)
                memory_updates = matches
                final_text = re.sub(r'\[MEMORY:.*?\]', '', final_text, flags=re.IGNORECASE).strip()

            return final_text, memory_updates
            
        except Exception as e:
            return f"Error generating response: {str(e)}", []

    async def generate_response_stream(self, message: str, conversation_history: list = None):
        # Default stream (no special context/system for simple stream for now)
        req_config = self._create_config()
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
                config=req_config,
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