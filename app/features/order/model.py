from sqlalchemy import Boolean, Column, Date, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(String(50), primary_key=True, index=True)

    emphasize_particular = Column(String(150))
    supplement = Column(String(150))
    supplement_other = Column(String(150))
    birth_date_idol = Column(Date)
    services_zodiac = Column(Boolean)
    services_auspicious = Column(Boolean)
    first_name_customer = Column(String(150))
    last_name_customer = Column(String(150))
    birth_date_customer = Column(Date)
    birth_time_customer = Column(String(20))
    gender = Column(String(100))
    lgbt_description = Column(String(255))
    congenital_disease = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    note = Column(String(255))
    newsletter = Column(Boolean)
    read_accept_pdpa = Column(Boolean)
    promotion_id = Column(String(50))
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
