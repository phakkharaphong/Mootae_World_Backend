from uuid import UUID
from pydantic import BaseModel, Field


class WallpaperCollectionGetDto(BaseModel):
    id: UUID = Field(
        description="Wallpaper Collection ID",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )

    name: str = Field(
        description="Wallpaper Collection Name",
        examples=["Nature Wallpapers"],
    )


class WallpaperCollectionCreateDto(BaseModel):
    name: str = Field(
        description="Wallpaper Collection Name",
        examples=["Nature Wallpapers"],
    )


class WallpaperCollectionUpdateDto(BaseModel):
    name: str | None = Field(
        description="Wallpaper Collection Name",
        examples=["Nature Wallpapers"],
    )
