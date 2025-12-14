from typing import List
from pydantic import BaseModel, Field
from datetime import datetime


class UserGetDto(BaseModel):
    id: str | None = Field(
        description="UID User", 
        default="EXasfew565d2"
    )
    
    username: str | None = Field(
        description="Username User", 
        default="Admin01"
    )
    
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
        description="Profile Image Path", 
        default="QgIBYWLvHfSJNZTVj8gC29zxv91lb8jKKP8pjirq7yVMg81Isa"
    )
    
    address: str | None = Field(
        description="Address", 
        default="test address"
    )
    
    following: int | None = Field(
        description="Number of Following"
    )
    
    keep_following: int | None = Field(
        description="Number of Keep Following"
    )
    
    role_id: str | None = Field(
        description="Role ID",
        default="EXasfew565d2"
    )
    
    is_active: bool | None = None
    
    model_config = {
        "from_attributes": True
    }
    
class UserCreateDto(BaseModel):
    username: str | None = Field(
        description="Username User", 
        default="Admin01"
    )
    
    password: str | None = Field(
        description="Password", 
        default="test"
    )
    
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
    )
    
    address: str | None = Field(
        description="Address",
    )
    
    following: int | None = Field(
        description="following"
    )
    
    keep_following: int | None = Field(
        description="keep_following"
    )
    
    role_id: str = Field(
        description="Role ID", 
        default="EXasfew565d2"
    )
    
    is_active: bool | None = None
    
    created_at: datetime = Field(
        description="Created time", 
        default_factory=datetime.now
    )
    
    model_config = {
        "from_attributes": True
    }

class UserUpdateDto(BaseModel):
    username: str | None = Field(
        description="Username User", 
        default="Admin01"
    )
    
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
    )
    
    address: str | None = Field(
        description="Address",
    )
    
    following: int | None = Field(
        description="following"
    )
    
    keep_following: int | None = Field(
        description="keep_following"
    )
    
    role_id: str = Field(
        description="Role ID", 
        default="EXasfew565d2"
    )
    
    is_active: bool | None = None
    
    updated_at: datetime = Field(
        description="Updated time", 
        default_factory=datetime.now
    )
    
    model_config = {
        "from_attributes": True
    }
    
class TokenDto(BaseModel):
    access_token: str = Field(
        description="Access Token"
    )
    
    token_type: str = Field(
        description="Token Type",
        default="bearer"
    )

class AccessTokenDto(BaseModel):
    access_token: str = Field(
        description="Access Token"
    )
    
class LoginDto(BaseModel):
    username: str = Field(
        description="Username User", 
        default="Admin01"
    )
    
    password: str = Field(
        description="Password", 
        default="test"
    )

class UserResponse(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[UserGetDto]