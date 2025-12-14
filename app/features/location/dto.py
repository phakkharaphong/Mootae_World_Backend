from pydantic import BaseModel
from typing import List


class ZoneGetDto(BaseModel):
    ZoneId: int
    ZoneNameTH: str
    ZoneNameEN: str

    model_config = {"from_attributes": True}


class ProvinceGetDto(BaseModel):
    ProvinceId: int
    ProvinceNameTH: str
    ProvinceNameEN: str
    ZoneId: int

    model_config = {"from_attributes": True}


class ZoneResponseDto(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[ZoneGetDto]


class ProvinceResponseDto(BaseModel):
    page: int
    limit: int
    total: int
    message: str
    Data: List[ProvinceGetDto]
