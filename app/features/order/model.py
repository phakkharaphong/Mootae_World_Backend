from datetime import datetime, timezone
from sqlalchemy import UUID,Boolean, Column, Date, DateTime, ForeignKey, Numeric, String, Integer
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name_customer = Column(String(150), unique=True, index=True, nullable=False)
    last_name_customer = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20))
    congenital_disease = Column(String(100)) 
    note = Column(String(255))
    gender = Column(String(100))
    birth_date_customer = Column(String(100), index=True, nullable=False)
    birth_date_customer_number = Column(Integer)
    birth_month_customer = Column(String(100), index=True, nullable=False)
    birth_month_customer_number = Column(Integer)
    zodiac_customer = Column(String(100), index=True, nullable=False)
    zodiac_customer_number = Column(Integer)
    promotion_id = Column(UUID, ForeignKey("promotions.id"), index=True)
    total_price = Column(Numeric(10, 2))
    payment_status = Column(String(20))
    send_wallpaper_status = Column(String(20))
    order_type_id = Column(UUID, ForeignKey("order_type.id"), index=True)

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

    order_type = relationship("OrderType", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
