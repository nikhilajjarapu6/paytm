from sqlalchemy.orm import Session
from app.services.wallet_service import WalletService
from app.services.transaction_service import TransactionService
from app.schemas.payment import PaymentRequest,PaymentResponse,PaymentMethod
from app.models.wallet import Wallet
from typing import List,Optional
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRequest,TransactionStatus

class PaymentService:
    def __init__(self,db:Session):
        self.db=db
        self.service=WalletService(db)
        self.transaction=TransactionService(db)

    def send(self,payment:PaymentRequest)->Transaction:
        with self.db.begin():
            sender_wallet=self.service.find_wallet_by_id(payment.sender_id)
            receiver_wallet=self.service.find_wallet_by_id(payment.receiver_wallet_id)

            if not sender_wallet or not receiver_wallet:
                 raise Exception("no wallet found")
            
            if sender_wallet.id == receiver_wallet.id:
                raise ValueError("Cannot send money to same wallet")

            if sender_wallet.balance < payment.amount:
                raise ValueError("Insufficient balance")
        
            req=self.transaction.create_initiated(
                sender_wallet.id,payment.receiver_wallet_id,payment.amount,payment.payment_method,payment.description
            )
            try:
                self.service.deduct_balance(sender_wallet.id,payment.amount)
                self.service.add_balance(receiver_wallet.id,payment.amount)
                self.transaction.mark_success(req)

            except Exception:
                self.transaction.mark_fail(req)
                raise       
            return req
    
    def receive(self,payment:PaymentRequest)->Transaction:
        with self.db.begin():
            sender_wallet=self.service.find_wallet_by_id(payment.sender_id)
            receiver_wallet=self.service.find_wallet_by_id(payment.receiver_wallet_id)

            if not sender_wallet or not receiver_wallet:
                 raise Exception("no wallet found")
            
            if sender_wallet.id == receiver_wallet.id:
                raise ValueError("Cannot send money to same wallet")

            if sender_wallet.balance < payment.amount:
                raise ValueError("Insufficient balance")
        
            req=self.transaction.create_initiated(
                sender_wallet.id,payment.receiver_wallet_id,payment.amount,payment.payment_method,payment.description
            )
            try:
                self.service.deduct_balance(receiver_wallet.id,payment.amount)
                self.service.add_balance(sender_wallet.id,payment.amount)
                self.transaction.mark_success(req)

            except Exception:
                self.transaction.mark_fail(req)
                raise       
            return req
            
    def refund(self,txn_id)->Transaction:
        with self.db.begin():
            txn=self.transaction.find_by_txn_id(txn_id)

            if not txn or txn.transaction_status!=TransactionStatus.SUCCESS:
                raise Exception("no transaction was found")
            
            self.service.add_balance(txn.sender_id,txn.amount)
            self.service.deduct_balance(txn.receiver_id,txn.amount)
            self.transaction.mark_reversed(txn)
            return txn

