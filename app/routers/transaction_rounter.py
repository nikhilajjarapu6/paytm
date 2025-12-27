from sqlalchemy.orm import Session
from fastapi import FastAPI,APIRouter,Depends
from app.services.transaction_service import TransactionService
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionResponse,PaymentMethod
from typing import List
from app.database.database import get_db
from app.security.path import current_user
from app.models.user import User
trans_router=APIRouter(prefix="/transactions")

def get_service(db:Session=Depends(get_db))->Transaction:
    return TransactionService(db)

@trans_router.get("/findByTxnId/{id}",response_model=TransactionResponse)
def find_by_id(id:str,current:User=Depends(current_user),service:TransactionService=Depends(get_service)):
    return service.find_by_txn_id(id,current)

@trans_router.get("/findByWallet/{id}",response_model=List[TransactionResponse])
def find_by_wallet(id:int,service:TransactionService=Depends(get_service)):
    return service.find_by_wallet(id)

@trans_router.get("/mytransactions",response_model=List[TransactionResponse])
def list_transactions(user:User=Depends(current_user),service:TransactionService=Depends(get_service)):
    return service.find_my_transactions(user)

@trans_router.get("/findByPayment/{payment}",response_model=List[TransactionResponse])
def find_by_payment(payment:PaymentMethod,service:TransactionService=Depends(get_service)):
    return service.find_by_payment(payment)

@trans_router.get("/date_sorted/{sort}",response_model=list[TransactionResponse])
def list_my_transaction_date(sort:str,user:User=Depends(current_user),service:TransactionService=Depends(get_service)):
    return service.date_sorted_transactions(sort,user)