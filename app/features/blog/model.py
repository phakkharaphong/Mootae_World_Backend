from datetime import datetime, timezone
import uuid
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Blog(Base):
    __tablename__ = "blog"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(150))
    cover_img = Column(String(150))
    content = Column(Text)
    view = Column(Integer)
    like = Column(Integer)
    
    category_id = Column(UUID(50), ForeignKey("category.id"), index=True)

    is_active = Column(Boolean)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    created_by = Column(String(50))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),)
    updated_by = Column(String(50))

    category = relationship("Category", back_populates="blogs")
