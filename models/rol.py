from typing import Optional

from sqlmodel import SQLModel, Field


class RolBase(SQLModel):
    nombre: str = Field(
        min_length=3,
        max_length=50
    )


class Rol(RolBase, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )


class RolCreate(RolBase):
    pass


class RolUpdate(SQLModel):
    nombre: Optional[str] = None