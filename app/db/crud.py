import app.blob_storage as file_maneger

from sqlalchemy.orm import Session
from app.auth import hashing
from fastapi import UploadFile
from . import models, schemas

# User


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, limit: int = 10):
    return db.query(models.User).order_by(None).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    user.senha = hashing.password_hash(user.senha)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {f"User updated successfully"}


def validate_user(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        return False

    if not hashing.verify_password(user.senha, db_user.senha):
        return False

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


# Pet
def get_pet(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()


def get_pets(db: Session, limit: int = 10):
    return db.query(models.Pet).order_by(None).limit(limit).all()


def create_pet(db: Session, nome: str, idade: int, especie: str, raca: str, sexo: str, observacoes: str, foto: str):
    pet = {
        "nome": nome,
        "idade": idade,
        "especie": especie,
        "raca": raca, "sexo": sexo,
        "observacoes": observacoes,
        "foto_url": foto
    }
    db_pet = models.Pet(**pet)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def update_pet(db: Session, pet_id: int, pet: schemas.PetBase):
    db_pet = get_pet(db, pet_id)
    if not db_pet:
        return None

    pet_data = pet.dict(exclude_unset=True)
    for key, value in pet_data.items():
        setattr(db_pet, key, value)

    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet


def delete_pet(db: Session, pet_id: int):
    db_pet = get_pet(db, pet_id)
    if not db_pet:
        return None

    db.delete(db_pet)
    db.commit()
    return db_pet


# File

def upload_file(file: UploadFile) -> bool:
    file_name = file_maneger.generate_uuid() + "." + file.filename.split(".")[-1]
    data = file.file._file
    file_uploaded = file_maneger.upload_file(file_name, data=data)

    if file_uploaded:
        return "https://adoptstorage2.blob.core.windows.net/pets/"+file_name
    else:
        return None
