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
    """
    Root endpoint to verify API is running

    Returns:
        dict: Simple status message.
    """
    return {"message": "API is running"}


# CREATE
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    """
    Creates a new User

    Args:
        name (str): Name of the user.
        email (str): Email of the user.
        db (Session): Database session dependency.

    Returns:
        The new user that has been added
    """
    return crud.create_user(db, name, email)


# READ ALL
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    """
    Reads all the users in the Database

    Args:
        db (Session): Database session dependency.

    Returns:
        Gives all the users
    """
    return crud.get_users(db)


# READ ONE
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Reads only specific Users with the requested Users Id

    Args:
        user_id (int): ID of the user to retrieve.
        db (Session): Database session dependency.

    Returns:
        The requested user Id
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# UPDATE
@app.put("/users/{user_id}")
def update_user(user_id: int, name: str = None, email: str = None, db: Session = Depends(get_db)):
    """
    Updates the existing user

    Args:
        user_id (int): ID of the user to update.
        name (str, optional): New name of the user.
        email (str, optional): New email of the user.
        db (Session): Database session dependency.

    Returns:
        The updated user in place of the previous user
    """
    user = crud.update_user(db, user_id, name, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# DELETE
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes the requested user

    Args:
        user_id (int): ID of the user to delete.
        db (Session): Database session dependency.

    Returns:
        User deleted message
    """
    user = crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}