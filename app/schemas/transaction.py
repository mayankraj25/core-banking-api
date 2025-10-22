from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal 
from ..models.transaction import TransactionType, TransactionStatus

class TransactionBase(BaseModel):
    amount: Decimal
    currency: Optional[str]="USD"
    description: Optional[str]=None

class TransactionCreate(TransactionBase):
    from_account_id: Optional[int]=None
    to_account_id: Optional[int]=None
    transaction_type: TransactionType

class TransactionInDB(TransactionBase):
    id: int
    transaction_id: str
    from_account_id: Optional[int]
    to_account_id: Optional[int]
    transaction_type: TransactionType
    status: TransactionStatus
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class TransactionResponse(TransactionInDB):
    pass