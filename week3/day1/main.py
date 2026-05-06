from fastapi import FastAPI, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel
import models, schemas, crud
from database import engine, get_db
from auth import (
    create_access_token, 
    create_refresh_token, 
    verify_token_type, 
    SECRET_KEY, 
    ALGORITHM
)
from jose import jwt, ExpiredSignatureError, JWTError

# Initialize Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Full App")

# --- Schema for the Refresh Logic ---
class TokenCheckRequest(BaseModel):
    access_token: str
    refresh_token: str

# --- Auth Dependency (Protects your routes) ---
def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid scheme")
        
        payload = verify_token_type(token, "access")
        return payload["sub"]

    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")

# =========================
# AUTH & SESSION LOGIC
# =========================

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})
    
    # We still create it, but we don't HAVE to return it if you don't want to
    # refresh_token = create_refresh_token({"sub": db_user.email})

    return {
        "access_token": access_token
        # "refresh_token": refresh_token  <-- Removing this line stops it from showing up
    }

@app.post("/verify-and-refresh")
def verify_and_refresh(data: TokenCheckRequest):
    """
    Checks if JWT is valid. If expired, uses refresh token to 
    automatically provide a new access token.
    """
    try:
        # 1. Check if Access Token is still valid
        jwt.decode(data.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"status": "valid", "new_access_token": None}

    except ExpiredSignatureError:
        # 2. If Expired, attempt to use the Refresh Token
        try:
            payload = verify_token_type(data.refresh_token, "refresh")
            new_access_token = create_access_token({"sub": payload.get("sub")})
            return {
                "status": "refreshed",
                "new_access_token": new_access_token
            }
        except Exception:
            raise HTTPException(status_code=401, detail="Session expired. Please login again.")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid access token")

# =========================
# USERS
# =========================

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

@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.User).all()

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    user_obj = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user_obj)
    db.commit()
    return {"message": "User deleted"}

# =========================
# CATEGORIES
# =========================

@app.post("/categories")
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    category = crud.create_category(db, data.name)
    if not category:
        raise HTTPException(status_code=400, detail="Category exists")
    return category

@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@app.put("/categories/{category_id}")
def update_category(category_id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = crud.update_category(db, category_id, data.name)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    cat = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return {"message": "Category deleted"}

# =========================
# ITEMS
# =========================

@app.post("/categories/{category_id}/items")
def create_item(category_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
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
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = crud.update_item(db, item_id, item)
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item_obj = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item_obj)
    db.commit()
    return {"message": "Item deleted"}

@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"message": f"Hello {user}, you are authorized"}