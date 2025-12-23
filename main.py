from app.database.database import engine,Base
from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.models import user,wallet,transaction
from app.routers.user_router import user_router
from app.routers.wallet_router import wallet_router
from app.routers.payment_router import payment_router
from app.routers.transaction_rounter import trans_router
from app.exceptions.base import PaymentException


app=FastAPI(title="Paytm clone",description="Digital Wallet System",version="1.0.0")
Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "Paytm Clone API running"}

@app.exception_handler(PaymentException)
async def paytm_exception_handler(request:Request,exc:PaymentException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code":exc.code,"message":exc.msg,"http_code":exc.status_code
        }
    )
app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(payment_router)
app.include_router(trans_router)
