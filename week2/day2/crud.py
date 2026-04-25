from sqlalchemy.orm import Session
from models import User


#  CREATE
def create_user(db: Session, name: str, email: str):
    """
    Create a new user in the database.

    Args:
        db (Session): Database session.
        name (str): Name of the user.
        email (str): Email of the user.

    Returns:
        User: The newly created user object.
    """
    try:
        user = User(name=name, email=email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
        return None


#  READ (ALL USERS)
def get_users(db: Session):
    """
    Retrieve all users from the database.

    Args:
        db (Session): Database session.

    Returns:
        list: List of all user objects.
    """
    try:
        return db.query(User).all()
    except Exception as e:
        print(f"Error fetching users: {e}")
        return []


#  READ (SINGLE USER)
def get_user(db: Session, user_id: int):
    """
    Retrieve a single user by ID.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user.

    Returns:
        User or None: The user if found, otherwise None.
    """
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None


#  UPDATE
def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    """
    Update an existing user's details.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to update.
        name (str, optional): New name of the user.
        email (str, optional): New email of the user.

    Returns:
        User or None: Updated user if found, otherwise None.
    """
    try:
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

    except Exception as e:
        db.rollback()
        print(f"Error updating user: {e}")
        return None


#  DELETE
def delete_user(db: Session, user_id: int):
    """
    Delete a user from the database.

    Args:
        db (Session): Database session.
        user_id (int): ID of the user to delete.

    Returns:
        User or None: Deleted user if found, otherwise None.
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            return None

        db.delete(user)
        db.commit()
        return user

    except Exception as e:
        db.rollback()
        print(f"Error deleting user: {e}")
        return None