from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

app = FastAPI()

# Leaving these credentials here for debugging
host = "0.0.0.0"  # Use the service name as the hostname ("localhost" works)
port = 5432
database = "learning_sql"
user = "sami"
password = "secret_123"

# This creates the database
models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root_get() -> None:
    return {"message": "Hello World"}


@app.get("/items")
async def read_all_item(db: Session = Depends(get_db)) -> list[schemas.ViewStore]:
    return crud.get_all_stores(db)


@app.get("/items/{item_id}")
async def read_item(item_id: int, db: Session = Depends(get_db)) -> schemas.ViewStore:
    db_store = crud.get_store(db, store_id=item_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="store not found")
    return serialize_store(db_store)


def serialize_store(db_item: models.StoresDB) -> schemas.ViewStore:
    return schemas.ViewStore(id=db_item.id, city=db_item.city, email=db_item.email, brand=db_item.brand)


@app.post("/add_item")
async def add_item(store: schemas.CreateStore, db: Session = Depends(get_db)):
    db_store = crud.get_store_by_email(db, store.email)
    if db_store:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_store(db=db, store=store)


@app.post("/delete_item/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    crud.delete_store(db, item_id)
    return f"Store with item_id: {item_id} has been deleted."


@app.post("/delete_all")
async def delete_table(db: Session = Depends(get_db)):
    crud.delete_all_store(db)
    return "all stores have been deleted."
