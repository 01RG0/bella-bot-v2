import httpx
import urllib.parse
from typing import Literal

ImageModel = Literal["flux", "turbo", "stable-diffusion"]

class ImageService:
    """Image generation service using Pollinations.ai API"""
    
    BASE_URL = "https://image.pollinations.ai/prompt"
    AVAILABLE_MODELS = ["flux", "turbo", "stable-diffusion"]
    
    def __init__(self, default_model: str = "flux", auth_token: str = None):
        self.default_model = default_model if default_model in self.AVAILABLE_MODELS else "flux"
        self.auth_token = auth_token
    
    def set_model(self, model: str) -> bool:
        """Set the default model for image generation"""
        if model in self.AVAILABLE_MODELS:
            self.default_model = model
            return True
        return False
    
    def get_current_model(self) -> str:
        """Get the currently selected model"""
        return self.default_model
    
    async def generate_image(
        self, 
        prompt: str, 
        model: str = None,
        width: int = 1024,
        height: int = 1024,
        seed: int = None,
        nologo: bool = True,
        enhance: bool = False
    ) -> str:
        """
        Generate an image using Pollinations AI
        
        Args:
            prompt: Text description of the image
            model: Model to use (flux, turbo, stable-diffusion). Uses default if None
            width: Image width (default 1024)
            height: Image height (default 1024)
            seed: Random seed for reproducibility
            nologo: Remove Pollinations logo (default True)
            enhance: Enhance prompt automatically (default False)
        
        Returns:
            URL to the generated image
        """
        # Use default model if not specified
        if model is None or model not in self.AVAILABLE_MODELS:
            model = self.default_model
        
        # Encode the prompt for URL
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Build URL with parameters
        url = f"{self.BASE_URL}/{encoded_prompt}"
        
        params = {
            "model": model,
            "width": width,
            "height": height,
            "nologo": str(nologo).lower(),
            "enhance": str(enhance).lower()
        }
        
        if seed is not None:
            params["seed"] = seed
        
        # Build query string
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        full_url = f"{url}?{query_string}"
        
        return full_url
    
    async def generate_image_bytes(
        self, 
        prompt: str, 
        model: str = None,
        width: int = 1024,
        height: int = 1024
    ) -> bytes:
        """
        Generate an image and return the raw bytes
        
        Args:
            prompt: Text description of the image
            model: Model to use (flux, turbo, stable-diffusion)
            width: Image width
            height: Image height
        
        Returns:
            Image data as bytes
        """
        url = await self.generate_image(prompt, model, width, height)
        
        # Prepare headers with authentication if token exists
        headers = {}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.content