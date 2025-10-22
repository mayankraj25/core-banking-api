from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class CardType(enum.Enum):
    DEBIT="debit"
    CREDIT="credit"

class CardStatus(enum.Enum):
    ACTIVE="active"
    BLOCKED="blocked"
    EXPIRED="expired"

class Card(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    card_number = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    card_type = Column(Enum(CardType), nullable=False)
    cvv = Column(String, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cards")
    account = relationship("Account")