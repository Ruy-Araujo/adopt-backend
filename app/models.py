from pydantic import BaseModel, Field, Extra


class PetSchema(BaseModel):
    name: str = Field(example="Fido")
    age: int = Field(example=3)
    type: str = Field(example="dog")

    class Config:
        extra = Extra.allow


class UserSchema(BaseModel):
    username: str = Field(example="fulano")
    first_name: str = Field(example="Fulano")
    last_name: str = Field(example="de Tal")
    email: str = Field(example="fulano@email.com")
    password: str = Field(example="123456")

    class Config:
        extra = Extra.allow
        schema_extra = {
            "user_demo": {
                "first_name": "Fulano",
                "last_name": "de Tal",
                "email": "fulano@mail.com",
                "password": "123456"
            }
        }


class UserLoginSchema(BaseModel):
    email: str = Field(example="fulano@email.com")
    password: str = Field(example="123456")
