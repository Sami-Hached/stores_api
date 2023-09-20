from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World"

def test_create_store():
    sample_payload = {
        "city": "Test_city",
        "email": "meow_100@test.com",
        "brand": "kitty_cat"
    }

    response = client.post("/add_item", json=sample_payload)
    assert response.status_code == 200
    saved_row = response.json()
    assert saved_row["city"] == "Test_city"
    assert saved_row["email"] == "meow_100@test.com"
    assert saved_row["brand"] == "kitty_cat"
    assert type(saved_row["id"]) == str
