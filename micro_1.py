import uvicorn
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI

from db import SessionLocal, Base, engine, RegistryBase, RegistryCreate, create_registry

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/registry/", response_model=RegistryBase)
def create_user(registry: RegistryCreate, db: Session = Depends(get_db)):
    return create_registry(db=db, registry=registry)
