from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..core.database import Base

class AccountType(enum.Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    CREDIT = "credit"

class AccountStatus(enum.Enum):
    ACTIVE = "active"
    FROZEN = "frozen"
    CLOSED = "closed"

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    balance = Column(Numeric(15, 2), default=0.00)
    currency = Column(String, default="USD")
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="accounts")
    transactions_from = relationship("Transaction", foreign_keys="[Transaction.from_account_id]", back_populates="from_account")
    transactions_to = relationship("Transaction", foreign_keys="[Transaction.to_account_id]", back_populates="to_account")