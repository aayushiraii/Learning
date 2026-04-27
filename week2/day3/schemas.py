from pydantic import BaseModel, Field,EmailStr


# ITEM 
class ItemCreate(BaseModel):
    name: str
    quantity: int
    price: int


class ItemUpdate(BaseModel):
    name: str
    quantity: int
    price: int


class ItemResponse(ItemCreate):
    id: int

    class Config:
        from_attributes = True


# CATEGORY 
class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(CategoryCreate):
    id: int
    items: list[ItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


# USER 
class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr


class UserUpdate(BaseModel):
    name: str


class UserResponse(UserCreate):
    id: int
    categories: list[CategoryResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True