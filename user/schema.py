from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    UserID: int = Field(
        description="UID User",
        default="1"
    )
    UserName: str |None = Field(
        description="Username User",
        default="Admin01"
    )
    FullName: str |None  = Field(
        description="Fullname user Frist Name and Last Name",
        default="Phakkharaphong Charoenphon"
    )
    uid:str |None = Field(
        description="UID User"
    )
    
    Telephone: str | None = None
    MobilePhone: str | None = None
    IsSuperUser: int | None = None
    IsActived: int | None = None

    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
    
class UserCreate(BaseModel):
    UserID: int
    UserName: str | None = Field(
        description="Username User",
        default="admin01"
    )
    Password: str | None = Field(
        description="Password User",
        default="Phak#150845"
    )
    FullName: str | None = Field(
        description="FullName User",
        default="Phakkharaphong Charoenphon"
    )
    Telephone: str | None = Field(
        description="FullName User",
        default="094395615"
    )
    MobilePhone: str | None = Field(
        description="FullName User",
        default="0876197982"
    )
    uid: str = Field(
        description="Nano Uis",
        default="W3KBuvoD"
    )
    IsSuperUser: int 
    IsActived: int

    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }