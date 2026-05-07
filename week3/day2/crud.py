from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import User, Category, Item
import schemas as schemas

from auth import hash_password, verify_password


# =========================
# USER CRUD
# =========================

def create_user(db: Session, user: schemas.UserCreate) -> User | None:
    try:
        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user:
            return None

        hashed_password = hash_password(user.password)

        db_user = User(
            name=user.name,
            email=user.email,
            password=hashed_password,
            role=user.role
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except IntegrityError:
        db.rollback()
        return None

    except Exception as e:
        db.rollback()
        raise e


def get_user(db: Session, user_id: int) -> User | None:
    try:
        return db.query(User).filter(
            User.id == user_id
        ).first()

    except Exception as e:
        raise e


def get_all_users(db: Session):
    try:
        return db.query(User).all()

    except Exception as e:
        raise e


def authenticate_user(
    db: Session,
    email: str,
    password: str
) -> User | None:
    try:
        user = db.query(User).filter(
            User.email == email
        ).first()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user

    except Exception as e:
        raise e


def update_user(
    db: Session,
    user_id: int,
    user: schemas.UserCreate
) -> User | None:

    try:
        db_user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not db_user:
            return None

        existing_user = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing_user and existing_user.id != user_id:
            return None

        db_user.name = user.name
        db_user.email = user.email
        db_user.role = user.role

        if user.password:
            db_user.password = hash_password(user.password)

        db.commit()
        db.refresh(db_user)

        return db_user

    except Exception as e:
        db.rollback()
        raise e


def delete_user(db: Session, user_id: int) -> bool:
    try:
        db_user = db.query(User).filter(
            User.id == user_id
        ).first()

        if not db_user:
            return False

        db.delete(db_user)
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise e


# =========================
# CATEGORY CRUD
# =========================

def create_category(db: Session, name: str):
    try:
        existing = db.query(Category).filter(
            Category.name == name
        ).first()

        if existing:
            return None

        category = Category(name=name)

        db.add(category)
        db.commit()
        db.refresh(category)

        return category

    except Exception as e:
        db.rollback()
        raise e


def get_category(db: Session, category_id: int):
    try:
        return db.query(Category).filter(
            Category.id == category_id
        ).first()

    except Exception as e:
        raise e


def get_all_categories(db: Session):
    try:
        return db.query(Category).all()

    except Exception as e:
        raise e


def update_category(
    db: Session,
    category_id: int,
    name: str
):
    try:
        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            return None

        existing = db.query(Category).filter(
            Category.name == name
        ).first()

        if existing and existing.id != category_id:
            return None

        category.name = name

        db.commit()
        db.refresh(category)

        return category

    except Exception as e:
        db.rollback()
        raise e


def delete_category(db: Session, category_id: int):
    try:
        category = db.query(Category).filter(
            Category.id == category_id
        ).first()

        if not category:
            return False

        db.delete(category)
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise e


# =========================
# ITEM CRUD
# =========================

def create_item(
    db: Session,
    item: schemas.ItemCreate,
    category_id: int
):
    try:
        item_name = item.name.strip().lower()

        existing = db.query(Item).filter(
            Item.name == item_name,
            Item.category_id == category_id
        ).first()

        if existing:
            return None

        db_item = Item(
            name=item_name,
            quantity=item.quantity,
            price=item.price,
            category_id=category_id
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        return db_item

    except Exception as e:
        db.rollback()
        raise e


def get_item(db: Session, item_id: int):
    try:
        return db.query(Item).filter(
            Item.id == item_id
        ).first()

    except Exception as e:
        raise e


def get_all_items(db: Session):
    try:
        return db.query(Item).all()

    except Exception as e:
        raise e


def update_item(
    db: Session,
    item_id: int,
    item: schemas.ItemCreate
):
    try:
        db_item = db.query(Item).filter(
            Item.id == item_id
        ).first()

        if not db_item:
            return None

        db_item.name = item.name.strip().lower()
        db_item.quantity = item.quantity
        db_item.price = item.price

        db.commit()
        db.refresh(db_item)

        return db_item

    except Exception as e:
        db.rollback()
        raise e


def delete_item(db: Session, item_id: int):
    try:
        db_item = db.query(Item).filter(
            Item.id == item_id
        ).first()

        if not db_item:
            return False

        db.delete(db_item)
        db.commit()

        return True

    except Exception as e:
        db.rollback()
        raise e