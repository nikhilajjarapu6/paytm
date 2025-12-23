from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import List, Optional


class UserRepo:
    def __init__(self, db: Session):
        self.db = db
    def create(self,data:User)->User:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    def get_by_id(self,id:int)->User|None:
        return self.db.query(User).filter(User.id==id).first()
    
    def find_all(self):
        return self.db.query(User).all()
    
    def find_by_email(self,email:str)->User|None:
        return (self.db.query(User).filter(User.email==email).first())
    def finb_by_mobile(self,mobile:str)->User|None:
        return (self.db.query(User).filter(User.phone==mobile).first())
    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

    def update(self,user:User)->Optional[User]:
        self.db.commit()
        self.db.refresh(user)
        return user
    
    # def update(self,db:Session,id:int,user:UserUpdate):
    #     fetched=db.query(User).filter(User.id==id).first()
    #     if not fetched:
    #         return None
    #     user_dict=user.model_dump(exclude_unset=True)
    #     for k,v in user_dict.items():
    #         setattr(fetched,k,v)
    #     db.commit()
    #     db.refresh(fetched)
    #     return fetched
    
    # def delete(self,db:Session,id:int):
    #     fetched=db.query(User).filter(User.id==id).first()
    #     if not fetched:
    #         return None
    #     db.delete(fetched)
    #     return fetched

