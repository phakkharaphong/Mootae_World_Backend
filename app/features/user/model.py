from datetime import datetime, timezone
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, String

from app.core.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    username = Column(String(100), index=True, unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    f_name = Column(String(100), index=True, nullable=False)
    l_name = Column(String(100), index=True, nullable=False)
    phone = Column(String(20))
    img_profile = Column(String(255))
    address = Column(String)
    is_admin = Column(Boolean)

    is_active = Column(Boolean)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    created_by = Column(String(50))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    updated_by = Column(String(50))
