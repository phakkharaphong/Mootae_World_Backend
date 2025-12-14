from datetime import datetime
from pydantic import BaseModel, Field


class RoleGetDto(BaseModel):
    id: str = Field(
        description="role id", 
        default="EXasfew565d2"
    )
    
    role_name: str | None = Field(
        description="role name", 
        default="Admin"
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


class RoleCreateDto(BaseModel):
    role_name: str | None = Field(
        description="role name", 
        default="Admin"
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

class RoleUpdateDto(BaseModel):
    role_name: str | None = Field(
        description="role name", 
        default="Admin"
    )
    
    is_active: bool | None = None
    
    updated_at: datetime = Field(
        description="updated time", 
        default_factory=datetime.now
    )
    
    updated_by: str = Field(
        description="updated by", 
        default="Admin"
    )

    model_config = {
        "from_attributes": True
    }