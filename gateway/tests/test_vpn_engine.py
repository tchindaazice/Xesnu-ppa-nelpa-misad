import pytest
from app.integrations.vpn_engine.fake import FakeEngine
from app.integrations.vpn_engine.marzban import MarzbanClient
from unittest.mock import patch, AsyncMock
import httpx
@pytest.fixture
def fake_engine():
    return FakeEngine()
@pytest.mark.asyncio
async def test_fake_engine_lifecycle(fake_engine):
    user = await fake_engine.create_user("testuser", 1000, 123456789)
    assert user["username"] == "testuser"
    assert user["status"] == "active"
    modified = await fake_engine.modify_user("testuser", 2000, 987654321)
    assert modified["quota_bytes"] == 2000
    suspended = await fake_engine.suspend_user("testuser")
    assert suspended["status"] == "suspended"
    deleted = await fake_engine.delete_user("testuser")
    assert deleted is True
@pytest.mark.asyncio
async def test_marzban_client_lifecycle():
    client = MarzbanClient()
    mock_request = httpx.Request("POST", "http://test")
    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_response = httpx.Response(200, json={"username": "testuser", "data_limit": 1000}, request=mock_request)
        mock_post.return_value = mock_response
        user = await client.create_user("testuser", 1000, 123456789)
        assert user["username"] == "testuser"
        assert user["data_limit"] == 1000
        mock_post.assert_called_once()
    with patch("httpx.AsyncClient.put", new_callable=AsyncMock) as mock_put:
        mock_response = httpx.Response(200, json={"username": "testuser", "data_limit": 2000}, request=mock_request)
        mock_put.return_value = mock_response
        user = await client.modify_user("testuser", 2000, None)
        assert user["data_limit"] == 2000
        mock_put.assert_called_once()
    with patch("httpx.AsyncClient.put", new_callable=AsyncMock) as mock_put:
        mock_response = httpx.Response(200, json={"username": "testuser", "status": "disabled"}, request=mock_request)
        mock_put.return_value = mock_response
        user = await client.suspend_user("testuser")
        assert user["status"] == "disabled"
        mock_put.assert_called_once()
    with patch("httpx.AsyncClient.delete", new_callable=AsyncMock) as mock_delete:
        mock_response = httpx.Response(200, request=mock_request)
        mock_delete.return_value = mock_response
        result = await client.delete_user("testuser")
        assert result is True
        mock_delete.assert_called_once()
