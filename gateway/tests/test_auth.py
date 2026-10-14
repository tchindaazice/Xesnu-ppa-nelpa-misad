import pytest
from datetime import datetime, timedelta, timezone
from app.core.security import verify_password, get_password_hash, create_access_token, generate_totp_secret, verify_totp
import pyotp

def test_password_hashing():
    password = "supersecretpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_jwt_generation():
    token = create_access_token(subject="user_123")
    assert isinstance(token, str)
    assert len(token) > 0

def test_totp():
    secret = generate_totp_secret()
    assert isinstance(secret, str)

    totp = pyotp.TOTP(secret)
    valid_code = totp.now()

    assert verify_totp(secret, valid_code) is True
    assert verify_totp(secret, "000000") is False

@pytest.mark.asyncio
async def test_login_flow():
    from app.models.staff import Staff, StaffRole
    from app.api.routers.auth import login, LoginRequest
    from fastapi import HTTPException
    import uuid
    from unittest.mock import AsyncMock

    hashed_password = get_password_hash("password123")
    totp_secret = generate_totp_secret()

    mock_staff = Staff(
        id=uuid.uuid4(),
        email="admin@test.com",
        password_hash=hashed_password,
        role=StaffRole.ADMIN,
        totp_secret_enc=totp_secret,
        failed_login_attempts=0
    )

    # Mocking the async db session and the get_staff_by_email query behavior
    mock_db = AsyncMock()

    # We patch the DB fetch behavior directly in the test to bypass the DB engine
    import app.api.routers.auth
    app.api.routers.auth.get_staff_by_email = AsyncMock(return_value=mock_staff)

    # 1. Missing TOTP for admin
    with pytest.raises(HTTPException) as exc:
        await login(LoginRequest(email="admin@test.com", password="password123"), mock_db)
    assert exc.value.status_code == 401
    assert "TOTP code required" in exc.value.detail

    # 2. Invalid TOTP
    with pytest.raises(HTTPException) as exc:
        await login(LoginRequest(email="admin@test.com", password="password123", totp_code="000000"), mock_db)
    assert exc.value.status_code == 401
    assert "Invalid TOTP" in exc.value.detail

    # 3. Successful Login
    valid_totp = pyotp.TOTP(totp_secret).now()
    response = await login(LoginRequest(email="admin@test.com", password="password123", totp_code=valid_totp), mock_db)
    assert response.access_token is not None
    assert response.refresh_token is not None
    assert mock_staff.failed_login_attempts == 0
    mock_db.commit.assert_called()

    # 4. Failed Password & Lockout Simulation
    with pytest.raises(HTTPException):
        await login(LoginRequest(email="admin@test.com", password="wrongpassword", totp_code=valid_totp), mock_db)
    assert mock_staff.failed_login_attempts == 1

    mock_staff.failed_login_attempts = 5
    mock_staff.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)

    with pytest.raises(HTTPException) as exc:
         await login(LoginRequest(email="admin@test.com", password="password123", totp_code=valid_totp), mock_db)
    assert exc.value.status_code == 403
    assert "Account locked" in exc.value.detail
