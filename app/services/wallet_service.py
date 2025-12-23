from sqlalchemy.orm import Session
from app.schemas.wallet import WalletResponse
from app.repo.transaction_repo import TransactionRepo
from app.models.wallet import Wallet
from app.repo.wallet_repo import WalletRepo
from typing import Optional
from app.models.transaction import Transaction
from decimal import Decimal
from app.exceptions.wallet_exceptions import InactiveWalletException,WalletNotFoundException,InsufficientBalanceException,NegativeBalException
from app.exceptions.user_exceptions import UserNotFoundException
from app.security.path import current_user
from app.models.user import User
from app.utils.authorization import ownership


class WalletService:
    def __init__(self,db:Session):
        self.repo=WalletRepo(db)
    
    def add_balance(self,wallet_id:int,amount:Decimal)->Optional[Wallet]:
        if amount<=0 :
            raise NegativeBalException(wallet_id,amount)
        
        wallet=self.repo.find_by_id(wallet_id)
        if not wallet:
            raise WalletNotFoundException(wallet_id)
        if not wallet.is_active:
            raise InactiveWalletException(wallet_id)
        wallet.balance+=amount
        self.repo.save(wallet)
        return wallet
    
    def add_money_auth(self,amount:Decimal,current:User)->Optional[Wallet]:
        wallet=self.repo.find_by_user_id(current.id)
        if amount<=0 :
            raise NegativeBalException(wallet.id,amount)

        if not wallet:
            raise WalletNotFoundException(wallet.id)
        if not wallet.is_active:
            raise InactiveWalletException(wallet.id)
        wallet.balance+=amount
        self.repo.save(wallet)
        return wallet
    

    def deduct_balance(self,wallet_id:int,amount:Decimal)->Optional[Wallet]:
        if amount<0 :
           raise NegativeBalException(wallet_id,amount)
        wallet=self.repo.find_by_id(wallet_id)
        if not wallet:
            raise WalletNotFoundException(wallet_id)
        if not wallet.is_active:
            raise InactiveWalletException(wallet_id)
        if wallet.balance<amount:
            raise InsufficientBalanceException(wallet_id,amount,wallet.balance)
        wallet.balance-=amount
        self.repo.save(wallet)
        return wallet
    
    def deduct_balance_auth(self,amount:Decimal,current:User)->Optional[Wallet]:
        wallet=self.repo.find_by_user_id(current.id)
        if amount<0 :
           raise NegativeBalException(wallet.id,amount)  
        if not wallet:
            raise WalletNotFoundException(wallet.id)
        if not wallet.is_active:
            raise InactiveWalletException(wallet.id)
        if wallet.balance<amount:
            raise InsufficientBalanceException(wallet.id,amount,wallet.balance)
        wallet.balance-=amount
        self.repo.save(wallet)
        return wallet
    
    def find_wallet_by_id(self,wallet_id:int)->Optional[Wallet]:
        fetched= self.repo.find_by_id(wallet_id)
        if not fetched:
            raise WalletNotFoundException(wallet_id)
        return fetched
    
    
    def find_wallet_by_user_id(self,id:int)->Optional[Wallet]:
        fetched=self.repo.find_by_user_id(id)
        if not fetched:
            raise UserNotFoundException(id)
        ownership(id,fetched.user_id)
        return fetched
    
    def check_balance(self,wallet_id:int)->Decimal|None:
        wallet=self.repo.find_by_id(wallet_id)
        if not wallet:
            raise WalletNotFoundException(wallet_id)
        return wallet.balance
    
    def check_balance(self,current:User)->Decimal|None:
        wallet=self.repo.find_by_user_id(current.id)
        if not wallet:
            raise WalletNotFoundException(wallet.id)
        return wallet.balance
    
    def deactivate_wallet(self, current:User) -> Wallet:
        wallet=self.repo.find_by_user_id(current.id)
        if not wallet:
            raise WalletNotFoundException(wallet.id)

        wallet.is_active = False
        return self.repo.save(wallet)

    def activate_wallet(self, current:User) -> Wallet:
        wallet=self.repo.find_by_user_id(current.id)
        if not wallet:
            raise WalletNotFoundException(wallet.id)

        wallet.is_active = True
        return self.repo.save(wallet)
    