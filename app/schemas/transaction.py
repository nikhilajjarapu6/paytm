from pydantic import BaseModel
from decimal import Decimal
from app.models.transaction import PaymentMethod,TransactionStatus
from datetime import datetime

class TransactionRequest(BaseModel):
    sender_id: int | None
    receiver_id: int | None
    amount: Decimal
    payment_method: PaymentMethod
    description: str | None

class TransactionResponse(BaseModel):
    txn_id: str|None
    sender_id: int | None
    receiver_id: int | None
    amount: Decimal
    payment_method: PaymentMethod
    transaction_status: TransactionStatus
    created_at: datetime
    description: str | None

    model_config = {"from_attributes": True}