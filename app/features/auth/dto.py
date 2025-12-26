from pydantic import BaseModel, Field


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
