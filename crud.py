from sqlalchemy.orm import Session
import models
import schemas


def get_store(db: Session, store_id: int):
    return db.query(models.StoresDB).filter(models.StoresDB.id == store_id).first()


def get_store_by_email(db: Session, email: str):
    return db.query(models.StoresDB).filter(models.StoresDB.email == email).first()


def get_all_stores(db: Session, limit: int = 100):
    return db.query(models.StoresDB).limit(limit).all()


def create_store(db: Session, store: schemas.CreateStore):
    # This is where to use UUID for store_ids to be added?
    db_store = models.StoresDB(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def delete_store(db: Session, store_id: int):
    db.query(models.StoresDB).filter(models.StoresDB.id == store_id).delete()
    db.commit()
    return


def delete_all_store(db: Session):
    db.query(models.StoresDB).delete()
    db.commit()
    return
