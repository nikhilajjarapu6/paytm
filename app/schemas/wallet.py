from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import List
from app.schemas.transaction import TransactionResponse



class WalletResponse(BaseModel):
    id: int
    balance: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config={
        "from_attributes":True
    }