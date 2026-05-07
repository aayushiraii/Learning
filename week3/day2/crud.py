from sqlalchemy.orm import Session
from models import User, Category, Item
import schemas as schemas
from auth import hash_password, verify_password


# USER
def create_user(db: Session, user: schemas.UserCreate) -> User | None:
    existing_user = db.query(User).filter(User.email == user.email).first()

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


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def update_user(db: Session, user_id: int, user: schemas.UserCreate) -> User | None:
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return None

    existing_user = db.query(User).filter(User.email == user.email).first()
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


# CATEGORY
def create_category(db: Session, name: str):
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        return None

    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# ITEM
def create_item(db: Session, item: schemas.ItemCreate, category_id: int):
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