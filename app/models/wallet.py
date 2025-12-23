from sqlalchemy import Integer,String,DateTime,ForeignKey,Column,DECIMAL,Boolean,Numeric
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime

class Wallet(Base):
    __tablename__="wallets"
    id=Column(Integer,primary_key=True,nullable=False)
    balance=Column(Numeric(12,2),nullable=False)
    is_active=Column(Boolean,default=True,nullable=False)
    created_at=Column(DateTime,nullable=False,default=datetime.utcnow)
    updated_at=Column(DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)
    user_id=Column(Integer,ForeignKey("users.id"),unique=True)
    user=relationship("User",back_populates="wallet")
    send_transactions=relationship("Transaction",foreign_keys="Transaction.sender_id",back_populates="sender_wallet")
    received_transactions=relationship("Transaction",foreign_keys="Transaction.receiver_id",back_populates="receiver_wallet")
