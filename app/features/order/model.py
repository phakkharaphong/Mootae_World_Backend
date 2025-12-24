from sqlalchemy import Boolean, Column, Date, ForeignKey, Numeric, String, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(String(50), primary_key=True, index=True)
    first_name_customer = Column(String(150))
    last_name_customer = Column(String(150))
    email = Column(String(100))
    phone = Column(String(20))
    congenital_disease = Column(String(100)) 
    note = Column(String(255))
    gender = Column(String(100))
    birth_date_customer = Column(String(100))
    birth_date_customer_number = Column(Integer)
    birth_month_customer = Column(String(100))
    birth_month_customer_number = Column(Integer)
    zodiac_customer = Column(String(100))
    zodiac_customer_number = Column(Integer)
    promotion_id = Column(String(50), ForeignKey("promotions.id"), index=True)
    total_price = Column(Numeric(10, 2))
    payment_status = Column(String(20))
    send_wallpaper_status = Column(String(20))
    order_type_id = Column(String(50), ForeignKey("order_type.id"), index=True)

    is_active = Column(Boolean, index=True)

    created_at = Column(Date)
    created_by = Column(String(50), index=True)
    updated_at = Column(Date)
    updated_by = Column(String(50), index=True)

    order_type = relationship("OrderType", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
