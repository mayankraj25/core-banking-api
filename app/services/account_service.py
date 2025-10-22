from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from decimal import Decimal
import uuid
from ..models.account import Account, AccountType, AccountStatus
from ..models.user import User
from ..schemas.account import AccountCreate, AccountUpdate

class AccountService:
    def __init__(self,db=Session):
        self.db=db
    
    def create_account(self, user_id: int,account_data: AccountCreate)-> Account:
        account_number = f"ACC{uuid.uuid4().hex[:10].upper()}"
        new_account=Account(
            account_number=account_number,
            user_id=user_id,
            account_type=account_data.account_type,
            currency=account_data.currency,
            balance=Decimal("0.00")
        )
        self.db.add(new_account)
        self.db.commit()
        self.db.refresh(new_account)
        return new_account
    
    def get_user_accounts(self,user_id: int)-> List[Account]:
        return self.db.query(Account).filter(and_(Account.user_id==user_id,Account.status==AccountStatus.ACTIVE)).all()
    
    def get_account_by_id(self, account_id: int, user_id: int) -> Optional[Account]:
        return self.db.query(Account).filter(and_(Account.id==account_id,Account.user_id==user_id)).first()
    
    def update_balance(self, account_id: int, amount: Decimal)-> bool:
        account=self.db.query(Account).filter(Account.id==account_id).first()
        if account:
            account.balance += amount
            self.db.commit()
            return True
        return False