from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
from app.config.config import URL as DB_URL

Base=declarative_base()
engine=create_engine(DB_URL)
SessionLocal=sessionmaker(bind=engine,autoflush=True,autocommit=False)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()