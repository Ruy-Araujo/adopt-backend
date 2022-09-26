
from fastapi import FastAPI, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import List, Union

from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from app.libs import load_metadata
from app.models import PetSchema
from app.db import crud, schemas
from app.db.database import SessionLocal

pets = []  # Lista provisoria de pets deve ser substituida por um banco de dados
pet_id = 1
metadata = load_metadata()

app = FastAPI(
    title=metadata["title"],
    description=metadata["description"],
    version=metadata["version"],
    contact=metadata["contact"],
    license_info=metadata["license_info"],
    openapi_tags=metadata["tags"]
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
async def main():
    response = RedirectResponse(url='/docs')
    return response


###################
# Pet endpoints
###################

@app.post("/pet/register", tags=["pet"])
def register_pet(pet: PetSchema):
    # Adicionar local de registro em banco
    global pet_id
    pet.id = pet_id
    pet_id += 1
    pets.append(pet)
    return {"message": "Pet registered successfully!"}


@app.get("/pets", tags=["pet"])
def list_pets():
    # Adicionar logica de busca no banco
    return pets


@app.get("/pet/{id}", tags=["pet"])
def get_pet(id: int):
    # Adicionar local de registro em banco
    for pet in pets:
        if pet.id == id:
            return pet
        else:
            return {"error": "Pet not found"}


@app.put("/pet/{id}", tags=["pet"])
def update_pet(id: int, pet: PetSchema = Body(default=None)):
    for i, item in enumerate(pets):
        if item.id == id:
            temp = pets.pop(i)
            temp = pet
            pets.append(temp)
            return {"message": "Pet updated successfully!"}
    else:
        return {
            "error": "Pet not found"
        }


@app.delete("/pet/{id}", tags=["pet"])
def delete_pet(id: int):
    global pets
    for i, pet in enumerate(pets):
        if pet.id == id:
            pets.pop(i)
            return {'message': f'Pet deleted successfully'}
    else:
        return {
            "error": "User not found"
        }


##################
# Login
##################

@app.post("/users/login", tags=["access"])
def user_login(user: schemas.UserLogin = Body(default=None), db: Session = Depends(get_db)):
    if crud.validate_user(db, user):
        return {
            "success": True,
            "access_token": signJWT(user.email)
        }
    else:
        raise HTTPException(status_code=401, detail={"success": False, "error": "Wrong credentials"})


##################
# Users Endpoints #
##################


@app.post("/user/register", tags=["user"], response_model=schemas.User)
async def user_register(user: schemas.UserCreate = Body(default=None), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Email already registered"})

    db_user = crud.create_user(db=db, user=user)

    if db_user:
        return db_user


@app.get("/users", tags=["user"], response_model=List[schemas.User], dependencies=[Depends(jwtBearer())])
async def list_users(limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, limit)
    return users


@app.get("/user/{id}", tags=["user"], response_model=schemas.User, dependencies=[Depends(jwtBearer())])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "User not found"})


@app.patch("/user/{id}", tags=["user"], dependencies=[Depends(jwtBearer())])
async def update_user(id: int, user: schemas.UserUpdate = Body(default=None),  db: Session = Depends(get_db)):
    db_user = crud.update_user(db, id, user)
    if db_user:
        return db_user
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "User not found"})


@app.delete("/user/{id}", tags=["user"], dependencies=[Depends(jwtBearer())])
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, id)

    if db_user:
        return {"success": True, 'message': 'User deleted successfully'}
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "User not found"})
