from sqlalchemy import Boolean, Column, DateTime, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class OrderType(Base):
    __tablename__ = "order_type"

    id = Column(String(50), primary_key=True, index=True)

    type_name = Column(String(150), index=True)
    price = Column(Numeric(10, 2))

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)

    orders = relationship("Order", back_populates="order_type")
