from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "API is running"}


# CREATE
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    return crud.create_user(db, name, email)


# READ ALL
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


# READ ONE
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# UPDATE
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, name, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}