from datetime import datetime
from pydantic import BaseModel, Field


class mtw_article_blog(BaseModel):
    id: str | None = Field(
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
    conten: str | None = Field(
        description="conten",
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
    article_categories_id: str | None = Field(
        description="article_categories_id",
        default="ynuJ2S1LDMNd4VVYLpIM0GZbMzlZz2A4fFH3gyxennX1Y0pR5e"
    )
    is_active: bool | None = None
    created_at: datetime = Field(
        description="Created time",
        default_factory=datetime.now() 
    )
    created_by: str = Field(
        description="created by",
        default="Admin"   
    )
    updated_at: datetime | None = None
    updated_by: str | None = None
    model_config = {
        "from_attributes": True
        }

class create_mtw_article_blog(BaseModel):
    # id: str | None = Field(
    #     description="article blog id",
    #     default="EXasfew565d2"
    # )
    title: str | None = Field(
        description="title article",
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )
    cover_img: str | None = Field(
        description="cover img",
        default="path/test/img.png"
    )
    conten: str | None = Field(
        description="conten",
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
    article_categories_id: str | None = Field(
        description="article_categories_id",
        default="ynuJ2S1LDMNd4VVYLpIM0GZbMzlZz2A4fFH3gyxennX1Y0pR5e"
    )
    is_active: bool | None = None
    created_at: datetime = Field(
        description="Created time",
        default_factory=datetime.now() 
    )
    created_by: str | None = Field(
        description="created by",
        default="Admin"   
    )
    model_config = {
        "from_attributes": True
        }

class update_mtw_article_blog(BaseModel):

    title: str | None = Field(
        description="title article",
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )
    cover_img: str | None = Field(
        description="cover img",
        default="path/test/img.png"
    )
    conten: str | None = Field(
        description="conten",
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
    article_categories_id: str | None = Field(
        description="article_categories_id",
        default="ynuJ2S1LDMNd4VVYLpIM0GZbMzlZz2A4fFH3gyxennX1Y0pR5e"
    )
    is_active: bool | None = None
    updated_at: datetime = Field(
        description="updated time",
        default_factory=datetime.now() 
    )
    updated_by: str = Field(
        description="updated by",
        default="Admin"   
    )
    model_config = {
        "from_attributes": True
        }