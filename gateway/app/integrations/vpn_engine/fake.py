from typing import Dict, Any, Optional
from .base import VpnEngineClient
import uuid
class FakeEngine(VpnEngineClient):
    def __init__(self):
        self.users = {}
    async def create_user(self, username: str, quota_bytes: Optional[int], expires_at: Optional[int]) -> Dict[str, Any]:
        if username in self.users:
            raise ValueError("User already exists")
        user_uuid = str(uuid.uuid4())
        user_data = {
            "username": username,
            "uuid": user_uuid,
            "quota_bytes": quota_bytes,
            "expires_at": expires_at,
            "status": "active"
        }
        self.users[username] = user_data
        return user_data
    async def modify_user(self, username: str, quota_bytes: Optional[int], expires_at: Optional[int]) -> Dict[str, Any]:
        if username not in self.users:
            raise ValueError("User not found")
        self.users[username]["quota_bytes"] = quota_bytes
        self.users[username]["expires_at"] = expires_at
        return self.users[username]
    async def suspend_user(self, username: str) -> Dict[str, Any]:
        if username not in self.users:
            raise ValueError("User not found")
        self.users[username]["status"] = "suspended"
        return self.users[username]
    async def delete_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            return True
        return False
