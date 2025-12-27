import uuid
from sqlalchemy import UUID, Column, ForeignKey, String
from app.core.database import Base


class Wallpaper(Base):
    __tablename__ = "wallpaper"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    url = Column(String(100), index=True, unique=True, nullable=False)

    wallpaper_collection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("wallpaper_collection.id"),
        nullable=True,
        index=True,
    )
