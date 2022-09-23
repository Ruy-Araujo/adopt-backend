from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, limit: int = 10):
    return db.query(models.User).order_by(None).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.senha+"notreallyhashed"
    user = user.dict()
    user.update({"senha": fake_hashed_password})
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {f"User created successfully {db_user}"}
