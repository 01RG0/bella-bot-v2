from fastapi import FastAPI, HTTPException, Form, WebSocket, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from uvicorn import run
import os
from dotenv import load_dotenv
import httpx
from fastapi.middleware.cors import CORSMiddleware
import json

from .ws import WebSocketManager

load_dotenv()

app = FastAPI()

# Configure CORS for the frontend
frontend_origin = os.getenv("VITE_API_ALLOW_ORIGIN", "http://localhost:5173")
allowed_origins = [
    frontend_origin,
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # Alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Bella Bot API"}


@app.post("/auth/discord/token")
async def exchange_discord_token(code: str = Form(...)):
    """Exchange OAuth authorization code for tokens server-side.

    Expects `code` (form) and uses environment variables for client id/secret/redirect.
    """
    client_id = os.getenv("VITE_DISCORD_CLIENT_ID") or os.getenv("DISCORD_CLIENT_ID")
    client_secret = os.getenv("VITE_DISCORD_CLIENT_SECRET") or os.getenv("DISCORD_CLIENT_SECRET")
    redirect_uri = os.getenv("VITE_DISCORD_REDIRECT_URI") or os.getenv("DISCORD_REDIRECT_URI")

    if not client_id or not client_secret or not redirect_uri:
        raise HTTPException(status_code=500, detail="OAuth server misconfiguration")

    token_url = "https://discord.com/api/oauth2/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient() as client:
        resp = await client.post(token_url, data=data, headers=headers, timeout=10)

    if resp.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Discord token exchange failed: {resp.text}")

    return resp.json()


# Simple WebSocket manager and endpoints so the web dashboard can receive live events
ws_manager = WebSocketManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            # Keep connection open; ignore incoming messages for now
            await websocket.receive_text()
    except Exception:
        ws_manager.disconnect(websocket)


# ... imports ...
from .services.logging_service import LoggingService
logging_service = LoggingService()

# ... existing code ...

@app.post("/events")
async def post_event(request: Request):
    """Receive events (from the bot process) and broadcast to connected websocket clients."""
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # Persist log
    try:
        await logging_service.log_event(
            type=payload.get("type", "system"),
            message=f"Event: {payload.get('type')}",
            details=payload.get("payload")
        )
    except Exception:
        pass

    try:
        text = json.dumps(payload)
        await ws_manager.broadcast(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to broadcast event: {e}")

    return {"status": "ok"}


@app.get("/api/logs")
async def get_logs_api(limit: int = 50, level: str = "ALL"):
    """Get system logs"""
    return {"logs": await logging_service.get_logs(limit, level)}


# Image Generation API endpoints
# ... rest of file ...


# Image Generation API endpoints
from .services.image_service import ImageService
from .config import config

image_service = ImageService(
    default_model=config.IMAGE_MODEL,
    auth_token=config.POLLINATIONS_TOKEN
)

@app.get("/api/image/models")
async def get_image_models():
    """Get available image generation models and current model"""
    return {
        "models": image_service.AVAILABLE_MODELS,
        "current_model": image_service.get_current_model()
    }

@app.post("/api/image/model")
async def set_image_model(model: str):
    """Set the default image generation model"""
    if image_service.set_model(model):
        return {"success": True, "model": model}
    raise HTTPException(status_code=400, detail=f"Invalid model. Choose from: {image_service.AVAILABLE_MODELS}")

@app.post("/api/image/generate")
async def generate_image_api(request: Request):
    """Generate an image from a prompt"""
    try:
        data = await request.json()
        prompt = data.get("prompt")
        model = data.get("model")
        width = data.get("width", 1024)
        height = data.get("height", 1024)
        enhance = data.get("enhance", False)
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Validate dimensions
        if width < 256 or width > 2048 or height < 256 or height > 2048:
            raise HTTPException(status_code=400, detail="Width and height must be between 256 and 2048")
        
        image_url = await image_service.generate_image(
            prompt=prompt,
            model=model,
            width=width,
            height=height,
            enhance=enhance
        )
        
        return {
            "success": True,
            "image_url": image_url,
            "prompt": prompt,
            "model": model or image_service.get_current_model(),
            "width": width,
            "height": height
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Behavior / System Instruction API
from .services.behavior_service import BehaviorService
behavior_service = BehaviorService()



# Behavior / System Instruction API
# ... imports usually at top ...
# from .services.behavior_service import BehaviorService
# behavior_service = BehaviorService() # Assumed initialized above or here

@app.get("/api/behaviors/config")
async def get_behavior_config():
    """Get full behavior configuration"""
    return behavior_service.get_full_config()

@app.post("/api/behaviors/persona")
async def update_persona(request: Request):
    """Create or update a persona"""
    try:
        data = await request.json()
        behavior_service.update_persona(data["id"], data["name"], data["prompt"])
        return {"success": True, "config": behavior_service.get_full_config()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/behaviors/persona/{pid}")
async def delete_persona(pid: str):
    """Delete a persona"""
    behavior_service.delete_persona(pid)
    return {"success": True, "config": behavior_service.get_full_config()}

@app.post("/api/behaviors/assign/user")
async def assign_user(request: Request):
    """Assign a persona to a User ID"""
    data = await request.json()
    behavior_service.assign_user(data["userId"], data["personaId"])
    return {"success": True}

@app.post("/api/behaviors/assign/role")
async def assign_role(request: Request):
    """Assign a persona to a Role Name"""
    data = await request.json()
    behavior_service.assign_role(data["role"], data["personaId"])
    return {"success": True}

@app.post("/api/behaviors/default")
async def set_default_persona(request: Request):
    """Set the default persona"""
    data = await request.json()
    behavior_service.set_default_persona(data["personaId"])
    return {"success": True}

@app.post("/api/behaviors/guidelines")
async def set_guidelines(request: Request):
    """Set global guidelines appended to all prompts"""
    data = await request.json()
    behavior_service.set_global_guidelines(data["text"])
    return {"success": True}
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
static_dir = os.path.join(project_root, "web", "dist")

if os.path.exists(static_dir):
    # Mount assets (JS/CSS/Images)
    if os.path.exists(os.path.join(static_dir, "assets")):
        app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="assets")
    
    # Catch-all for SPA routing
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # API routes are prioritized by FastAPI order, but we can verify
        if full_path.startswith("api/") or full_path.startswith("auth/") or full_path.startswith("events") or full_path.startswith("ws"):
             raise HTTPException(status_code=404)

        # Check for specific file request
        file_path = os.path.join(static_dir, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        # Default to index.html for unknown routes (Client-side routing)
        return FileResponse(os.path.join(static_dir, "index.html"))


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
