from pydantic import BaseModel, EmailStr, Field

# USER
class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=4)
    role: str = "staff"  

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str  

    model_config = {"from_attributes": True}


# CATEGORY
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)

class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


# ITEM
class ItemCreate(BaseModel):
    name: str = Field(min_length=2)
    quantity: int = Field(ge=0)
    price: int = Field(gt=0)

class ItemResponse(ItemCreate):
    id: int

    model_config = {"from_attributes": True}


class RefreshRequest(BaseModel):
    refresh_token: str