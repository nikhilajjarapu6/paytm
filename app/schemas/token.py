from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub:str
    issued:str

class TokenResponse(BaseModel):
    access_token:str
    token_type:str = "bearer"