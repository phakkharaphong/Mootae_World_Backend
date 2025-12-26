from datetime import datetime, timezone
from pydantic import BaseModel, Field
from uuid import UUID

class BlogHomePageGetDto(BaseModel):
    id: UUID | None = Field(
        description="blog home page", 
        default="EXasfew565d2"
    )
    
    title: str | None = Field(
        description="blog title", 
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )
    
    note: str | None = Field(
        description="blog note", 
        default="ดูดวงวันนี้"
    )
    
    img_path: str | None = Field(
        description="blog img path", 
        default="img/test/filename.png"
    )
    
    link: str | None = Field(
        description="blog link", 
        default="img/test/filename.png"
    )
    
    is_active: bool | None = Field(
        description="Is Active Category", 
        default=True
    )
    
    created_at: datetime | None = Field(
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


class BlogHomePageCreateDto(BaseModel):
    title: str | None = Field(
        description="blog title", 
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )
    
    note: str | None = Field(
        description="blog note", 
        default="ดูดวงวันนี้"
    )
    
    img_path: str | None = Field(
        description="blog img path", 
        default="img/test/filename.png"
    )
    
    link: str | None = Field(
        description="blog link", 
        default="img/test/filename.png"
    )
    
    is_active: bool | None = None

    model_config = {
        "from_attributes": True
    }


class BlogHomePageUpdateDto(BaseModel):
    title: str | None = Field(
        description="blog title", 
        default="ดวงคุณเป็นอย่างไรบ้างวันนี้"
    )
    
    note: str | None = Field(
        description="blog note", 
        default="ดูดวงวันนี้"
    )
    
    img_path: str | None = Field(
        description="blog img path", 
        default="img/test/filename.png"
    )
    
    link: str | None = Field(
        description="blog link", 
        default="img/test/filename.png"
    )
    
    is_active: bool | None = None
    
    model_config = {
        "from_attributes": True
    }