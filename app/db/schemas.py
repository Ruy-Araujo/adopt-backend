from pydantic import BaseModel, Field, Extra
from typing import Optional


class UserBase(BaseModel):
    email: str = Field(example="fulano@email.com")
    primeiro_nome: str = Field(example="Fulano")
    ultimo_nome: str = Field(example="de Tal")


class UserUpdate(BaseModel):
    primeiro_nome: Optional[str] = Field(example="Fulano")
    ultimo_nome: Optional[str] = Field(example="de Tal")


class PasswordUpdate(BaseModel):
    senha: Optional[str] = Field(example="123456")


class UserCreate(UserBase):
    senha: str = Field(example="123456")


class UserLoginSchema(UserBase):
    email: str = Field(example="fulano@email.com")
    senha: str = Field(example="123456")


class User(UserBase):
    id: int = Field(example=1)

    class Config:
        orm_mode = True


class PetSchema(BaseModel):
    name: str = Field(example="Fido")
    age: int = Field(example=3)
    type: str = Field(example="dog")

    class Config:
        extra = Extra.allow
