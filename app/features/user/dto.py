from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class UserGetDto(BaseModel):
    id: UUID = Field(
        description="User ID", 
        default="3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
    
    username: str = Field(
        description="Username User", 
        default="Admin01"
    )
    
    f_name: str = Field(
        description="First Name", 
        default="Phakkharaphong"
    )
    
    l_name: str = Field(
        description="Last Name",
        default="Charoenphon"
    )
    
    phone: str | None = Field(
        description="Phone Number",
        default="0876197982"
    )
    
    img_profile: str | None = Field(
        description="Profile Image Path", 
        default="QgIBYWLvHfSJNZTVj8gC29zxv91lb8jKKP8pjirq7yVMg81Isa"
    )
    
    address: str | None = Field(
        description="Address", 
        default="test address"
    )
    
    is_admin: bool | None = Field(
        description="Is Admin User", 
        default=True
    )
    
    is_active: bool | None = Field(
        description="Is Active User", 
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
    
class UserCreateDto(BaseModel):
    username: str = Field(
        description="Username User", 
        default="Admin01"
    )
    
    password: str = Field(
        description="Password", 
        default="test"
    )
    
    f_name: str = Field(
        description="First Name", 
        default="Phakkharaphong"
    )
    
    l_name: str = Field(
        description="Last Name", 
        default="Charoenphon"
    )
    
    phone: str | None = Field(
        description="Phone Number", 
        default="0876197982"
    )
    
    img_profile: str | None = Field(
        description="Profile",
    )
    
    address: str | None = Field(
        description="Address",
    )
    
    is_admin: bool | None = Field(
        description="Is Admin User", 
        default=True
    )
    
    is_active: bool | None = Field(
        description="Is Active User", 
        default=True
    )
    
    model_config = {
        "from_attributes": True
    }

class UserUpdateDto(BaseModel):    
    f_name: str | None = Field(
        description="First Name", 
        default="Phakkharaphong"
    )
    
    l_name: str | None = Field(
        description="Last Name", 
        default="Charoenphon"
    )
    
    phone: str | None = Field(
        description="Phone Number", 
        default="0876197982"
    )
    
    img_profile: str | None = Field(
        description="Profile",
        default="QgIBYWLvHfSJNZTVj8gC29zxv91lb8jKKP8pjirq7yVMg81Isa",
    )
    
    address: str | None = Field(
        description="Address",
        default="Room 101, 1st Floor, ABC Building, 123 Moo 4, Sukhumvit Road, Bangna, Bangkok 10260",
    )
    
    is_admin: bool | None = Field(
        description="Is Admin User", 
        default=True
    )
    
    is_active: bool | None = Field(
        description="Is Active User", 
        default=True
    )
    
    model_config = {
        "from_attributes": True
    }
