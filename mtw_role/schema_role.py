from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class mtw_role(BaseModel):
    id: str = Field(
        description="role id",
        default="EXasfew565d2"
    )
    role_name: str |None = Field(
        description="role name",
        default="Admin"
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
       "from_attributes": True   # ✅ Pydantic v2
    }

class create_mtw_role(BaseModel):
    role_name: str |None = Field(
        description="role name",
        default="Admin"
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
    # updated_at: datetime = Field(
    #     description="Created time",
    #     default_factory=datetime.utcnow   
    # )
    # updated_by: str = Field(
    #     description="updated by",
    #     default="Admin"    
    # )
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
class RoleResponse(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[mtw_role]