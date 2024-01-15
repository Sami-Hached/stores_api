from sqlalchemy.orm import Session
from . import models
from . import schemas
from uuid import UUID


def get_store(db: Session, store_id: int):
    return db.query(models.StoresDB).filter(models.StoresDB.id == store_id).first()


def get_store_by_email(db: Session, email: str):
    return db.query(models.StoresDB).filter(models.StoresDB.email == email).first()


def get_all_stores(db: Session, limit: int = 100):
    return db.query(models.StoresDB).limit(limit).all()


def create_store(db: Session, store: schemas.CreateStore) -> schemas.ViewStore:
    # This is where to use UUID for store_ids to be added?
    db_store = models.StoresDB(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return schemas.ViewStore(
        id=db_store.id,
        city=db_store.city,
        email=db_store.email,
        brand=db_store.brand,
    )


def delete_store(db: Session, store_id: int) -> None:
    db.query(models.StoresDB).filter(models.StoresDB.id == store_id).delete()
    db.commit()


def update_store(db: Session, store_id: UUID, updated_store: schemas.CreateStore) -> schemas.ViewStore:
    (
        db.query(models.StoresDB).
        filter(models.StoresDB.id == store_id).
        update(updated_store.dict())
    )
    db.commit()
    return schemas.ViewStore(
        id=store_id,
        city=updated_store.city,
        email=updated_store.email,
        brand=updated_store.brand,
    )


def delete_all_store(db: Session) -> None:
    db.query(models.StoresDB).delete()
    db.commit()
