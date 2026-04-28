from sqlalchemy.orm import Session
from models import User, Category, Item
import schemas


# =========================
# USER
# =========================
def create_user(db: Session, user: schemas.UserCreate) -> User | None:
    """
    Create a new user if email is unique.
    """
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        return None

    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> User | None:
    """
    Get a user by ID.
    """
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user: schemas.UserCreate) -> User | None:
    """
    Update a user's name and email.
    """
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user and existing_user.id != user_id:
        return None

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)
    return db_user


# =========================
# CATEGORY
# =========================
def create_category(db: Session, name: str) -> Category:
    """
    Create a category (no user relation).
    """
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, name: str) -> Category | None:
    """
    Update a category.
    """
    category = db.query(Category).filter(Category.id == category_id).first()

    if not category:
        return None

    category.name = name

    db.commit()
    db.refresh(category)
    return category


# =========================
# ITEM
# =========================
def create_item(db: Session, item: schemas.ItemCreate, category_id: int) -> Item:
    """
    Create an item inside a category.
    """
    db_item = Item(
        name=item.name,
        quantity=item.quantity,
        price=item.price,
        category_id=category_id
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemCreate) -> Item | None:
    """
    Update an item.
    """
    db_item = db.query(Item).filter(Item.id == item_id).first()

    if not db_item:
        return None

    db_item.name = item.name
    db_item.quantity = item.quantity
    db_item.price = item.price

    db.commit()
    db.refresh(db_item)
    return db_item