from sqlalchemy import Boolean, Column, Float, String, Date, DateTime, Numeric,ForeignKey
from database_config import Base
from sqlalchemy.orm import relationship
class mtw_orders(Base):
    __tablename__ = "mtw_orders"

    id = Column(String(50), primary_key=True, index=True)
    order_type_id = Column(String(50), ForeignKey("mtw_orders_type.id"), index=True)
    emphasize_particular = Column(String(150))
    supplement = Column(String(150))
    supplement_other = Column(String(150))
    
    birth_date_idol = Column(Date)
    services_zodiac = Column(Boolean)
    services_auspicious = Column(Boolean)
    frist_name_customer = Column(String(150))
    last_name_customer = Column(String(150))
    birth_date_customer = Column(Date)
    birth_time_customer = Column(String(20))
    gendor = Column(String(100))
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
    send_wallpaer_status = Column(String(20))
    is_active = Column(Boolean, index=True)
    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
    # Relationship
    order_type = relationship("mtw_orders_type", back_populates="orders")
