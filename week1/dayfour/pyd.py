#instead of checking the data manually each and every time, pydantic model does it automatically.
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

user = User(id="1", name="Aayushi")
print(user)

##to fix the error that i made was fixed with naming the file name, directory, /learnings/learning/dayfour/pyd.py 
#circular import error--comes when two or more modules depend on each other at the same time forming loop btw them

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr

user = User(name="Aayushi", email="Aayushi@gmail.com")
print(user)

## email wasnt there so again error-- fixed it with installing email 
#pip install pydantic[email]

from pydantic import BaseModel, EmailStr, field_validator

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

data = {
    "username": "Aayushi12345",
    "email": "Aayushi@gmail.com",
    "password": "secret123"
}

user = UserSignup(**data)
print(user)

from pydantic import BaseModel, EmailStr

class Login(BaseModel):
    email: EmailStr
    password: str

login_data = {
    "email": "Aayushi@gmail.com",
    "password": "mypassword"
}

login = Login(**login_data)
print(login)



