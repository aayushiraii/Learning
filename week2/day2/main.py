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
    try:
        db = SessionLocal()
        yield db
    except Exception as e:
        print(f"DB Session Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")
    finally:
        db.close()


@app.get("/")
def home():
    """
    Root endpoint to verify API is running

    Returns:
        dict: Simple status message.
    """
    try:
        return {"message": "API is running"}
    except Exception as e:
        print(f"Home Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# CREATE
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    """
    Creates a new User
    """
    try:
        user = crud.create_user(db, name, email)
        if not user:
            raise HTTPException(status_code=400, detail="User not created")
        return user
    except Exception as e:
        print(f"Create Error: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")


# READ ALL
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    """
    Reads all the users in the Database
    """
    try:
        return crud.get_users(db)
    except Exception as e:
        print(f"Get Users Error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users")


# READ ONE
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Reads only specific Users with the requested Users Id
    """
    try:
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get User Error: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user")


# UPDATE
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None, db: Session = Depends(get_db)):
    """
    Updates the existing user
    """
    try:
        user = crud.update_user(db, user_id, name, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update Error: {e}")
        raise HTTPException(status_code=500, detail="Error updating user")


# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes the requested user
    """
    try:
        user = crud.delete_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete Error: {e}")
        raise HTTPException(status_code=500, detail="Error deleting user")