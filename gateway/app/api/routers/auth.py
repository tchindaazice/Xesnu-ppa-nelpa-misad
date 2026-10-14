from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import verify_password, create_access_token, create_refresh_token, verify_totp
from app.models.staff import Staff, StaffRole
from app.core.database import get_db

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str
    totp_code: Optional[str] = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

async def get_staff_by_email(email: str, db: AsyncSession) -> Optional[Staff]:
    result = await db.execute(select(Staff).where(Staff.email == email))
    return result.scalars().first()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):

    # 1. Fetch user by email
    staff = await get_staff_by_email(login_data.email, db)

    if not staff:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if staff.locked_until and staff.locked_until > datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account locked")

    # 2. Verify password
    if not verify_password(login_data.password, staff.password_hash):
        staff.failed_login_attempts += 1
        if staff.failed_login_attempts >= 5:
            staff.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
        await db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    # Reset failed attempts on success
    staff.failed_login_attempts = 0
    staff.locked_until = None

    # 3. Verify TOTP if required (SUPER_ADMIN and ADMIN)
    if staff.role in [StaffRole.SUPER_ADMIN, StaffRole.ADMIN]:
        if not login_data.totp_code:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="TOTP code required")
        if not staff.totp_secret_enc or not verify_totp(staff.totp_secret_enc, login_data.totp_code):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid TOTP code")

    # 4. Generate tokens
    access_token = create_access_token(subject=str(staff.id))
    refresh_token = create_refresh_token(subject=str(staff.id))

    staff.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )
