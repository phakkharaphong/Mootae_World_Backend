from datetime import datetime, timezone
from pydantic import BaseModel, Field
from uuid import UUID


class BlogGetDto(BaseModel):
    id: UUID  = Field(
        description="article blog id", 
        default="EXasfew565d2"
    )

    title: str | None = Field(
        description="title article", 
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )

    cover_img: str | None = Field(
        description="cover img", 
        default="path/test/img.png"
    )

    content: str | None = Field(
        description="content", 
        default="test\ntest\ntest\n"
    )

    view: int | None = Field(
        description="view", 
        default=10
    )

    like: int | None = Field(
        description="like", 
        default=10
    )

    category_id: UUID = Field(
        description="blog category id",
        default="ynuJ2S1LDMNd4VVYLpIM0GZbMzlZz2A4fFH3gyxennX1Y0pR5e",
    )

    is_active: bool | None = Field(
        description="Is Active Blog", 
        default=True
    )

    created_at: datetime = Field(
        description="Created time", 
       default_factory=lambda: datetime.now(timezone.utc)
    )

    created_by: str | None = Field(
        description="Created by User", 
        default="System"
    )

    updated_at: datetime | None = Field(
        description="Updated time", 
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_by: str | None = Field(
        description="Updated by User", 
        default="System"
    )

    model_config = {
        "from_attributes": True
    }


class BlogCreateDto(BaseModel):
    title: str | None = Field(
        description="title article", 
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )

    cover_img: str | None = Field(
        description="cover img", 
        default="path/test/img.png"
    )

    content: str | None = Field(
        description="content", 
        default="test\ntest\ntest\n"
    )

    category_id: str | None = Field(
        description="blog category id",
        default="ynuJ2S1LDMNd4VVYLpIM0GZbMzlZz2A4fFH3gyxennX1Y0pR5e",
    )

    created_by: str | None = Field(
        description="created By",
        default="System"
    )

    is_active: bool | None = Field(
        description="Is Active Blog", 
        default=True
    )


    model_config = {"from_attributes": True}


class BlogUpdateDto(BaseModel):
    title: str | None = Field(
        description="title article", 
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )

    cover_img: str | None = Field(
        description="cover img", 
        default="path/test/img.png"
    )

    content: str | None = Field(
        description="content", 
        default="test\ntest\ntest\n"
    )

    category_id: str | None = Field(
        description="blog category id",
        default="ynuJ2S1LDMNd4VVYLpIM0GZbMzlZz2A4fFH3gyxennX1Y0pR5e",
    )

    updated_by: str | None = Field(
        description="created By",
        default="System"
    )

    is_active: bool | None = Field(
        description="Is Active Blog", 
        default=True
    )

    model_config = {"from_attributes": True}
