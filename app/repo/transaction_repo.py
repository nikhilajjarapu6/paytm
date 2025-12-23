from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionStatus, PaymentMethod
from typing import List, Optional

class TransactionRepo:
    def __init__(self, db: Session):
        self.db = db

    def add(self, txn: Transaction) -> Transaction:
        self.db.add(txn)
        return txn

    def find_by_id(self, id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == id).first()

    def find_by_txn_id(self, txn_id: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.txn_id == txn_id).first()

    def find_by_wallet(self, wallet_id: int) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(
                (Transaction.sender_id == wallet_id) |
                (Transaction.receiver_id == wallet_id)
            )
            .order_by(Transaction.created_at.desc())
            .all()
        )

    def find_by_status(self, status: TransactionStatus) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.transaction_status == status)
            .all()
        )

    def find_by_payment_type(self, method: PaymentMethod) -> List[Transaction]:
        return (
            self.db.query(Transaction)
            .filter(Transaction.payment_method == method.value)
            .all()
        )
