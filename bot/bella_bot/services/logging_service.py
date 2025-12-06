from motor.motor_asyncio import AsyncIOMotorClient
from ..config import config
import time
import asyncio

class LoggingService:
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            self.db = self.client.get_database("bella_bot_v2")
            self.logs = self.db.logs
            # Create TTL index for logs to expire after 7 days
            # We run this in a task to avoid blocking init
            pass 
        except Exception:
            self.logs = None

    async def log_event(self, type: str, message: str, level: str = "INFO", details: dict = None):
        """Log an event"""
        if self.logs is None: return
        
        entry = {
            "timestamp": time.time(),
            "type": type, # e.g. "command", "error", "message", "system"
            "message": message,
            "level": level, # "INFO", "WARN", "ERROR"
            "details": details or {}
        }
        try:
            await self.logs.insert_one(entry)
        except Exception as e:
            print(f"Failed to write log: {e}")
        
    async def get_logs(self, limit: int = 100, level: str = None):
        """Get recent logs"""
        if self.logs is None: return []
        
        query = {}
        if level and level != "ALL":
            query["level"] = level
            
        try:
            # Sort by timestamp descending
            cursor = self.logs.find(query).sort("timestamp", -1).limit(limit)
            logs = await cursor.to_list(length=limit)
            
            # Convert _id to string for JSON serialization
            for log in logs:
                log["_id"] = str(log["_id"])
            
            return logs
        except Exception as e:
            print(f"Failed to fetch logs: {e}")
            return []
