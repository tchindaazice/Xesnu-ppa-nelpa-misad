import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from .base import Base

class JoinRequest(Base):
    __tablename__ = "join_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    channel_type = Column(String, nullable=False)
    contact_value_enc = Column(String, nullable=False)
    install_id = Column(String, nullable=False)
    device_pubkey = Column(String, nullable=False)
    reseller_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(String, nullable=False, default="PENDING")
    reviewed_by = Column(UUID(as_uuid=True), nullable=True)
    reject_reason = Column(String, nullable=True)
    ip = Column(String, nullable=True)
    locale = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class VpnAccount(Base):
    __tablename__ = "vpn_accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("join_requests.id"), nullable=False)
    marzban_username = Column(String, unique=True, nullable=False)
    uuid = Column(String, nullable=False)
    plan_id = Column(UUID(as_uuid=True), nullable=True)
    quota_bytes = Column(Integer, nullable=True)
    used_bytes = Column(Integer, default=0)
    expires_at = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="ACTIVE")
    owner_staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=True)
    node_group = Column(String, nullable=True)
    rotated_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = Column(UUID(as_uuid=True), ForeignKey("vpn_accounts.id"), nullable=False)
    install_id = Column(String, nullable=False)
    pubkey = Column(String, nullable=False)
    platform = Column(String, nullable=True)
    model = Column(String, nullable=True)
    app_version = Column(String, nullable=True)
    attestation_ok = Column(Boolean, default=False)
    first_seen = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
