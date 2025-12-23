from fastapi import FastAPI,HTTPException,APIRouter,Depends
from app.services.user_service import UserService
from app.schemas.user import UserResponse,UserCreate,UserUpdate
from app.database.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.schemas.user import LoginRequest
from typing import List
from app.security.path import create_token,current_user
from app.schemas.token import TokenPayload,TokenResponse

user_router=APIRouter(prefix="/users")

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)



@user_router.post("/save",response_model=UserResponse)
def create(user:UserCreate,service:UserService=Depends(get_user_service)):
    return service.create_user(user)

@user_router.get("/find_by_id/{id}",response_model=UserResponse)
def find_by_id(id:int,current:User=Depends(current_user),service:UserService=Depends(get_user_service)):
    return service.get_user_by_id(id,current)

@user_router.post("/find_by_email",response_model=UserResponse)
def find_by_email(email:str,current:User=Depends(current_user),service:UserService=Depends(get_user_service)):
    return service.get_user_by_email(email,current)

@user_router.post("/find_by_mobile",response_model=UserResponse)
def find_by_mobile(mobile:int,current:User=Depends(current_user),service:UserService=Depends(get_user_service)):
    return service.find_by_mobile(mobile,current)

@user_router.put("/update/{id}")
def update(id:int,user:UserCreate,current:User=Depends(current_user),service:UserService=Depends(get_user_service)):
    return service.update_user(id,user,current)

@user_router.get("/list",response_model=List[UserResponse])
def find_all(service:UserService=Depends(get_user_service)):
    return service.get_all()

@user_router.post("/login",response_model=TokenResponse)
def login(user:LoginRequest,service:UserService=Depends(get_user_service)):
    db_user=service.login(user.email,user.password)
    token=create_token(TokenPayload(sub=db_user.email,issued=db_user.name))
    print(db_user.email,db_user.password)
    print(token)
    return {"access_token":token,"token_type":"bearer"}