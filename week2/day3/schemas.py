from pydantic import BaseModel, Field, EmailStr


# =========================
# ITEM
# =========================
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


# =========================
# CATEGORY
# =========================
class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# =========================
# USER
# =========================
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