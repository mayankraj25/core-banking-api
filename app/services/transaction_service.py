from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from decimal import Decimal
import uuid
from datetime import datetime
from ..models.transaction import Transaction, TransactionType, TransactionStatus
from ..models.account import Account
from ..schemas.transaction import TransactionCreate

class TransactionService:
    def __init__(self, db: Session):
        self.db=db

    def create_transaction(self, transaction_data: TransactionCreate, user_id:int) -> Transaction:
        transaction_id = f"TXN{uuid.uuid4().hex[:12].upper()}"
        transaction = Transaction(
            transaction_id=transaction_id,
            from_account_id=transaction_data.from_account_id,
            to_account_id=transaction_data.to_account_id,
            transaction_type=transaction_data.transaction_type,
            amount=transaction_data.amount,
            currency=transaction_data.currency,
            description=transaction_data.description,
            status=TransactionStatus.PENDING
        )

        self.db.add(transaction)

        if transaction_data.transaction_type==TransactionType.DEPOSIT:
            success=self._process_deposit(transaction)
        elif transaction_data.transaction_type==TransactionType.WITHDRAWAL:
            success=self._process_withdrawal(transaction)
        elif transaction_data.transaction_type==TransactionType.TRANSFER:
            success=self._process_transfer(transaction)

        if success:
            transaction.status=TransactionStatus.COMPLETED
            transaction.completed_at=datetime.utcnow()
        else:
            transaction.status=TransactionStatus.FAILED

        self.db.commit()
        self.db.refresh(transaction)
        return transaction
    
    def _process_transfer(self, transaction_data: Transaction, user_id: int) -> bool:
        from_account=self.db.query(Account).filter(and_(Account.id==transaction_data.from_account_id,Account.user_id==user_id)).first()
        to_account=self.db.query(Account).filter(Account.id==transaction_data.to_account_id).first()

        if not from_account or not to_account:
            return False
        if from_account.balance<transaction_data.amount:
            return False
        
        from_account.balance-=transaction_data.amount
        to_account.balance+=transaction_data.amount
        return True
    
    def _process_deposit(self,transaction_data: Transaction, user_id: int) -> bool:
        to_account=self.db.query(Account).filter(and_(Account.id==transaction_data.to_account_id,Account.user_id==user_id)).first()
        if not to_account:
            return False
        to_account.balance+=transaction_data.amount
        return True
    
    def _process_withdrawal(self, transaction_data: Transaction, user_id: int) -> bool:
        from_account=self.db.query(Account).filter(and_(Account.id==transaction_data.from_account_id,Account.user_id==user_id)).first()
        if not from_account:
            return False
        if from_account.balance<transaction_data.amount:
            return False
        from_account.balance-=transaction_data.amount
        return True
    


        