#Parameterised tests are basically single test with multiple times with different inputs

import pytest
import schemas as schemas
from crud import create_user


@pytest.mark.parametrize("value", ["bad", "wrong", "noatsign"])
def test_values(value):
    # simple check
    assert isinstance(value, str)



@pytest.mark.parametrize("name,email", [
    ("Aayushi", "a@test.com"),
    ("John", "john@test.com")
])
def test_create_user(db, name, email):
    # Arrange
    user_data = schemas.UserCreate(name=name, email=email)

    # Act
    user = create_user(db, user_data)

    # Assert
    assert user.email == email



@pytest.mark.parametrize("email", ["bad", "wrong", "noatsign"])
def test_invalid_emails(email):
    with pytest.raises(Exception):   # or ValidationError if you prefer
        schemas.UserCreate(name="Test", email=email)
        