from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.mssql import TIMESTAMP, DATETIME2
from sqlalchemy.schema import FetchedValue

from .database import Base


class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    primeiro_nome = Column(String)
    ultimo_nome = Column(String)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    data_cadastro = Column(
        TIMESTAMP().with_variant(DATETIME2, "mssql"),
        server_default=FetchedValue(),
        nullable=False,
    )
