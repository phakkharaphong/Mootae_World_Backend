from datetime import datetime, timezone
import uuid
from sqlalchemy import UUID, Boolean, Column, Date, DateTime, Numeric, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    promocode = Column(String(50), index=True)
    promotion_title = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    discount = Column(Numeric(5, 2))

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


    orders = relationship("Order", back_populates="promotion")
