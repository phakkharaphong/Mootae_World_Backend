from uuid import UUID
from pydantic import BaseModel, Field


class WallpaperGetDto(BaseModel):
    id: UUID = Field(
        description="Wallpaper ID",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
    )

    url: str = Field(
        description="Wallpaper URL",
        examples=["https://example.com/wallpaper1.jpg"],
    )
    original: str | None = Field(
        description="original file",
        examples=["https://example.com/wallpaper1.jpg"]
    )

    wallpaper_collection_id: UUID | None = Field(
        description="Wallpaper Collection ID",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        default=None,
    )


class WallpaperCreateDto(BaseModel):
    url: str = Field(
        description="Wallpaper URL",
        examples=["https://example.com/wallpaper1.jpg"],
    )

    wallpaper_collection_id: UUID | None = Field(
        description="Wallpaper Collection ID",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        default=None,
    )
    original: str | None = Field(
        description="original file",
        examples=["https://example.com/wallpaper1.jpg"]
    )


class WallpaperUpdateDto(BaseModel):
    url: str | None = Field(
        description="Wallpaper URL",
        examples=["https://example.com/wallpaper1.jpg"],
        default=None,
    )

    wallpaper_collection_id: UUID | None = Field(
        description="Wallpaper Collection ID",
        examples=["3fa85f64-5717-4562-b3fc-2c963f66afa6"],
        default=None,
    )
