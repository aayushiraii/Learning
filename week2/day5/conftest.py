import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from tests.testing import TestingSessionLocal

#  DB FIXTURE 
@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#CLIENT FIXTURE 
@pytest.fixture()
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# REUSABLE DATA
@pytest.fixture()
def user_data():
    return {
        "name": "Aayushi",
        "email": "a@test.com"
    }

@pytest.fixture()
def item_data():
    return {
        "name": "Phone",
        "quantity": 1,
        "price": 1000
    }