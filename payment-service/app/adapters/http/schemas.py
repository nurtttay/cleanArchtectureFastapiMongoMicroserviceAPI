from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentIn(BaseModel):
    tournament_id: str
    amount: float = Field(..., gt=0)
    payment_method: str = "card"
    card_number: Optional[str] = None

class PaymentOut(BaseModel):
    id: str
    user_id: str
    tournament_id: str
    amount: float
    transaction_type: str
    status: str
    payment_method: Optional[str]
    transaction_id: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
