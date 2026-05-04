from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

import models as models, schemas as schemas, crud as crud
from database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# =========================
# DB SESSION
# =========================

# @app.get("/")
# def home():
#     return {"message": "API is running"}


def get_db():
    """
    Provide a database session for each request.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# USER ROUTES
# =========================
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (UserCreate): Input user data (name, email)
        db (Session): Database session

    Returns:
        UserResponse: The created user object

    Raises:
        HTTPException: If email already exists or any server error occurs
    """
    try:
        new_user = crud.create_user(db, user)

        if not new_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.

    Args:
        db (Session): Database session

    Returns:
        List[UserResponse]: List of all users

    Raises:
        HTTPException: If a server error occurs
    """
    try:
        return db.query(models.User).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.

    Args:
        user_id (int): ID of the user
        db (Session): Database session

    Returns:
        UserResponse: User details

    Raises:
        HTTPException: If user is not found or error occurs
    """
    try:
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Update an existing user.

    Args:
        user_id (int): ID of the user to update
        user (UserCreate): Updated user data
        db (Session): Database session

    Returns:
        UserResponse: Updated user object

    Raises:
        HTTPException: If user not found or error occurs
    """
    try:
        updated_user = crud.update_user(db, user_id, user)

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        return updated_user

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
  

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.

    Args:
        user_id (int): ID of the user to delete
        db (Session): Database session

    Returns:
        dict: Confirmation message

    Raises:
        HTTPException: If user not found or error occurs
    """
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()

        return {"message": "User deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# CATEGORY ROUTES
# =========================
@app.post("/categories")
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.
    """
    try:
        category = crud.create_category(db, data.name)

        if not category:
            raise HTTPException(status_code=400, detail="Category already exists")

        return category

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    Args:
        db (Session): Database session

    Returns:
        List[Category]: List of categories

    Raises:
        HTTPException: If an error occurs
    """
    try:
        return db.query(models.Category).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/categories/{category_id}")
def update_category(category_id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Update a category.

    Args:
        category_id (int): ID of the category
        data (CategoryCreate): Updated data
        db (Session): Database session

    Returns:
        Category: Updated category object

    Raises:
        HTTPException: If category not found or error occurs
    """
    try:
        updated_category = crud.update_category(db, category_id, data.name)

        if not updated_category:
            raise HTTPException(status_code=404, detail="Category not found")

        return updated_category

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category.

    Args:
        category_id (int): ID of the category
        db (Session): Database session

    Returns:
        dict: Confirmation message

    Raises:
        HTTPException: If category not found or error occurs
    """
    try:
        category = db.query(models.Category).filter(
            models.Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        db.delete(category)
        db.commit()

        return {"message": "Category deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ITEM ROUTES
# =========================
@app.post("/categories/{category_id}/items")
def create_item(category_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item in a category.
    """
    try:
        # check if category exists
        category = db.query(models.Category).filter(
            models.Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        # create item
        new_item = crud.create_item(db, item, category_id)

        # check duplicate
        if not new_item:
            raise HTTPException(status_code=400, detail="Item already exists")

        return new_item

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    """
    Retrieve all items.

    Args:
        db (Session): Database session

    Returns:
        List[Item]: List of items

    Raises:
        HTTPException: If an error occurs
    """
    try:
        return db.query(models.Item).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories/{category_id}/items")
def get_category_items(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve items in a specific category.

    Args:
        category_id (int): Category ID
        db (Session): Database session

    Returns:
        List[Item]: Items in the category

    Raises:
        HTTPException: If category not found or error occurs
    """
    try:
        category = db.query(models.Category).filter(
            models.Category.id == category_id
        ).first()

        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        return db.query(models.Item).filter(
            models.Item.category_id == category_id
        ).all()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Update an item.

    Args:
        item_id (int): Item ID
        item (ItemCreate): Updated item data
        db (Session): Database session

    Returns:
        Item: Updated item object

    Raises:
        HTTPException: If item not found or error occurs
    """
    try:
        updated_item = crud.update_item(db, item_id, item)

        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")

        return updated_item

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item.

    Args:
        item_id (int): Item ID
        db (Session): Database session

    Returns:
        dict: Confirmation message

    Raises:
        HTTPException: If item not found or error occurs
    """
    try:
        item = db.query(models.Item).filter(models.Item.id == item_id).first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        db.delete(item)
        db.commit()

        return {"message": "Item deleted"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/items")
def delete_all_items(db: Session = Depends(get_db)):
    """
    Delete all items from the database.

    Args:
        db (Session): Database session

    Returns:
        dict: Number of deleted items

    Raises:
        HTTPException: If an error occurs
    """
    try:
        deleted = db.query(models.Item).delete()
        db.commit()
        return {"message": f"{deleted} items deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/health")
def health():
    return {"status": "ok"}