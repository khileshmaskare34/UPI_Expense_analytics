from pydantic import BaseModel
from typing import Optional


class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    category_id: Optional[int]
    user_id: int

    class Config:
        orm_mode = True
    

class TransactionUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    