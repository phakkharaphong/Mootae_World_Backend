from uuid import UUID
from pydantic import BaseModel, Field


class ExternalBiDto(BaseModel): 
    email: str | None = Field(
        description="email",
        examples=["aSefdCrwweDAe"]
    )
    total: int | None = Field(
        description="Total Cal For Type", 
        examples=[0]
    )

class BiOrderTypeItem(BaseModel):
    order_type_id: UUID
    order_type_name: str
    total: int

class BiOrderStatusDto(BaseModel):
    status: str
    total: int