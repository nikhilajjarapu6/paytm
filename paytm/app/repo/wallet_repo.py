from sqlalchemy.orm import Session
from app.models.wallet import Wallet
from app.schemas.wallet import WalletResponse
from typing import Optional

class WalletRepo():
    def __init__(self,db:Session):
        self.db=db
    
    def create(self,data:Wallet)->Wallet:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data
    
    def save(self,data:Wallet)->Optional[Wallet]:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def find_by_id(self,id:int)->Wallet:
        return self.db.query(Wallet).filter(Wallet.id==id).first()
    
    def find_by_user_id(self,user_id:int)->Wallet:
        return self.db.query(Wallet).filter(Wallet.user_id==user_id).first()
    
    def delete(self, wallet: Wallet):
        self.db.delete(wallet)
        self.db.commit()

        
