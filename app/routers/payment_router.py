from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.payment_service import PaymentService
from app.schemas.payment import PaymentRequest,PaymentResponse

payment_router=APIRouter(prefix="/payment")

def get_service(db:Session=Depends(get_db))->PaymentService:
    return PaymentService(db)

@payment_router.post("/payment_send",response_model=PaymentResponse)
def send_money(payment:PaymentRequest,service:PaymentService=Depends(get_service)):
    return service.send(payment)

@payment_router.post("/payment_receive",response_model=PaymentResponse)
def receove_money(payment:PaymentRequest,service:PaymentService=Depends(get_service)):
    return service.receive(payment)