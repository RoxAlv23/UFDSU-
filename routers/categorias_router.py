from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlmodel import Session

from config.session_dependencia import SessionDep, get_session

from config.segurity_Dependencia import Token_Dependencia

from fastapi import Depends

from fastapi import HTTPException

from config.segurity_Dependencia import (
    Token_Dependencia,
    verificar_rol
)

from models.cateogoria import (
    Categoria,
    CategoriaCreate,
    CategoriaUpdate
)


router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)


# LISTAR TODAS LAS CATEGORÍAS
@router.get("/", response_model=list[Categoria])
def listar_categorias(session: SessionDep):

    consulta = select(Categoria)

    resultado = session.exec(consulta).all()

    return resultado


# BUSCAR UNA CATEGORÍA POR ID
@router.get("/{id}", response_model=Categoria)
def buscar_categoria(id: int, session: SessionDep):

    consulta = select(Categoria).where(
        Categoria.id == id
    )

    categoria = session.exec(consulta).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    return categoria


# AGREGAR UNA CATEGORÍA
@router.post("/")
def crear_categoria(
    categoria: Categoria,
    token: Token_Dependencia,
    session: Session = Depends(get_session)
):
    verificar_rol(
        token,
        [1]
    )

    session.add(categoria)
    session.commit()
    session.refresh(categoria)

    return categoria


# ACTUALIZAR UNA CATEGORÍA
@router.put("/{id}", response_model=Categoria)
def actualizar_categoria(
    id: int,
    datos_categoria: CategoriaUpdate,
    session: SessionDep
):

    consulta = select(Categoria).where(
        Categoria.id == id
    )

    categoria = session.exec(consulta).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoria no encontrada"
        )

    if datos_categoria.nombre is not None:
        categoria.nombre = datos_categoria.nombre

    if datos_categoria.descripcion is not None:
        categoria.descripcion = datos_categoria.descripcion

    session.add(categoria)

    session.commit()

    session.refresh(categoria)

    return categoria


# ELIMINAR UNA CATEGORÍA
@router.delete("/{categoria_id}")
def eliminar_categoria(
    categoria_id: int,
    token: Token_Dependencia,
    session: Session = Depends(get_session)
):
    verificar_rol(
        token,
        [1]
    )

    categoria = session.get(
        Categoria,
        categoria_id
    )

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    session.delete(categoria)
    session.commit()

    return {
        "mensaje": "Categoría eliminada correctamente"
    }

# PAGINACION DE CATEGORIAS

@router.get("/paginacion/")
def paginar_categorias(
    session: SessionDep,
    pagina: int = 1,
    limite: int = 5
):

    if pagina < 1:
        pagina = 1

    if limite < 1:
        limite = 5

    desplazamiento = (pagina - 1) * limite

    consulta = (
        select(Categoria)
        .offset(desplazamiento)
        .limit(limite)
    )

    resultado = session.exec(consulta).all()

    return {
        "pagina": pagina,
        "limite": limite,
        "categorias": resultado
    }