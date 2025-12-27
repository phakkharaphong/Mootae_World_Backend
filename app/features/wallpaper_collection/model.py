import uuid
from sqlalchemy import UUID, Column, String
from app.core.database import Base


class WallpaperCollection(Base):
    __tablename__ = "wallpaper_collection"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(100), unique=True, index=True, nullable=False)
