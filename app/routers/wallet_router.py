from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.wallet import Wallet
from app.schemas.wallet import WalletResponse
from app.services.wallet_service import WalletService
from app.security.path import current_user
from app.models.user import User

wallet_router=APIRouter(prefix="/wallet")
def get_service(db:Session=Depends(get_db))->WalletService:
    return WalletService(db)

@wallet_router.get("/find/{id}")
def find_by_id(id:int,service:WalletService=Depends(get_service)):
    return service.find_wallet_by_id(id)

@wallet_router.get("/find_wallet_user")
def find_by_user_id(current:User=Depends(current_user),service:WalletService=Depends(get_service)):
    return service.find_wallet_by_user_id(current)

@wallet_router.get("/check_balance")
def check_balance(current:User=Depends(current_user),service:WalletService=Depends(get_service)):
    return service.check_balance(current)