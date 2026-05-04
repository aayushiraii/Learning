from pydantic import BaseModel, Field, EmailStr


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)


class CategoryResponse(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    quantity: int = Field(ge=0)
    price: int = Field(gt=0)


class ItemResponse(ItemCreate):
    id: int
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = {"from_attributes": True}