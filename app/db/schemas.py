from pydantic import BaseModel, Field, Extra
from typing import Any, Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel

# Response
DataType = TypeVar("DataType")


class BaseResponse(GenericModel, Generic[DataType]):
    success: bool = Field(..., example=True)
    content: Optional[DataType] = Field(None, example={"id": 1, "name": "John Doe"})


class UserResponse(GenericModel, Generic[DataType]):
    success: bool = Field(..., example=True)
    content: Optional[DataType] = Field(None, example={"id": 1, "name": "John Doe"})
    access_token: str = Field(None)
    expires: int = Field(1440)


# User Schemas


class UserBase(BaseModel):
    email: str = Field(example="fulano@email.com")


class UserUpdate(BaseModel):
    primeiro_nome: Optional[str] = Field(example="Fulano")
    ultimo_nome: Optional[str] = Field(example="de Tal")


class UserCreate(UserBase):
    primeiro_nome: str = Field(example="Fulano")
    ultimo_nome: str = Field(example="de Tal")
    senha: str = Field(example="123456")


class UserLogin(UserBase):
    senha: str = Field(example="123456")


class User(UserBase):
    id: int = Field(example=1)
    primeiro_nome: str = Field(example="Fulano")
    ultimo_nome: str = Field(example="de Tal")

    class Config:
        orm_mode = True

# Pet Schemas


class PetBase(BaseModel):
    nome: str = Field(example="Fido")
    idade: int = Field(example=2)
    especie: str = Field(example="Cachorro")
    raca: str = Field(example="Vira-lata")
    sexo: str = Field(example="Macho")
    observacoes: str = Field(example="Cachorro muito brincalhão")


class UpdatePet(BaseModel):
    idade: Optional[int] = Field(example=2)
    especie: Optional[str] = Field(example="Cachorro")
    raca: Optional[str] = Field(example="Vira-lata")
    sexo: Optional[str] = Field(example="Macho")
    observacoes: Optional[str] = Field(example="Cachorro muito brincalhão")
    adotado: Optional[bool] = Field(example=False)


class Pet(PetBase):
    id: int = Field(example=1)
    adotado: bool = Field(example=False)

    class Config:
        orm_mode = True
