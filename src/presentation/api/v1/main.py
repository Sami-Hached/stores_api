import logging
import os
import uuid

from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.infrastructure import crud, schemas, models
from src.infrastructure.database import get_engine, get_session

app = FastAPI()

config = {
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "host": os.environ["DB_HOST"],
    "port": os.environ["DB_PORT"],
    "database": os.environ["DB_DATABASE"],
}

# # This config is only to be used while debugging
# config = {
#     "user": "sami",
#     "password": "secret_123",
#     "host": "localhost",
#     "port": "5432",
#     "database": "learning_sql",
# }

# This creates the database
models.Base.metadata.create_all(bind=get_engine(config))

# Dependency
def get_db() -> Session:
    session = get_session(config)
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root_get() -> str:
    return "Hello, world!"


@app.get("/items", tags=["get_methods"])
async def read_all_item(db: Session = Depends(get_db)) -> list[schemas.ViewStore]:
    return crud.get_all_stores(db)


@app.get("/items/{email}")
async def read_item(email: str, db: Session = Depends(get_db)) -> schemas.ViewStore:
    db_store = crud.get_store_by_email(db, email=email)
    if db_store is None:
        raise HTTPException(status_code=404, detail="store not found")
    return serialize_store(db_store)


@app.post("/add_item")
async def add_item(store: schemas.CreateStore, db: Session = Depends(get_db)):
    db_store = crud.get_store_by_email(db, store.email)
    if db_store:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_store(db=db, store=store)


@app.put("/update_item/{item_id}")
async def update_item(item_id: str, updated_store: schemas.CreateStore, db: Session = Depends(get_db)) -> dict:
    item_uuid = uuid.UUID(item_id)

    try:
        result = crud.update_store(db, item_uuid, updated_store)
    except IntegrityError as same_email:
        raise HTTPException(401, detail=repr(same_email.detail))

    return {
        "msg": f"Store with item_id: {str(item_uuid)} has been updated."
            }


@app.post("/delete_item/{item_id}")
async def delete_item(item_id: str, db: Session = Depends(get_db)) -> str:
    item_uuid = uuid.UUID(item_id)
    crud.delete_store(db, item_uuid)
    return f"Store with item_id: {item_uuid} has been deleted."


@app.post("/delete_all")
async def delete_table(db: Session = Depends(get_db)):
    crud.delete_all_store(db)
    return "all stores have been deleted."


def serialize_store(db_item: models.StoresDB) -> schemas.ViewStore:
    return schemas.ViewStore(
        id=db_item.id, city=db_item.city, email=db_item.email, brand=db_item.brand
    )
