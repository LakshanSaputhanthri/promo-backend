from pydantic import BaseModel
from datetime import date
import uuid


class PromotionOut(BaseModel):
    id: uuid.UUID
    title: str
    merchant: str
    thumb: str | None
    card_type: str
    valid_to: date

    class Config:
        orm_mode = True
