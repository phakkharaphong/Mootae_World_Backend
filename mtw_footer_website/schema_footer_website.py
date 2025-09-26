from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class mtw_footer_website(BaseModel):
    id: str | None = Field(
        description="role id",
        default="EXasfew565d2"
    )
    title: Optional[str] | None = Field(
        description="title icon",
        default="วอลเปเปอร์เสริมดวง"
    )
    icon_img: Optional[str] | None = Field(
        description="icon img",
        default="img/test.png"
    )
    link_ref: Optional[str] | None = Field(
        description="link ref",
        default="www.example.com"
    )
    is_active: bool | None = None
    created_at: datetime| None = Field(
        description="Created time",
        default_factory=datetime.now() 
    )
    created_by: Optional[str] | None= Field(
        description="created by",
        default="Admin"   
    )
    updated_at: datetime | None = None
    updated_by: Optional[str] | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }


class create_footer_website(BaseModel):
    # id: str | None = Field(
    #     description="role id",
    #     default="EXasfew565d2"
    # )
    title: Optional[str] | None = Field(
        description="title icon",
        default="วอลเปเปอร์เสริมดวง"
    )
    icon_img: Optional[str] | None = Field(
        description="icon img",
        default="img/test.png"
    )
    link_ref: Optional[str] | None = Field(
        description="link ref",
        default="www.example.com"
    )
    is_active: bool | None = None
    created_at: datetime| None = Field(
        description="Created time",
        default_factory=datetime.now() 
    )
    created_by: Optional[str] | None= Field(
        description="created by",
        default="Admin"   
    )
    # updated_at: datetime | None = None
    # updated_by: Optional[str] | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class update_footer_website(BaseModel):
    # id: str | None = Field(
    #     description="role id",
    #     default="EXasfew565d2"
    # )
    title: Optional[str] | None = Field(
        description="title icon",
        default="วอลเปเปอร์เสริมดวง"
    )
    icon_img: Optional[str] | None = Field(
        description="icon img",
        default="img/test.png"
    )
    link_ref: Optional[str] | None = Field(
        description="link ref",
        default="www.example.com"
    )
    is_active: bool | None = None
    updated_at: datetime| None = Field(
        description="updated time",
        default_factory=datetime.now() 
    )
    updated_by: Optional[str] | None= Field(
        description="updated by",
        default="Admin"   
    )
    # updated_at: datetime | None = None
    # updated_by: Optional[str] | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
