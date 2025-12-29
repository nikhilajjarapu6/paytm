from sqlalchemy.orm import Session
from app.repo.user_repo import UserRepo
from app.repo.wallet_repo import WalletRepo
from app.schemas.user import UserCreate,UserUpdate,EmailRequest
from app.models.user import User
from app.models.wallet import Wallet
from typing import Optional,List
from app.exceptions.user_exceptions import UserNotFoundException,EmailnotFOundException,MobilenotFOundException,InvalidCredException,UserForbidden
from app.security.path import verify_pwd, hash_pwd
from app.utils.authorization import ownership

class UserService:
    def __init__(self,db:Session):
        self.repo=UserRepo(db)
        self.wallet_repo=WalletRepo(db)
    
    def create_user(self,data:UserCreate)->Optional[User]:
        # Hash password before creating user
        user_dict = data.model_dump()
        if user_dict.get('password'):
            user_dict['password'] = hash_pwd(user_dict['password'])
        fetched=User(**user_dict)
        existing=self.repo.find_by_email(data.email)
        if existing:
            raise UserNotFoundException(fetched.id)
        user=self.repo.create(fetched)
        wallet=Wallet(user_id=user.id,balance=0)
        self.wallet_repo.create(wallet)
        return user
    def get_user_by_id(self,id:int,current:User)->Optional[User]:
        fetched=self.repo.get_by_id(id)
        if not fetched: 
            raise UserNotFoundException(id)
        ownership(current.id,fetched.id)    #function for auth
        return fetched
    
    def get_user_by_email(self,email:str,current:User)->Optional[User]:
        fetched= self.repo.find_by_email(email)
        print(fetched)
        if not fetched:
            raise EmailnotFOundException(email)
        ownership(current.id,fetched.id)
        return fetched
    
    def get_user_by_auth_email(self,email:str)->Optional[User]:
        fetched= self.repo.find_by_email(email)
        if not fetched:
            raise EmailnotFOundException(email)
        return fetched
    
    def find_by_mobile(self,phone:str,current:User)->Optional[User]:
        fetched=self.repo.finb_by_mobile(phone)
        if not fetched:
            raise MobilenotFOundException(phone)
        ownership(current.id,fetched.id)
        return fetched
    
    def get_all(self)->List[User]:
        return self.repo.find_all()
    
    def update_user(self,data:UserUpdate,current:User)->Optional[User]:
        fetched=self.repo.get_by_id(current.id)
        if not fetched:
            raise UserNotFoundException(current.id)
        ownership(current.id,fetched.id)
        updated=data.model_dump(exclude_unset=True)
        # If password provided, hash it before saving
        if 'password' in updated and updated.get('password'):
            updated['password'] = hash_pwd(updated['password'])

        for k,v in updated.items():
            setattr(fetched,k,v)
        # Use repo.update to commit changes for existing user
        self.repo.update(fetched)
        return fetched

    def delete_user(self,id:int)->Optional[User]:
        fetched=self.repo.get_by_id(id)
        if not fetched:
            raise UserNotFoundException(id)
        self.repo.delete(fetched)
        return fetched
    def login(self,email:str,password:str)->Optional[User]:
        user=self.repo.find_by_email(email)
        if not user:
            raise EmailnotFOundException(email)
        if not verify_pwd(password,user.password):
            raise InvalidCredException()
        return user
