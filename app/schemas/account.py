from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal
from ..models.account import AccountType, AccountStatus

class AccountBase(BaseModel):
    account_type: AccountType
    currency: Optional[str] = "USD"

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    account_type: Optional[AccountType] = None
    status: Optional[AccountStatus] = None

class AccountInDB(AccountBase):
    id: int
    account_number: str
    balance: Decimal
    status: AccountStatus
    created_at: datetime

    class Config:
        from_attributes = True

class AccountResponse(AccountInDB):
    pass
