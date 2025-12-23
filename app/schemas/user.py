from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str | None = None
    phone: int | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserUpdate(UserCreate):
    name: str | None = None
    phone: int | None = None

class UserResponse(UserCreate):
    id: int
    name: str
    phone: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config={
        "from_attributes":True
    }
class LoginRequest(BaseModel):
    email:str
    password:str

        
