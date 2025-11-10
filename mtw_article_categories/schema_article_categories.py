from datetime import datetime
from pydantic import BaseModel, Field


class mtw_article_categories(BaseModel):
    id: str | None = Field(
        description="role id",
        default="EXasfew565d2"
    )
    name: str | None = Field(
        description="Title Slide New",
        default="สายมู"
    )
    is_active: bool | None = None
    created_at: datetime = Field(
        description="Created time",
        default_factory=datetime.now() 
    )
    created_by: str| None = Field(
        description="created by",
        default="Admin"   
    )
    updated_at: datetime | None = None
    updated_by: str | None = None
    model_config = {"from_attributes": True}


class mtw_article_categories_ref(BaseModel):
    id: str | None = Field(
        description="role id",
        default="EXasfew565d2"
    )
    name: str | None = Field(
        description="Title Slide New",
        default="สายมู"
    )
    is_active: bool | None = None
    model_config = {"from_attributes": True}

class create_mtw_article_categories(BaseModel):
    # id: str | None = Field(
    #     description="role id",
    #     default="EXasfew565d2"
    # )
    name: str | None = Field(
        description="Title Slide New",
        default="สายมู"
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
    model_config = {"from_attributes": True}

class update_mtw_article_categories(BaseModel):
    # id: str | None = Field(
    #     description="role id",
    #     default="EXasfew565d2"
    # )
    name: str | None = Field(
        description="Title Slide New",
        default="สายมู"
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
    model_config = {"from_attributes": True}