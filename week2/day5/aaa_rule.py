import pytest
import schemas as schemas
from crud import create_user, create_category, create_item, get_user, update_user
from tests.testing import TestingSessionLocal
from fastapi.testclient import TestClient
from main import app, get_db
from pydantic import ValidationError
from tests.testing import DATABASE_URL


#FIXTURES 
@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# USER CRUD 

def test_create_user_duplicate_email(db):
    # Arrange
    data = schemas.UserCreate(name="Aayushi", email="dup@test.com")

    # Act
    create_user(db, data)
    user2 = create_user(db, data)

    # Assert
    assert user2 is None





#  CATEGORY + ITEM


def test_create_duplicate_category(db):
    # Arrange
    name = "Books"

    # Act
    create_category(db, name)
    duplicate = create_category(db, name)

    # Assert
    assert duplicate is None


#  SCHEMA TESTS 

def test_user_invalid_email():
    # Arrange + Act + Assert
    with pytest.raises(ValidationError):
        schemas.UserCreate(name="Test", email="bad")


def test_category_empty_name():
    # Arrange + Act + Assert
    with pytest.raises(ValidationError):
        schemas.CategoryCreate(name="")


def test_item_invalid_quantity():
    # Arrange + Act + Assert
    with pytest.raises(ValidationError):
        schemas.ItemCreate(name="Phone", quantity=-1, price=100)


#API TESTS 




def test_create_user_duplicate_api(client):
    # Arrange
    user = {"name": "Test", "email": "dup@test.com"}

    # Act
    client.post("/users", json=user)
    res = client.post("/users", json=user)

    # Assert
    assert res.status_code != 200


def test_delete_user_api(client):
    # Arrange
    create = client.post("/users", json={
        "name": "Delete",
        "email": "delete@test.com"
    })
    user_id = create.json()["id"]

    # Act
    response = client.delete(f"/users/{user_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"



def test_get_all_users_api(client):
    # Arrange
    client.post("/users", json={
        "name": "User1",
        "email": "u1@test.com"
    })

    # Act
    res = client.get("/users")

    # Assert
    assert res.status_code == 200
    assert len(res.json()) >= 1

 #SIMPLE TEST 

def add(a, b):
    return a + b


def test_add():
    # Arrange
    a, b = 2, 3

    # Act
    result = add(a, b)

    # Assert
    assert result == 5
    
    
