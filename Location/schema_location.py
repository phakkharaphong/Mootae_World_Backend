from typing import List
from pydantic import BaseModel, Field

class province(BaseModel):
    ProvinceId: int
    ProvinceNameTH: str
    ProvinceNameEN: str
    ZoneId: int

    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
class zone(BaseModel):
    ZoneId: int
    ZoneNameTH: str
    ZoneNameEN:str
    model_config = {
       "from_attributes": True   # ✅ Pydantic v2
    }
class ZoneResponse(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[zone]
class ProvinceResponse(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[province]