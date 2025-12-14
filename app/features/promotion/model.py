from sqlalchemy import Boolean, Column, Date, DateTime, Numeric, String
from app.core.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(String(50), primary_key=True, index=True)

    promocode = Column(String(50), index=True)
    promotion_title = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    discount = Column(Numeric(5, 2))

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
