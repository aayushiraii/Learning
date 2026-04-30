from pydantic import BaseModel, Field, EmailStr
from pydantic import Field

class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)

#items
class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    quantity: int = Field(ge=0)
    price: int = Field(gt=0)

class ItemUpdate(BaseModel):
    name: str
    quantity: int
    price: int


class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True


#category
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)



class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


#user
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True