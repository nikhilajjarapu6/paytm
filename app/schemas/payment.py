from pydantic import BaseModel
from decimal import Decimal
from app.models.transaction import PaymentMethod,TransactionStatus
from datetime import datetime

class PaymentRequest(BaseModel):
    sender_id:int
    receiver_id: int
    amount: Decimal
    payment_method: PaymentMethod
    description: str | None = None

class PaymentResponse(BaseModel):
    txn_id:str
    amount:Decimal
    payment_time:datetime
    payment_method:PaymentMethod
    transaction_status:TransactionStatus
    description:str|None=None

    model_config={
        "from_attributes":True
    }