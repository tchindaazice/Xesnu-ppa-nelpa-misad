from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.vpn import JoinRequest

router = APIRouter()

class RegisterRequest(BaseModel):
    full_name: str
    country_code: str
    channel_type: str
    contact_value: str
    install_id: str
    device_pubkey: str
    reseller_code: Optional[str] = None

class RegisterResponse(BaseModel):
    status: str
    message: str

@router.post("/register", response_model=RegisterResponse)
async def register(request_data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # 1. Validation and Rate Limiting (to be implemented with Redis)

    # 2. Create the join request in PENDING state
    # Note: Contact value should be encrypted before storage
    new_request = JoinRequest(
        full_name=request_data.full_name,
        country_code=request_data.country_code,
        channel_type=request_data.channel_type,
        contact_value_enc=f"enc_{request_data.contact_value}", # stub encryption
        install_id=request_data.install_id,
        device_pubkey=request_data.device_pubkey,
        status="PENDING"
    )

    db.add(new_request)
    await db.commit()

    # 3. Trigger notifications (e.g. Telegram Bot) asynchronously

    return RegisterResponse(
        status="PENDING",
        message="Your request has been submitted and is pending review."
    )
