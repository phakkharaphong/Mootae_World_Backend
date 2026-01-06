from datetime import datetime, timezone
from sqlalchemy import (
    UUID,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Integer,
)
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name_customer = Column(String(150), nullable=False)
    last_name_customer = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    birth_date_customer_number = Column(Integer)
    birth_month_customer_number = Column(Integer)
    zodiac_customer_number = Column(Integer)
    full_mootext = Column(String(100))
    total_price = Column(Numeric(10, 2))
    payment_status = Column(String(20))
    order_type_id = Column(UUID, ForeignKey("order_type.id"), index=True)
    wallpaper_url = Column(String(255))

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    created_by = Column(String(50))
    updated_at = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    updated_by = Column(String(50))

    order_type = relationship("OrderType", back_populates="orders")
    order_payment = relationship("OrderPayment", back_populates="orders")
