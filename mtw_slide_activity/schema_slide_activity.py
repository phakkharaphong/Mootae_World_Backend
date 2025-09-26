from datetime import datetime
from pydantic import BaseModel, Field


class mtw_slide_activity(BaseModel):
    id: str = Field(
        description="id",
        default="EXasfew565d2"
    )
    title: str |None = Field(
        description="title",
        default="งานสัมนา"
    )

    img_file_name: str |None = Field(
        description="img_file_name",
        default="test.png"
    )

    img_path: str | None = Field(
        description="img_file_name",
        default="img/test.png"
    ) 

    like: int| None = Field(
        description="like",
        default= 0
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

class create_slide_activity(BaseModel):
    # id: str = Field(
    #     description="id",
    #     default="EXasfew565d2"
    # )
    title: str |None = Field(
        description="title",
        default="งานสัมนา"
    )

    img_file_name: str |None = Field(
        description="img_file_name",
        default="test.png"
    )

    img_path: str | None = Field(
        description="img_file_name",
        default="img/test.png"
    ) 

    like: int| None = Field(
        description="like",
        default= 0
  
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
    # updated_at: datetime | None = None
    # updated_by: str | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }

class update_slide_activity(BaseModel):
    # id: str = Field(
    #     description="id",
    #     default="EXasfew565d2"
    # )
    title: str |None = Field(
        description="title",
        default="งานสัมนา"
    )

    img_file_name: str |None = Field(
        description="img_file_name",
        default="test.png"
    )

    img_path: str | None = Field(
        description="img_file_name",
        default="img/test.png"
    ) 

    like: int| None = Field(
        description="like",
        default= 0
  
  )
    is_active: bool | None = None
    updated_at: datetime = Field(
        description="updated time",
        default_factory=datetime.now() 
    )
    updated_by: str = Field(
        description="updated by",
        default="Admin"   
    )
    # updated_at: datetime | None = None
    # updated_by: str | None = None
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }