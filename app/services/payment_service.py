from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.wallet_service import WalletService
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.schemas.payment import PaymentRequest
from app.models.wallet import Wallet
from typing import List,Optional
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRequest,TransactionStatus
from app.exceptions.wallet_exceptions import WalletNotFoundException,InsufficientBalanceException,WalletException

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.wallet_service = WalletService(db)
        self.transaction_service = TransactionService(db)

    def generate_txn_id(self) -> str:
        self.db.execute(text("INSERT INTO txn_sequence VALUES ()"))
        next_id = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        return f"TXN{next_id + 10000}"

    def send(self, payment: PaymentRequest) -> Transaction:
        with self.db.begin():
            sender_wallet = self.wallet_service.find_wallet_by_id(payment.sender_id)
            receiver_wallet = self.wallet_service.find_wallet_by_id(payment.receiver_id)

            if not sender_wallet or not receiver_wallet:
                raise WalletNotFoundException(payment.sender_id)

            if sender_wallet.id == receiver_wallet.id:
                raise WalletException(payment.sender_id,payment.receiver_id)

            if sender_wallet.balance < payment.amount:
                raise InsufficientBalanceException(sender_wallet.id,payment.amount,sender_wallet.balance)
            txn_id_random=self.generate_txn_id()
            txn = self.transaction_service.create_initiated(
                txn_id=txn_id_random,
                sender_id=sender_wallet.id,
                receiver_id=receiver_wallet.id,
                amount=payment.amount,
                payment_method=payment.payment_method,
                description=payment.description
            )

            if payment.amount > 1000:
                self.transaction_service.mark_fail(txn)
                return txn

            self.wallet_service.deduct_balance(sender_wallet.id, payment.amount)
            self.wallet_service.add_balance(receiver_wallet.id, payment.amount)
            

            self.transaction_service.mark_success(txn)
            return txn

    def refund(self, txn_id: str) -> Transaction:
        with self.db.begin():
            txn = self.transaction_service.find_by_txn_id(txn_id)

            if not txn or txn.transaction_status != TransactionStatus.SUCCESS:
                raise ValueError("Invalid transaction")

            if txn.transaction_status == TransactionStatus.REVERSED:
                return txn  # idempotent refund

            self.wallet_service.add_balance(txn.sender_id, txn.amount)
            self.wallet_service.deduct_balance(txn.receiver_id, txn.amount)
            self.transaction_service.mark_reversed(txn)
            return txn
# def refund(self, txn_id: str) -> Transaction:
#     with self.db.begin():

#         original_txn = self.transaction_service.find_by_txn_id(txn_id)

#         if not original_txn:
#             raise ValueError("Transaction not found")

#         if original_txn.transaction_status != TransactionStatus.SUCCESS:
#             raise ValueError("Only successful transactions can be refunded")

#         # idempotency check
#         if self.transaction_service.has_refund(original_txn.id):
#             return self.transaction_service.get_refund(original_txn.id)

#         # lock wallets (important)
#         sender_wallet = self.wallet_service.lock_wallet(original_txn.receiver_id)
#         receiver_wallet = self.wallet_service.lock_wallet(original_txn.sender_id)

#         refund_txn = Transaction(
#             sender_id=original_txn.receiver_id,
#             receiver_id=original_txn.sender_id,
#             amount=original_txn.amount,
#             payment_method=original_txn.payment_method,
#             transaction_status=TransactionStatus.REVERSED,
#             description=f"Refund for {original_txn.txn_id}",
#             txn_id=self.generate_txn_id(),
#             parent_txn_id=original_txn.id   # 
#         )

#         self.wallet_service.deduct_balance(sender_wallet.id, original_txn.amount)
#         self.wallet_service.add_balance(receiver_wallet.id, original_txn.amount)

#         self.transaction_repo.add(refund_txn)

#         return refund_txn

# parent_txn_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)

