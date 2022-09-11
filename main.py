from fastapi import FastAPI, Body, Depends
from app.auth.jwt_handler import signJWT
from app.models import PetSchema, UserSchema, UserLoginSchema
from app.libs import load_metadata
from app.auth.jwt_bearer import jwtBearer

pets = []  # Lista provisoria de pets deve ser substituida por um banco de dados
users = []  # Lista provisorio de usuarios deve ser substituida por um banco de dados
metadata = load_metadata()

app = FastAPI(
    title=metadata["title"],
    description=metadata["description"],
    version=metadata["version"],
    contact=metadata["contact"],
    license_info=metadata["license_info"],
    openapi_tags=metadata["tags"]
)


@app.get("/pets", tags=["pets"])
def get_all_pets():
    # Adicionar logica de busca no banco
    return pets


@app.get("/pets/{id}", tags=["pets"])
def get_pet(id: int):
    # Adicionar logica de busca no banco
    if id > len(pets):
        return {
            "error": "Pet not found"
        }

    for pet in pets:
        if pet["id"] == id:
            return {"data": pet}


@app.post("/pets/register", tags=["pets"], dependencies=[Depends(jwtBearer())])
def register_pet(pet: PetSchema):
    # Adicionar local de registro em banco
    pets.append(pet)
    return {"message": "Pet registered successfully!"}


@app.post("/user/register", tags=["user"])
def user_register(user: UserSchema = Body(default=None)):
    # Adicionar logica de registro em banco
    users.append(user)
    return {"message": "User registered successfully!"}


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            False


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    # Adicionar logica de validação do usuario no banco
    if check_user(user):
        return {
            "logged": True,
            "access_token": signJWT(user.email)
        }
    return {"logged": False, "error": "User not found"}


@app.get("/users", tags=["user"])
def list_users():
    return users
