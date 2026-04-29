import pytest
import schemas
from crud import create_user, create_category, create_item, get_user, update_user
from tests.testing import engine
from models import Base
from fastapi.testclient import TestClient
from main import app
from pydantic import ValidationError




client = TestClient(app)


# ------------------ USER CRUD ------------------

def test_create_user(db):
    user = create_user(db, schemas.UserCreate(
        name="Aayushi",
        email="a@test.com"
    ))
    assert user is not None


def test_create_user_duplicate_email(db):
    data = schemas.UserCreate(name="Aayushi", email="dup@test.com")

    assert create_user(db, data) is not None
    assert create_user(db, data) is None


def test_get_user(db):
    created = create_user(db, schemas.UserCreate(
        name="Test",
        email="get@test.com"
    ))

    fetched = get_user(db, created.id)

    assert fetched is not None
    assert fetched.id == created.id


def test_update_user_success(db):
    user = create_user(db, schemas.UserCreate(
        name="Old",
        email="old@test.com"
    ))

    updated = update_user(db, user.id, schemas.UserCreate(
        name="New",
        email="new@test.com"
    ))

    assert updated.name == "New"


# ------------------ CATEGORY + ITEM ------------------

def test_create_category(db):
    category = create_category(db, "Electronics")
    assert category is not None


def test_create_duplicate_category(db):
    create_category(db, "Books")
    assert create_category(db, "Books") is None


def test_create_item(db):
    cat = create_category(db, "Electronics")

    item = create_item(db, schemas.ItemCreate(
        name=" Phone ",
        quantity=2,
        price=1000
    ), cat.id)

    assert item.name == "phone"


def test_create_duplicate_item_same_category(db):
    cat = create_category(db, "Electronics")

    data = schemas.ItemCreate(name="Laptop", quantity=1, price=2000)

    create_item(db, data, cat.id)
    assert create_item(db, data, cat.id) is None


# ------------------ SCHEMA TESTS ------------------

def test_user_invalid_email():
    with pytest.raises(ValidationError):
        schemas.UserCreate(name="Test", email="bad")


def test_category_empty_name():
    with pytest.raises(ValidationError):
        schemas.CategoryCreate(name="")


def test_item_invalid_quantity():
    with pytest.raises(ValidationError):
        schemas.ItemCreate(name="Phone", quantity=-1, price=100)


# ------------------ API TESTS ------------------

def test_home():
    res = client.get("/")
    assert res.status_code == 200


def test_create_user_api():
    res = client.post("/users", json={
        "name": "API",
        "email": "api@test.com"
    })
    assert res.status_code == 200


def test_create_user_duplicate_api():
    user = {"name": "Test", "email": "dup@test.com"}

    client.post("/users", json=user)
    res = client.post("/users", json=user)

    assert res.status_code != 200


def test_get_user_api():
    create = client.post("/users", json={
        "name": "Fetch",
        "email": "fetch@test.com"
    })

    user_id = create.json()["id"]

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200


def test_create_category_api():
    res = client.post("/categories", json={"name": "Electronics"})
    assert res.status_code == 200


def test_create_item_api():
    cat = client.post("/categories", json={"name": "Electronics"})
    cat_id = cat.json()["id"]

    res = client.post(
        f"/categories/{cat_id}/items",
        json={
            "name": "Phone",
            "quantity": 1,
            "price": 1000
        }
    )

    assert res.status_code == 200
    assert res.json()["name"] == "phone"


def test_delete_user_api():
    create = client.post("/users", json={
        "name": "Delete",
        "email": "delete@test.com"
    })

    user_id = create.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"


def test_get_items_by_category_api():
    cat = client.post("/categories", json={"name": "Electronics"})
    cat_id = cat.json()["id"]

    client.post(f"/categories/{cat_id}/items", json={
        "name": "Laptop",
        "quantity": 1,
        "price": 2000
    })

    response = client.get(f"/categories/{cat_id}/items")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_users_api():
    client.post("/users", json={
        "name": "User1",
        "email": "u1@test.com"
    })

    res = client.get("/users")

    assert res.status_code == 200
    assert len(res.json()) >= 1


def test_delete_all_items():
    cat = client.post("/categories", json={"name": "Electronics"})
    cat_id = cat.json()["id"]

    client.post(f"/categories/{cat_id}/items", json={
        "name": "Phone",
        "quantity": 1,
        "price": 1000
    })

    res = client.delete("/items")

    assert res.status_code == 200
    assert "items deleted" in res.json()["message"]


# ------------------ SIMPLE TEST ------------------

def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5