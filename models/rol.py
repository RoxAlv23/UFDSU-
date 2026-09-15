from typing import Optional
from sqlmodel import SQLModel, Field


class Rol(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    nombre: str = Field(
        max_length=50,
        unique=True,
        nullable=False
    )