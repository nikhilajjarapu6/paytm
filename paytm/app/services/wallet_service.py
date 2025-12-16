from sqlalchemy.orm import Session
from app.schemas.wallet import WalletResponse
from app.repo.transaction_repo import TransactionRepo
from app.models.wallet import Wallet
from app.repo.wallet_repo import WalletRepo
from typing import Optional
from app.models.transaction import Transaction
from decimal import Decimal


class WalletService:
    def __init__(self,db:Session):
        self.repo=WalletRepo(db)
    
    def add_balance(self,wallet_id:int,amount:Decimal)->Optional[Wallet]:
        if amount<=0 :
            raise ValueError("Amount must be greater than zero")
        
        wallet=self.repo.find_by_id(wallet_id)
        if not wallet:
            raise Exception("Wallet not found")
        if not wallet.is_active:
            raise ValueError("Wallet is inactive")
        wallet.balance+=amount
        self.repo.save(wallet)
        return wallet
    def deduct_balance(self,wallet_id:int,amount:Decimal)->Optional[Wallet]:
        if amount<0 :
            raise Exception("balance should not be negative")
        
        wallet=self.repo.find_by_id(wallet_id)
        if not wallet:
            raise Exception("Wallet not found")
        if not wallet.is_active:
            raise ValueError("Wallet is inactive")
        if wallet.balance<amount:
            raise Exception("Insufficient balance")
        wallet.balance-=amount
        self.repo.save(wallet)
        return wallet
    
    def find_wallet_by_id(self,wallet_id:int)->Optional[Wallet]:
        return self.repo.find_by_id(wallet_id)
    
    def find_wallet_by_user_id(self,user_id:int)->Optional[Wallet]:
        return self.repo.find_by_user_id(user_id)
    
    def check_balance(self,wallet_id:int)->Decimal|None:
        wallet=self.repo.find_by_id(wallet_id)
        if not wallet:
            raise Exception("Wallet not found")
        return wallet.balance
    def deactivate_wallet(self, wallet_id: int) -> Wallet:
        wallet = self.repo.get_by_id(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        wallet.is_active = False
        return self.repo.save(wallet)

    def activate_wallet(self, wallet_id: int) -> Wallet:
        wallet = self.repo.get_by_id(wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        wallet.is_active = True
        return self.repo.save(wallet)