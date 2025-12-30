from datetime import datetime, timezone
from sqlalchemy import UUID, Boolean, Column, DateTime, Numeric, String
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class OrderType(Base):
    __tablename__ = "order_type"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    type_name = Column(String(150), unique=True, index=True, nullable=False)
    price = Column(Numeric(10, 2))
    key = Column(String(100), unique=True, index=True, nullable=True)

    is_active = Column(Boolean)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    created_by = Column(String(50))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    updated_by = Column(String(50))

    orders = relationship("Order", back_populates="order_type")
