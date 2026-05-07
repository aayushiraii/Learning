from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models as models, schemas as schemas, crud as crud
from database import engine, get_db
from auth import (
    create_access_token,
    create_refresh_token,
    verify_token_type,
    SECRET_KEY,
    ALGORITHM
)
from jose import jwt, ExpiredSignatureError, JWTError

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Full App")


# =========================
# AUTH DEPENDENCIES
# =========================

def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid scheme")

        payload = verify_token_type(token, "access")
        return payload  # ✅ returns role also

    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")


def require_role(allowed_roles: list):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return role_checker


# =========================
# AUTH
# =========================

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role  
    })

    refresh_token = create_refresh_token({
        "sub": db_user.email,
        "role": db_user.role  
    })

    return {
        "access_token": access_token,
        # "refresh_token": refresh_token
    }


@app.post("/verify-and-refresh")
def verify_and_refresh(data: schemas.RefreshRequest):
    try:
        jwt.decode(data.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        payload = verify_token_type(data.refresh_token, "refresh")

        new_access_token = create_access_token({
            "sub": payload.get("sub"),
            "role": payload.get("role")  
        })

        return {
            "status": "refreshed",
            "new_access_token": new_access_token
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Session expired")


# =========================
# USERS
# =========================

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.create_user(db, user)
    if not new_user:
        raise HTTPException(status_code=400, detail="Email exists")
    return new_user


@app.get("/users")
def get_users(db: Session = Depends(get_db), user=Depends(require_role(["admin"]))):
    return db.query(models.User).all()


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(require_role(["admin"]))):
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
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db),
                    user=Depends(require_role(["admin", "manager"]))):
    category = crud.create_category(db, data.name)
    if not category:
        raise HTTPException(status_code=400, detail="Category exists")
    return category


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()


# =========================
# ITEMS
# =========================

@app.post("/categories/{category_id}/items")
def create_item(category_id: int, item: schemas.ItemCreate,
                db: Session = Depends(get_db),
                user=Depends(require_role(["admin", "manager"]))):
    return crud.create_item(db, item, category_id)


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db),
                user=Depends(require_role(["admin"]))):
    item_obj = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item_obj)
    db.commit()
    return {"message": "Item deleted"}