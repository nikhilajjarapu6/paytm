from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.payment_service import PaymentService
from app.schemas.payment import PaymentRequest,PaymentResponse,MobilePaymentRequest
from app.security.path import current_user
from app.models.user import User

payment_router=APIRouter(prefix="/payment")

def get_service(db:Session=Depends(get_db))->PaymentService:
    return PaymentService(db)

@payment_router.post("/payment_send",response_model=PaymentResponse)
def send_money(payment:PaymentRequest,current:User=Depends(current_user),service:PaymentService=Depends(get_service)):
    print(current)
    return service.send(payment,current)

@payment_router.post("/payment_receive",response_model=PaymentResponse)
def receove_money(payment:PaymentRequest,current:User=Depends(current_user),service:PaymentService=Depends(get_service)):
    return service.receive(payment,current)

@payment_router.post("/upi_send",response_model=PaymentResponse)
def send_money_upi(payment:MobilePaymentRequest,current:User=Depends(current_user),service:PaymentService=Depends(get_service)):
    return service.send_upi(payment,current)