from typing import Optional
from datetime import datetime

from sqlmodel import SQLModel, Field


class UsuarioBase(SQLModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )

    nombre: str = Field(
        min_length=3,
        max_length=100
    )

    correo: str = Field(
        min_length=5,
        max_length=150
    )

    password: str = Field(
        min_length=3,
        max_length=255
    )

    id_rol: int


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(SQLModel):
    username: Optional[str] = None
    nombre: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    id_rol: Optional[int] = None


class UsuarioPatch(SQLModel):
    username: Optional[str] = None
    nombre: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    id_rol: Optional[int] = None