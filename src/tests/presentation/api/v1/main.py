import uuid

import pytest
import os
from fastapi.testclient import TestClient

from src.presentation.api.v1.main import app, get_db
from src.infrastructure.database import get_session, get_engine
from src.infrastructure import models


test_config = {
        "user": os.environ["TEST_DB_USER"],
        "password": os.environ["TEST_DB_PASSWORD"],
        "host": os.environ["TEST_DB_HOST"],
        "port": os.environ["TEST_DB_PORT"],
        "database": os.environ["TEST_DB_DATABASE"],
    }

def override_get_db():
    try:
        session = get_session(test_config)
        db = session()
        yield db
    finally:
        db.close()

# for api methods to access the test database instead of the main one
app.dependency_overrides[get_db] = override_get_db

# create tables within the test database
models.Base.metadata.create_all(bind=get_engine(test_config))

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
