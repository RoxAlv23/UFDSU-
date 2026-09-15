from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel


class ProductoBase(SQLModel):
    nombre: str
    descripcion: str | None = None
    precio_compra: Decimal
    precio_venta: Decimal
    stock: int = 0
    imagen: str | None = None
    id_categoria: int


class Producto(ProductoBase, table=True):
    __tablename__ = "productos"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    id_categoria: int = Field(
        foreign_key="categorias.id"
    )

    created_at: datetime = Field(
        default_factory=datetime.now
    )

    updated_at: datetime = Field(
        default_factory=datetime.now
    )


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(SQLModel):
    nombre: str | None = None
    descripcion: str | None = None
    precio_compra: Decimal | None = None
    precio_venta: Decimal | None = None
    stock: int | None = None
    imagen: str | None = None
    id_categoria: int | None = None


class ProductoPatch(ProductoUpdate):
    pass