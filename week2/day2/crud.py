from sqlalchemy.orm import Session
from models import User


#  CREATE
def create_user(db: Session, name: str, email: str):
    """
    Create a new user in the database.

    

    Returns:
        User: The newly created user object.
    """
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


#  READ (ALL USERS)
def get_users(db: Session):
    """
    Retrieve all users from the database.

    

    Returns:
        list: List of all user objects.
    """
    return db.query(User).all()


#  READ (SINGLE USER)
def get_user(db: Session, user_id: int):
    """
    Retrieve a single user by ID.

    

    Returns:
        User or None: The user if found, otherwise None.
    """
    return db.query(User).filter(User.id == user_id).first()


#  UPDATE
def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    """
    Update an existing user's details.

    Returns:
        User or None: Updated user if found, otherwise None.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    if name:
        user.name = name
    if email:
        user.email = email

    db.commit()
    db.refresh(user)
    return user


#  DELETE
def delete_user(db: Session, user_id: int):
    """
    Delete a user from the database.


    Returns:
        User or None: Deleted user if found, otherwise None.
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return user