from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models, schemas, crud
from database import engine, get_db

from auth import (
    create_access_token,
    create_refresh_token,
    decode_token
)

from pydantic import BaseModel

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Full App")
#auth 


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        scheme, token = authorization.split()

        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid auth scheme")

        payload = decode_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Wrong token type")

        return payload["sub"]

    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")


#user
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = crud.create_user(db, user)

        if not new_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


#login
@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = crud.authenticate_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


#refresh
class RefreshRequest(BaseModel):
    refresh_token: str


@app.post("/refresh")
def refresh_token(payload: RefreshRequest):

    data = decode_token(payload.refresh_token)

    if not data:
        raise HTTPException(status_code=401, detail="Invalid token")

    if data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Not refresh token")

    email = data.get("sub")

    new_access_token = create_access_token({"sub": email})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


#users
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(models.User).all()


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_user = crud.update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}


#category
@app.post("/categories")
def create_category(
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    category = crud.create_category(db, data.name)

    if not category:
        raise HTTPException(status_code=400, detail="Category exists")

    return category


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


@app.put("/categories/{category_id}")
def update_category(
    category_id: int,
    data: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    updated = crud.update_category(db, category_id, data.name)

    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()

    return {"message": "Category deleted"}


#items
@app.post("/categories/{category_id}/items")
def create_item(
    category_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_item = crud.create_item(db, item, category_id)

    if not new_item:
        raise HTTPException(status_code=400, detail="Item exists")

    return new_item


@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()


@app.get("/categories/{category_id}/items")
def get_category_items(category_id: int, db: Session = Depends(get_db)):
    return db.query(models.Item).filter(models.Item.category_id == category_id).all()


@app.put("/items/{item_id}")
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    updated = crud.update_item(db, item_id, item)

    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated


@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted"}