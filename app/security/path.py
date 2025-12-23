from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from app.config.config import ALGORITHAM,ACCESS_TOKEN_EXPIRE_MINUTES,SECRET_KEY
from app.schemas.token import TokenPayload,TokenResponse
from datetime import timedelta,datetime
from app.exceptions.user_exceptions import EmailnotFOundException,UserNotFoundException
from app.database.database import get_db


context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth=OAuth2PasswordBearer(tokenUrl="/users/login")

def hash_pwd(password:str):
    return context.hash(password)

def verify_pwd(password,hashed):
    return context.verify(password,hashed)

def create_token(data:TokenPayload):
    payload=data.model_dump()
    token_expire_minutes = 60 * 24  # 1 day
    expire = datetime.utcnow() + timedelta(minutes=token_expire_minutes)

    payload.update({
        "exp": int(expire.timestamp()),          
        "iat": int(datetime.utcnow().timestamp()) 
    })

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHAM)

def verify_token(token:str=Depends(oauth)):
    try:
        payload= jwt.decode(token,SECRET_KEY,ALGORITHAM)
        if payload:
            print(payload)
        return payload
    except JWTError:
        return None

def current_user(token:str=Depends(oauth),db:Session=Depends(get_db)):
    from app.services.user_service import UserService
    try:
        payload= jwt.decode(token,SECRET_KEY,ALGORITHAM)
    except JWTError:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if payload:
            print(payload)
    email=payload.get("sub")
    if not email:
            raise EmailnotFOundException(email)
    service=UserService(db)
    db_user=service.get_user_by_auth_email(email)
    if not db_user:
         raise EmailnotFOundException(email)
    return db_user
    
        