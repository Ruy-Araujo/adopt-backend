from fastapi import FastAPI, Body, Depends
from starlette.responses import RedirectResponse
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer
from app.libs import load_metadata
from app.models import PetSchema, UserSchema, UserLoginSchema


pets = []  # Lista provisoria de pets deve ser substituida por um banco de dados
users = []  # Lista provisorio de usuarios deve ser substituida por um banco de dados
user_id = 1
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


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        else:
            False


@app.post("/users/login", tags=["access"])
def user_login(user: UserLoginSchema = Body(default=None)):
    # Adicionar logica de validação do usuario no banco
    if check_user(user):
        return {
            "logged": True,
            "access_token": signJWT(user.email)
        }
    return {"logged": False, "error": "User not found"}

##################
# Users Endpoints #
##################


@app.post("/user/register", tags=["user"])
def user_register(user: UserSchema = Body(default=None)):
    # Adicionar logica de registro em banco
    global user_id
    user.id = user_id
    users.append(user)
    user_id += 1
    return {"message": "User registered successfully!"}


@app.get("/users", tags=["user"], dependencies=[Depends(jwtBearer())])
def list_users():
    return users


@app.get("/user/{id}", tags=["user"], dependencies=[Depends(jwtBearer())])
def get_user(id: int):
    for user in users:
        if user.id == id:
            return user
    else:
        return {
            "error": "User not found"
        }


@app.put("/user/{id}", tags=["user"], dependencies=[Depends(jwtBearer())])
def update_user(id: int, user: UserSchema = Body(default=None)):
    for index, item in enumerate(users):
        if item.id == id:
            temp = users.pop(index)
            temp = user
            users.append(temp)
            return {"message": "User updated successfully!"}
    else:
        return {
            "error": "User not found"
        }


@app.delete("/user/{id}", tags=["user"], dependencies=[Depends(jwtBearer())])
def delete_user(id: int):
    global users
    for i, user in enumerate(users):
        if user.id == id:
            users.pop(i)
            return {'message': f'User deleted successfully'}
    else:
        return {
            "error": "User not found"
        }
