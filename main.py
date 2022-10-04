
from fastapi import FastAPI, Body, Depends, HTTPException, UploadFile, Form, File
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from typing import List, Union

from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from app.libs import load_metadata
from app.db import crud, schemas
from app.db.database import SessionLocal


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


##################
# Login
##################

@app.post("/login", tags=["access"], response_model=schemas.UserResponse[schemas.User])
def user_login(user: schemas.UserLogin = Body(default=None), db: Session = Depends(get_db)):
    db_user = crud.validate_user(db, user)
    if db_user:
        return schemas.UserResponse[schemas.User](success=True, content=db_user, access_token=signJWT(user.email), expires=1440)
    else:
        raise HTTPException(status_code=401, detail={"success": False, "error": "Wrong credentials"})


##################
# Users Endpoints #
##################


@app.post("/user/register", tags=["user"], response_model=schemas.UserResponse[schemas.User], dependencies=[Depends(jwtBearer())])
async def user_register(user: schemas.UserCreate = Body(default=None), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Email already registered"})

    db_user = crud.create_user(db=db, user=user)

    if db_user:
        return schemas.UserResponse[schemas.User](success=True, content=db_user, access_token=signJWT(user.email), expires=1440)


@app.get("/users", tags=["user"], response_model=schemas.BaseResponse[List[schemas.User]], dependencies=[Depends(jwtBearer())])
async def list_users(limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, limit)
    return schemas.BaseResponse[List[schemas.User]](success=True, content=users)


@app.get("/user/{id}", tags=["user"], response_model=schemas.BaseResponse[schemas.User], dependencies=[Depends(jwtBearer())])
async def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, id)
    if user:
        return schemas.BaseResponse[schemas.User](success=True, content=user, message="User found")
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "User not found"})


@app.patch("/user/{id}", tags=["user"], response_model=schemas.BaseResponse[schemas.User], dependencies=[Depends(jwtBearer())])
async def update_user(id: int, user: schemas.UserUpdate = Body(default=None),  db: Session = Depends(get_db)):
    db_user = crud.update_user(db, id, user)
    if db_user:
        return schemas.BaseResponse[schemas.User](success=True, content=db_user)
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "User not found"})


@app.delete("/user/{id}", tags=["user"], response_model=schemas.BaseResponse[schemas.User], dependencies=[Depends(jwtBearer())])
async def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, id)

    if db_user:
        return schemas.BaseResponse[schemas.User](success=True, content=db_user)
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "User not found"})

###################
# Pet endpoints
###################


@app.post("/pet/register", tags=["pet"], response_model=schemas.BaseResponse[schemas.Pet], dependencies=[Depends(jwtBearer())])
def register_pet(nome: str = Form(example="Fido"),
                 idade: int = Form(...),
                 especie: str = Form(...),
                 raca: str = Form(...),
                 sexo: str = Form(...),
                 observacoes: str = Form(...),
                 foto: UploadFile = File(..., media_type="image/jpeg"),
                 db: Session = Depends(get_db)):

    if foto.content_type != "image/jpeg":
        raise HTTPException(status_code=400, detail={"success": False, "message": "Image must be in JPEG format"})

    foto_url = crud.upload_file(foto)
    if not foto_url:
        raise HTTPException(status_code=400, detail={"success": False, "message": "Error uploading file"})

    db_pet = crud.create_pet(db, nome, idade, especie, raca, sexo, observacoes, foto_url)

    if db_pet:
        return schemas.BaseResponse[schemas.Pet](success=True, content=db_pet)


@app.get("/pets", tags=["pet"], response_model=schemas.BaseResponse[List[schemas.Pet]])
def list_pets(limit: int = 10, db: Session = Depends(get_db)):
    pets = crud.get_pets(db, limit)
    return schemas.BaseResponse[List[schemas.Pet]](success=True, content=pets)


@app.get("/pet/{id}", tags=["pet"], response_model=schemas.BaseResponse[schemas.Pet])
def get_pet(id: int, db: Session = Depends(get_db)):
    db_pet = crud.get_pet(db, id)
    if db_pet:
        return schemas.BaseResponse[schemas.Pet](success=True, content=db_pet)
    raise HTTPException(status_code=404, detail={"success": False, "message": "Pet not found"})


@app.patch("/pet/{id}", tags=["pet"], response_model=schemas.BaseResponse[schemas.Pet], dependencies=[Depends(jwtBearer())])
def update_pet(id: int, pet: schemas.UpdatePet = Body(default=None), db: Session = Depends(get_db)):
    db_pet = crud.update_pet(db, id, pet)
    if db_pet:
        return schemas.BaseResponse[schemas.Pet](success=True, content=db_pet)
    raise HTTPException(status_code=404, detail={"success": False, "message": "Pet not found"})


@app.delete("/pet/{id}", tags=["pet"], response_model=schemas.BaseResponse[schemas.Pet], dependencies=[Depends(jwtBearer())])
def delete_pet(id: int, db: Session = Depends(get_db)):
    db_pet = crud.delete_pet(db, id)
    if db_pet:
        return schemas.BaseResponse[schemas.Pet](success=True, content=db_pet)
    else:
        raise HTTPException(status_code=404, detail={"success": False, "message": "Pet not found"})
