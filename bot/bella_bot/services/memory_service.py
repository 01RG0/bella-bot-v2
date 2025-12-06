from motor.motor_asyncio import AsyncIOMotorClient
from ..config import config
import time
import asyncio

class MemoryService:
    def __init__(self):
        # Use motor for async MongoDB
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            self.db = self.client.get_database("bella_bot_v2")
            self.users = self.db.users
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            self.users = None

    async def update_user_interaction(self, user_id: str, username: str, roles: list[str]):
        """Update user info and last seen timestamp"""
        if self.users is None: return
        
        try:
            await self.users.update_one(
                {"user_id": str(user_id)},
                {
                    "$set": {
                        "username": username,
                        "roles": roles,
                        "last_seen": time.time()
                    },
                    "$setOnInsert": {
                        "facts": [],
                        "conversation_summary": "",
                        "created_at": time.time()
                    }
                },
                upsert=True
            )
        except Exception as e:
            print(f"Error updating user memory: {e}")

    async def get_memory(self, user_id: str) -> dict:
        """Get user memory facts and context"""
        if self.users is None: return {"facts": [], "roles": []}
        
        user = await self.users.find_one({"user_id": str(user_id)})
        if not user:
            return {"facts": [], "roles": []}
            
        return {
            "facts": user.get("facts", []),
            "roles": user.get("roles", []),
            "summary": user.get("conversation_summary", "")
        }

    async def add_memory_fact(self, user_id: str, fact: str):
        """Add a specific fact to user memory"""
        if self.users is None: return
        await self.users.update_one(
            {"user_id": str(user_id)},
            {"$push": {"facts": fact}}
        )