from datetime import datetime

from sqlmodel import Field, SQLModel


class CategoriaBase(SQLModel):
    nombre: str
    descripcion: str | None = None


class Categoria(CategoriaBase, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None