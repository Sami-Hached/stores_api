import uuid

import pytest
from src.presentation.api.v1.main import app, get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.infrastructure.database import Base


# TEST_DATABASE_URL = "sqlite://"
#
# engine = create_engine(
#     TEST_DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )
#
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base.metadata.create_all(bind=engine)
#
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
#
#
# app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, world!"


def test_create_store():
    sample_payload = {
        "city": "Test_city",
        "email": "meow_100@test.com",
        "brand": "kitty_cat"
    }

    response = client.post("/add_item", json=sample_payload)
    saved_row = response.json()

    assert response.status_code == 200
    assert saved_row["city"] == "Test_city"
    assert saved_row["email"] == "meow_100@test.com"
    assert saved_row["brand"] == "kitty_cat"
    assert _is_UUID(saved_row["id"])


def test_delete_store(preexisting_store):
    response = client.post(f"/delete_item/{preexisting_store['id']}")
    assert response.status_code == 200
    assert response.json() == f"Store with item_id: {preexisting_store['id']} has been deleted."

@pytest.fixture(autouse=True)
def teardown():
    yield
    client.post("/delete_all")

@pytest.fixture
def preexisting_store():
    store = {
        "city": "test_city",
        "email": "email_unq@test.com",
        "brand": "test_brand",
    }
    response = client.post("/add_item", json=store)
    yield response.json()


def _is_UUID(id):
    try:
        uuid.UUID(id)
    except ValueError:
        return False

    return True
