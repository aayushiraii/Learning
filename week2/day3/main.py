from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



# DB SESSION

def get_db():
    """
    Provides a database session for each request.

    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# USER ROUTES


from sqlalchemy.exc import IntegrityError

@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
    Retrieve all users.

    Args:
        db (Session): Database session

    Returns:
        List[UserResponse]: List of users
    """
    return db.query(models.User).all()


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single user by ID.

    Args:
        user_id (int): ID of the user
        db (Session): Database session

    Returns:
        UserResponse: User object

    Raises:
        HTTPException: If user not found
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Update a user.

    Args:
        user_id (int): ID of the user
        user (UserCreate): Updated user data
        db (Session): Database session

    Returns:
        UserResponse: Updated user

    Raises:
        HTTPException: If user not found
    """
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.

    Args:
        user_id (int): ID of the user
        db (Session): Database session

    Returns:
        dict: Success message
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# CATEGORY ROUTES


@app.post("/users/{user_id}/categories")
def create_category(user_id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a category for a specific user.

    Args:
        user_id (int): Owner user ID
        data (CategoryCreate): Category data
        db (Session): Database session

    Returns:
        Category: Created category
    """
    user = crud.get_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        return crud.create_category(db, data.name, user_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories")
def get_all_categories(db: Session = Depends(get_db)):
    """
    Retrieve all categories.

    Returns:
        List[Category]: List of categories
    """
    return db.query(models.Category).all()


@app.get("/users/{user_id}/categories")
def get_user_categories(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all categories for a specific user.

    Args:
        user_id (int): User ID

    Returns:
        List[Category]: Categories belonging to the user
    """
    return db.query(models.Category).filter(models.Category.owner_id == user_id).all()


@app.put("/categories/{category_id}")
def update_category(category_id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Update a category.

    Args:
        category_id (int): Category ID
        data (CategoryCreate): Updated data

    Returns:
        Category: Updated category
    """
    updated_category = crud.update_category(db, category_id, data.name)

    if not updated_category:
        raise HTTPException(status_code=404, detail="Category not found")

    return updated_category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """
    Delete a category and its items.

    Args:
        category_id (int): Category ID

    Returns:
        dict: Success message
    """
    category = db.query(models.Category).filter(models.Category.id == category_id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    try:
        db.delete(category)
        db.commit()
        return {"message": "Category deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# ITEM ROUTES


@app.post("/categories/{category_id}/items")
def create_item(category_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create an item inside a category.

    Args:
        category_id (int): Category ID
        item (ItemCreate): Item data

    Returns:
        Item: Created item
    """
    try:
        return crud.create_item(db, item, category_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/items")
def get_all_items(db: Session = Depends(get_db)):
    """
    Retrieve all items.

    Returns:
        List[Item]: List of items
    """
    return db.query(models.Item).all()


@app.get("/categories/{category_id}/items")
def get_category_items(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all items in a category.

    Args:
        category_id (int): Category ID

    Returns:
        List[Item]: Items in the category
    """
    return db.query(models.Item).filter(models.Item.category_id == category_id).all()


@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Update an item.

    Args:
        item_id (int): Item ID
        item (ItemCreate): Updated item data

    Returns:
        Item: Updated item
    """
    updated_item = crud.update_item(db, item_id, item)

    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific item.

    Args:
        item_id (int): Item ID

    Returns:
        dict: Success message
    """
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    try:
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

    Returns:
        dict: Number of deleted items
    """
    try:
        deleted = db.query(models.Item).delete()
        db.commit()
        return {"message": f"{deleted} items deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



# JOINED DATA


@app.get("/items/full")
def get_full_items(db: Session = Depends(get_db)):
    """
    Retrieve items along with category and user details.

    Returns:
        List[dict]: Joined data including item, category, user, price, quantity
    """
    return (
        db.query(
            models.Item.name.label("item_name"),
            models.Item.price.label("price"),
            models.Item.quantity.label("quantity"),
            models.Category.name.label("category_name"),
            models.User.name.label("user_name"),
            models.User.email.label("email"),
        )
        .join(models.Category, models.Item.category_id == models.Category.id)
        .join(models.User, models.Category.owner_id == models.User.id)
        .all()
    )