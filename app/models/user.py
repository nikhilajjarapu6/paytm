from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(255),nullable=False)
    phone=Column(String(255),nullable=False,unique=True)
    email=Column(String(255),unique=True,nullable=False)
    password=Column(String(255),nullable=False)
    created_at=Column(DateTime,nullable=False,default=datetime.utcnow())
    updated_at=Column(DateTime,nullable=False,default=datetime.utcnow(),onupdate=datetime.utcnow())
    wallet=relationship("Wallet",back_populates="user",uselist=False)
