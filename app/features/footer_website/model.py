from datetime import datetime, timezone
from sqlalchemy import UUID, Boolean, Column, DateTime, String
from app.core.database import Base
import uuid

class FooterWebsite(Base):
    __tablename__ = "footer_website"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(150), index=True)
    icon_img = Column(String(100))
    link_ref = Column(String(100))

    is_active = Column(Boolean)

    created_at = Column(
        DateTime(timezone=True), 
        default=datetime.now(timezone.utc)
    )
    created_by = Column(String(50))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    updated_by = Column(String(50))
