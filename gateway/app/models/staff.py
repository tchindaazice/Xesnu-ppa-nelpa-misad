import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Enum, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from datetime import datetime, timezone
import enum
from .base import Base

class StaffRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    RESELLER = "RESELLER"

class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(StaffRole), nullable=False)
    totp_secret_enc = Column(String, nullable=True) # Could be encrypted, storing plain for MVP
    country_scope = Column(JSON(), nullable=True)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
