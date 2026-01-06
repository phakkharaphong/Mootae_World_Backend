from datetime import datetime, timezone
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Numeric, String
import uuid
from app.core.database import Base
from sqlalchemy.orm import relationship

class OrderPayment(Base):
    __tablename__ = "order_payment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    amount = Column(Numeric(10, 2))
    slip_url = Column(String(255))
    payment_date = Column(DateTime(timezone=True))

    status = Column(String(50))
    admin_note = Column(String(255))

    order_id = Column(UUID, ForeignKey("order.id"), index=True)

    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    orders = relationship("Order", back_populates="order_payment")
