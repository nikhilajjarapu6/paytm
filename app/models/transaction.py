from sqlalchemy import Column,Integer,String,DateTime,Enum,ForeignKey,Numeric
from sqlalchemy.orm import relationship
from app.database.database import Base
from datetime import datetime
import enum

class PaymentMethod(str, enum.Enum):
    UPI = "UPI"
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"
class TransactionStatus(str, enum.Enum):
    INITIATED = "INITIATED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    REVERSED = "REVERSED"


class Transaction(Base):
    __tablename__="transactions"
    id=Column(Integer,primary_key=True,index=True)
    txn_id = Column(String(20), unique=True, nullable=False, index=True)
    sender_id=Column(Integer,ForeignKey("wallets.id"))
    receiver_id=Column(Integer,ForeignKey("wallets.id"))
    amount=Column(Numeric(10,2),nullable=False)
    description=Column(String(255),nullable=True)
    created_at=Column(DateTime,nullable=False,default=datetime.utcnow)
    payment_method=Column(Enum(PaymentMethod),nullable=False)
    transaction_status=Column(Enum(TransactionStatus),nullable=False)
    payment_time=Column(DateTime,onupdate=datetime.utcnow)
    sender_wallet=relationship("Wallet",foreign_keys=[sender_id],back_populates="send_transactions")
    receiver_wallet=relationship("Wallet",foreign_keys=[receiver_id],back_populates="received_transactions")


