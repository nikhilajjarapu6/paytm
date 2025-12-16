from sqlalchemy.orm import Session
from app.repo.user_repo import UserRepo
from app.repo.wallet_repo import WalletRepo
from app.schemas.user import UserCreate,UserUpdate
from app.models.user import User
from app.models.wallet import Wallet
from typing import Optional,List

class UserService:
    def __init__(self,db:Session):
        self.repo=UserRepo(db)
        self.wallet_repo=WalletRepo(db)
    
    def create_user(self,data:UserCreate)->Optional[User]:
        fetched=User(**data.model_dump())
        existing=self.repo.find_by_email(data.email)
        if existing:
            raise ValueError("user with this email alredy exists")
        user=self.repo.create(fetched)
        wallet=Wallet(user_id=user.id,balance=0)
        self.wallet_repo.create(wallet)
        return user
    def get_user_by_id(self,id:int)->Optional[User]:
        return self.repo.get_by_id(id)
    
    def get_user_by_email(self,email:str)->Optional[User]:
        return self.repo.find_by_email(email)
    
    def get_all(self)->List[User]:
        return self.repo.find_all()
    
    def update_user(self,id:int,data:UserUpdate)->Optional[User]:
        fetched=self.repo.get_by_id(id)
        if not fetched:
            raise Exception("No user found")
        updated=data.model_dump(exclude_unset=True)
        for k,v in updated.items():
            setattr(fetched,k,v)
        self.repo.create(fetched)
        return fetched

    def delete_user(self,id:int)->Optional[User]:
        fetched=self.repo.get_by_id(id)
        if not fetched:
            raise Exception("No user found")
        self.repo.delete(fetched)
        return fetched

        

