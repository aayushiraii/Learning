import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db
from models import Base, User, Category, Item
from tests.testing import DATABASE_URL


# ✅ Use your Postgres DB
engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ✅ Create tables once
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# ✅ Transaction per test (safe rollback)
@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


# ✅ Override FastAPI DB
@pytest.fixture(autouse=True)
def override_db(db):
    def _override():
        yield db

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()


# ✅ CLEAN DB BEFORE EACH TEST
@pytest.fixture(autouse=True)
def clean_db(db):
    db.query(Item).delete()
    db.query(Category).delete()
    db.query(User).delete()
    db.commit()