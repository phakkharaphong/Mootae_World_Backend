from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
class UserSchema(BaseModel):
    id: str = Field(
        description="UID User",
        default="EXasfew565d2"
    )
    username: str |None = Field(
        description="Username User",
        default="Admin01"
    )
    f_name: str |None  = Field(
        description="Frist Name",
        default="Phakkharaphong"
    )
    l_name: str |None  = Field(
        description="Last Name",
        default="Charoenphon"
    )
    phone:str |None = Field(
        description="number phone",
        default="0876197982"
    )
    img_profile:str |None = Field(
        description="Profile",
        default="QgIBYWLvHfSJNZTVj8gC29zxv91lb8jKKP8pjirq7yVMg81Isa"
    )
    address:str |None = Field(
        description="address",
        default="test address"
    )
    following:int |None = Field(
        description="following"
    )
    keep_following:int |None = Field(
        description="keep_following"
    )
    role_id: str = Field(
        description="role User",
        default="EXasfew565d2"
    ) 
    is_active: bool | None = None

    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
    
class UserCreate(BaseModel):
    username: str |None = Field(
        description="Username User",
        default="Admin01"
    )
    password: str | None = Field(
        description="Username User",
        default="test"
    )
    f_name: str |None  = Field(
        description="Frist Name",
        default="Phakkharaphong"
    )
    l_name: str |None  = Field(
        description="Last Name",
        default="Charoenphon"
    )
    phone:str |None = Field(
        description="number phone"
    )
    img_profile:str |None = Field(
        description="Profile"
    )
    address:str |None = Field(
        description="address"
    )
    following:int |None = Field(
        description="following"
    )
    keep_following:int |None = Field(
        description="keep_following"
    )
    role_id: str = Field(
        description="role User",
        default="EXasfew565d2"
    ) 
    is_active: bool | None = None
    created_at: datetime = Field(
        description="Created time",
        default_factory=datetime.utcnow   # ✅ ใช้ UTC
    )

    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class UserSchemaModel(BaseModel):
    id: str
    username: str
    f_name: str 
    l_name: str 
    phone:str 
    img_profile:str 
    address:str 
    following:int
    keep_following:int 
    role_id: str
    is_active: bool

    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
class UsersResponse(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[UserSchemaModel]