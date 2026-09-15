from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from config.session_dependencia import SessionDep

from models.cateogoria import Categoria

from models.producto import (
    Producto,
    ProductoCreate,
    ProductoUpdate,
    ProductoPatch
)


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


# LISTAR TODOS LOS PRODUCTOS
@router.get("/", response_model=list[Producto])
def listar_productos(session: SessionDep):

    consulta = select(Producto)

    resultado = session.exec(consulta).all()

    return resultado


# BUSCAR PRODUCTO POR ID
@router.get("/{id}", response_model=Producto)
def buscar_producto(
    id: int,
    session: SessionDep
):

    consulta = select(Producto).where(
        Producto.id == id
    )

    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto


# AGREGAR PRODUCTO
@router.post("/", response_model=Producto)
def agregar_producto(
    datos_producto: ProductoCreate,
    session: SessionDep
):

    consulta = select(Categoria).where(
        Categoria.id == datos_producto.id_categoria
    )

    categoria = session.exec(consulta).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="La categoria no existe"
        )

    producto_nuevo = Producto(
        nombre=datos_producto.nombre,
        descripcion=datos_producto.descripcion,
        precio_compra=datos_producto.precio_compra,
        precio_venta=datos_producto.precio_venta,
        stock=datos_producto.stock,
        imagen=datos_producto.imagen,
        id_categoria=datos_producto.id_categoria
    )

    session.add(producto_nuevo)

    session.commit()

    session.refresh(producto_nuevo)

    return producto_nuevo


# ACTUALIZAR PRODUCTO CON PUT
@router.put("/{id}", response_model=Producto)
def actualizar_producto(
    id: int,
    datos_producto: ProductoUpdate,
    session: SessionDep
):

    consulta = select(Producto).where(
        Producto.id == id
    )

    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    if datos_producto.id_categoria is not None:

        consulta_categoria = select(Categoria).where(
            Categoria.id == datos_producto.id_categoria
        )

        categoria = session.exec(
            consulta_categoria
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=404,
                detail="La categoria no existe"
            )

    if datos_producto.nombre is not None:
        producto.nombre = datos_producto.nombre

    if datos_producto.descripcion is not None:
        producto.descripcion = datos_producto.descripcion

    if datos_producto.precio_compra is not None:
        producto.precio_compra = datos_producto.precio_compra

    if datos_producto.precio_venta is not None:
        producto.precio_venta = datos_producto.precio_venta

    if datos_producto.stock is not None:
        producto.stock = datos_producto.stock

    if datos_producto.imagen is not None:
        producto.imagen = datos_producto.imagen

    if datos_producto.id_categoria is not None:
        producto.id_categoria = datos_producto.id_categoria

    producto.updated_at = datetime.now()

    session.add(producto)

    session.commit()

    session.refresh(producto)

    return producto


# ELIMINAR PRODUCTO
@router.delete("/{id}")
def eliminar_producto(
    id: int,
    session: SessionDep
):

    consulta = select(Producto).where(
        Producto.id == id
    )

    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    session.delete(producto)

    session.commit()

    return {
        "mensaje": "Producto eliminado correctamente"
    }

# ACTUALIZAR PRODUCTO PARCIALMENTE CON PATCH
@router.patch("/{id}", response_model=Producto)
def actualizar_producto_parcial(
    id: int,
    datos_producto: ProductoPatch,
    session: SessionDep
):

    consulta = select(Producto).where(
        Producto.id == id
    )

    producto = session.exec(consulta).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    datos = datos_producto.model_dump(
        exclude_unset=True
    )

    if "id_categoria" in datos:

        consulta_categoria = select(Categoria).where(
            Categoria.id == datos["id_categoria"]
        )

        categoria = session.exec(
            consulta_categoria
        ).first()

        if not categoria:
            raise HTTPException(
                status_code=404,
                detail="La categoria no existe"
            )

    producto.sqlmodel_update(datos)

    producto.updated_at = datetime.now()

    session.add(producto)

    session.commit()

    session.refresh(producto)

    return producto