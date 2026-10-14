import httpx
from typing import Dict, Any, Optional
from .base import VpnEngineClient
from app.core.config import settings
class MarzbanClient(VpnEngineClient):
    def __init__(self):
        self.base_url = settings.marzban_api_url
        self.token = None
    async def _get_client(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        return httpx.AsyncClient(base_url=self.base_url, headers=headers)
    async def create_user(self, username: str, quota_bytes: Optional[int], expires_at: Optional[int]) -> Dict[str, Any]:
        async with await self._get_client() as client:
            payload = {"username": username, "data_limit": quota_bytes, "expire": expires_at, "proxies": {"vless": {}}}
            response = await client.post("/api/user", json=payload)
            response.raise_for_status()
            return response.json()
    async def modify_user(self, username: str, quota_bytes: Optional[int], expires_at: Optional[int]) -> Dict[str, Any]:
        async with await self._get_client() as client:
            payload = {}
            if quota_bytes is not None: payload["data_limit"] = quota_bytes
            if expires_at is not None: payload["expire"] = expires_at
            response = await client.put(f"/api/user/{username}", json=payload)
            response.raise_for_status()
            return response.json()
    async def suspend_user(self, username: str) -> Dict[str, Any]:
        async with await self._get_client() as client:
            payload = {"status": "disabled"}
            response = await client.put(f"/api/user/{username}", json=payload)
            response.raise_for_status()
            return response.json()
    async def delete_user(self, username: str) -> bool:
        async with await self._get_client() as client:
            response = await client.delete(f"/api/user/{username}")
            return response.status_code == 200
