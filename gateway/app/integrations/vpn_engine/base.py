from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
class VpnEngineClient(ABC):
    @abstractmethod
    async def create_user(self, username: str, quota_bytes: Optional[int], expires_at: Optional[int]) -> Dict[str, Any]:
        pass
    @abstractmethod
    async def modify_user(self, username: str, quota_bytes: Optional[int], expires_at: Optional[int]) -> Dict[str, Any]:
        pass
    @abstractmethod
    async def suspend_user(self, username: str) -> Dict[str, Any]:
        pass
    @abstractmethod
    async def delete_user(self, username: str) -> bool:
        pass
