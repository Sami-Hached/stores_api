from sqlalchemy.orm import Session
from . import models, schemas

def get_store(db: Session, store_id: int):
    return db.query(models.StoresDB).filter(models.StoresDB.id == store_id).first()

def get_all_stores(db: Session, limit: int = 100):
    return db.query(models.StoresDB).limit(limit).all()

def create_user(db: Session, store: schemas.CreateStore):
    # This is where to use UUID for store_ids to be added?
    db_store = models.StoresDB(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store
