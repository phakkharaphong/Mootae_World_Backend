from datetime import datetime, timezone
from sqlalchemy import UUID, Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), unique=True, index=True, nullable=False)

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

    blogs = relationship("Blog", back_populates="category")
