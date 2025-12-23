from sqlalchemy.orm import Session
from fastapi import FastAPI,APIRouter,Depends
from app.services.transaction_service import TransactionService
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse,PaymentMethod
from typing import List
from app.database.database import get_db

trans_router=APIRouter(prefix="/transactions")

def get_service(db:Session=Depends(get_db))->Transaction:
    return TransactionService(db)

@trans_router.get("/findByTxnId/{id}",response_model=TransactionResponse)
def find_by_id(id:str,service:TransactionService=Depends(get_service),db:Session=Depends(get_db)):
    return service.find_by_txn_id(id)

@trans_router.get("/findByWallet/{id}",response_model=List[TransactionResponse])
def find_by_wallet(id:int,service:TransactionService=Depends(get_service)):
    return service.find_by_wallet(id)

@trans_router.get("/findByPayment/{payment}",response_model=List[TransactionResponse])
def find_by_payment(payment:PaymentMethod,service:TransactionService=Depends(get_service)):
    return service.find_by_payment(payment)