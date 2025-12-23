from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from typing import Optional

class WalletRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: Wallet) -> Wallet:
        self.db.add(data)
        return data

    def save(self, data: Wallet) -> Wallet:
        self.db.add(data)
        return data

    def find_by_id(self, id: int) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.id == id).first()

    def find_by_user_id(self, user_id: int) -> Optional[Wallet]:
        return self.db.query(Wallet).filter(Wallet.user_id == user_id).first()

    def delete(self, wallet: Wallet):
        self.db.delete(wallet)
