from sqlalchemy import Boolean, Column, DateTime, String
from app.core.database import Base


class FooterWebsite(Base):
    __tablename__ = "footer_website"

    id = Column(String(50), primary_key=True, index=True)

    title = Column(String(150), index=True)
    icon_img = Column(String(100))
    link_ref = Column(String(100))

    is_active = Column(Boolean, index=True)

    created_at = Column(DateTime)
    created_by = Column(String(50), index=True)
    updated_at = Column(DateTime)
    updated_by = Column(String(50), index=True)
