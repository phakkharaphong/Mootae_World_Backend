from datetime import datetime
from pydantic import BaseModel, Field


class BlogHomePageGetDto(BaseModel):
    id: str | None = Field(
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
    
    is_active: bool | None = None
    
    created_at: datetime = Field(
        description="Created time", 
        default_factory=datetime.now
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
    
    created_at: datetime = Field(
        description="Created time", 
        default_factory=datetime.now
    )
    
    created_by: str = Field(
        description="created by", 
        default="Admin"
    )

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
    
    updated_at: datetime = Field(
        description="update time", 
        default_factory=datetime.now
    )
    
    updated_by: str = Field(
        description="update by", 
        default="Admin"
    )

    model_config = {
        "from_attributes": True
    }