from sqlalchemy.orm import Session
from typing import Optional,List
from app.schemas.transaction import TransactionResponse,PaymentMethod,TransactionStatus,TransactionRequest
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.repo.transaction_repo import TransactionRepo
from app.services.wallet_service import WalletService
from decimal import Decimal
from app.exceptions.payment_exceptions import TxnNotFoundException
from app.exceptions.wallet_exceptions import WalletNotFoundException

class TransactionService:
    def __init__(self,db:Session):
        self.repo=TransactionRepo(db)

    def create_initiated(self,txn_id:str,sender_id: int,receiver_id: int,amount: Decimal,payment_method: PaymentMethod,description: str | None) -> Transaction:
     txn=Transaction(
        txn_id=txn_id,
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        payment_method=payment_method,
        description=description,
        transaction_status=TransactionStatus.INITIATED
     )
     return self.repo.add(txn)
    
    def mark_success(self,txn:Transaction)->Transaction:
       txn.transaction_status=TransactionStatus.SUCCESS
       return self.repo.add(txn)
    
    def mark_fail(self,txn:Transaction)->Transaction:
        txn.transaction_status=TransactionStatus.FAILED
        return self.repo.add(txn)
    
    def mark_pending(self,txn:Transaction)->Transaction:
        txn.transaction_status=TransactionStatus.PENDING
        return self.repo.add(txn)
    
    def mark_reversed(self,txn:Transaction)->Transaction:
        txn.transaction_status=TransactionStatus.REVERSED
        return self.repo.add(txn)
    
    def find_by_txn_id(self,txt_id:str)->Optional[Transaction]:
       transaction=self.repo.find_by_txn_id(txt_id)
       if not transaction :
          raise TxnNotFoundException(id)
       return transaction
    
    def find_by_wallet(self,id:int)->List[Transaction]:
       wallet=self.repo.find_by_wallet(id)
       if not wallet:
          raise WalletNotFoundException(id)
       return wallet
    
    def find_by_status(self,status:TransactionStatus)->List[Transaction]:
       list=self.repo.find_by_status(status)
    
    def find_by_payment(self,payment:PaymentMethod)->List[Transaction]:
       print(payment, type(payment))
       return self.repo.find_by_payment_type(payment)