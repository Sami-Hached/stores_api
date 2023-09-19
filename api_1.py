from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel, Field

app = FastAPI()


class CreateStore(BaseModel):
    city: str
    email: str = Field(max_length=20)
    brand: str


class ViewStore(BaseModel):
    id: int = Field()
    city: str = Field()
    email: str = Field(max_length=20)
    brand: str = Field()


host = "0.0.0.0"  # Use the service name as the hostname ("localhost" works)
port = 5432
database = "learning_sql"
user = "sami"
password = "secret_123"

conn = psycopg2.connect(
    host=host,
    port=port,
    dbname=database,
    user=user,
    password=password,
    connect_timeout=3600,
)


@app.get("/")
async def root_get():
    return {"message": "Hello World"}


@app.get("/createTable")
async def createTable():
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE stores_DE(
                store_id SERIAL PRIMARY KEY,
                store_city VARCHAR(20) NOT NULL,
                store_email VARCHAR(30) UNIQUE,
                BRAND VARCHAR(10) NOT NULL)
                """
            )
            conn.commit()
        return {"message": "Table created successfully."}

    except psycopg2.errors.DuplicateTable:
        conn.rollback()
        return {"message": "Table already exists."}

    except Exception as e:
        print(e)
        conn.rollback()
        return {"message": "failed due to unknown error."}


@app.get("/items")
async def read_all_item():
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT store_id, store_city, store_email, BRAND "
                "FROM stores_de "
            )
            rows = cur.fetchall()
            conn.commit()
        return [serialize_store(*row) for row in rows]
    except Exception as e:
        print(e)
        conn.rollback()
        return {"message": "failed due to unknown error."}

@app.get("/items/{item_id}")
async def read_item(item_id: int) -> ViewStore:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT store_id, store_city, store_email, BRAND "
            "FROM stores_de "
            f"WHERE store_id={item_id}"
        )
        row = cur.fetchone()
        conn.commit()
    if row:
        return serialize_store(*row)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Item with id: {item_id} not found"
        )


def serialize_store(id, city, email, brand):
    return ViewStore(id=id, city=city, email=email, brand=brand)


@app.post("/add_item")
async def add_item(store: CreateStore):
    city = store.city
    email = store.email
    brand = store.brand

    try:
        with conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO stores_DE(store_city, store_email, BRAND) VALUES('{city}','{email}','{brand}')"
            )
            conn.commit()
        return {"message": "store added successfully."}
    except Exception as e:
        print(e)
        conn.rollback()
        return {"message": "failed due to unknown error."}


@app.post("/delete_item/{item_id}")
async def delete_item(item_id: int):
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM stores_de "
                f"WHERE store_id={item_id}"
            )
            conn.commit()
        return {"message": f"store with store_id {item_id} deleted."}
    except Exception as e:
        conn.rollback()
        print(e)
        return {"message": "failed due to unknown error."}


@app.post("/delete_all")
async def delete_table():
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DROP TABLE stores_de;"
            )
            conn.commit()
        return {
            "message": "All stores deleted. In order to add new items, please create a new table first."
        }
    except Exception as e:
        conn.rollback()
        print(e)
        return {"message": "failed due to unknown error."}

# For testing purposes only.
if __name__ == '__main__':
    host = "0.0.0.0"  # Use the service name as the hostname ("localhost" works)
    port = 5432
    database = "learning_sql"
    user = "sami"
    password = "secret_123"

    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=password,
        connect_timeout=3600,
    )

    print("finished")
