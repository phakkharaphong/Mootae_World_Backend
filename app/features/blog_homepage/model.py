from datetime import datetime, timezone
from sqlalchemy import UUID,Boolean, Column, DateTime, String
from app.core.database import Base
import uuid

class BlogHomepage(Base):
    __tablename__ = "blog_home_page"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(200))
    note = Column(String(150))
    img_path = Column(String(150))
    link = Column(String(150))

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

