from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from walrus import Database as RedisDatabase
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

redisDatabase = RedisDatabase(host='localhost', port=6379, db=0)

Base = declarative_base()

class Registry(Base):
    __tablename__ = "registries"

    id = Column(Integer, primary_key=True, index=True)
    kwh = Column(String(10))
    
class RegistryCreate(BaseModel):
    kwh: str
    
class RegistryBase(RegistryCreate):
    id: int
    kwh: str

    class Config:
        orm_mode = True

def create_registry(db: Session, registry: RegistryCreate):
    db_registry = Registry(kwh=registry.kwh)
    try:
        db.add(db_registry)
        db.commit()
        db.refresh(db_registry)
        
        stream = 'data-entry'
        #redisDatabase.xadd(stream, {'data': ''})
        cg = redisDatabase.consumer_group('cg-energy', stream)
        #cg.create()  # Create the consumer group.
        #cg.set_id('$')
        cg.data_entry.add({'data': registry.kwh})
        
        return db_registry
    except Exception as error:
        db.rollback()
        return error