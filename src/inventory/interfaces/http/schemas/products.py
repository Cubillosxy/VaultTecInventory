from dataclasses import asdict
from typing import Optional
from pydantic import BaseModel, Field
from inventory.domain.entities import Product

class ProductIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field("", max_length=2000)
    price: float = Field(ge=0)
    quantity: int = Field(ge=0)

class ProductUpdateIn(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[float] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)

class ProductOut(BaseModel):
    id: str
    name: str
    description: str
    price: float
    quantity: int

    @classmethod
    def from_entity(cls, p: Product) -> "ProductOut":
        return cls(**asdict(p))
