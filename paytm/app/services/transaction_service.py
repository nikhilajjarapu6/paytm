from sqlalchemy.orm import Session
from typing import Optional,List
from app.schemas.transaction import TransactionResponse,PaymentMethod,TransactionStatus,TransactionRequest
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.repo.transaction_repo import TransactionRepo
from app.services.wallet_service import WalletService
from decimal import Decimal

class TransactionService:
    def __init__(self,db:Session):
        self.repo=TransactionRepo(db)

    def create_initiated(self,sender_wallet_id: int,receiver_wallet_id: int,amount: Decimal,payment_method: PaymentMethod,description: str | None) -> Transaction:
     txn=Transaction(
        sender_wallet_id=sender_wallet_id,
        receiver_wallet_id=receiver_wallet_id,
        amount=amount,
        payment_method=payment_method,
        description=description,
        transaction_status=TransactionStatus.INITIATED
     )
     return self.repo.create(txn)
    
    def mark_success(self,txn:Transaction)->Transaction:
       txn.transaction_status=TransactionStatus.SUCCESS
       return self.repo.save(txn)
    
    def mark_fail(self,txn:Transaction)->Transaction:
        txn.transaction_status=TransactionStatus.FAILED
        return self.repo.save(txn)
    
    def mark_pending(self,txn:Transaction)->Transaction:
        txn.transaction_status=TransactionStatus.PENDING
        return self.repo.save(txn)
    
    def mark_reversed(self,txn:Transaction)->Transaction:
        txn.transaction_status=TransactionStatus.REVERSED
        return self.repo.save(txn)
    
    def find_by_txn_id(self,txt_id:int)->Optional[Transaction]:
       return self.repo.find_by_txn_id(txt_id)
    
    def find_by_wallet(self,id:int)->List[Transaction]:
       return self.repo.find_by_wallet(id)
    
    def find_by_status(self,status:TransactionStatus)->Optional[Transaction]:
       return self.repo.find_by_status(status)