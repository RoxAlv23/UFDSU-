from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(
        max_length=50,
        unique=True,
        nullable=False
    )

    nombre: str = Field(
        max_length=100,
        nullable=False
    )

    correo: EmailStr = Field(
        max_length=150,
        nullable=False
    )

    password: str = Field(
        max_length=255,
        nullable=False
    )

    id_rol: int = Field(
        foreign_key="roles.id",
        nullable=False
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )