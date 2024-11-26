from typing import Optional

from pydantic import BaseModel


class ItemPayload(BaseModel):
    item_id: Optional[int]
    item_name: str
    quantity: int
    plate: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class Plate(BaseModel):
    plate: str