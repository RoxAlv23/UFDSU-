from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from config.session_dependencia import get_session
from models.usuario import (
    Usuario,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioPatch
)
from models.rol import Rol


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/", response_model=List[Usuario])
def listar_usuarios(
    session: Session = Depends(get_session)
):
    consulta = select(Usuario)

    resultado = session.exec(consulta)

    return resultado.all()


@router.get("/{usuario_id}", response_model=Usuario)
def buscar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("/", response_model=Usuario, status_code=201)
def crear_usuario(
    datos_usuario: UsuarioCreate,
    session: Session = Depends(get_session)
):
    consulta_username = select(Usuario).where(
        Usuario.username == datos_usuario.username
    )

    usuario_existente = session.exec(
        consulta_username
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El username ya existe"
        )

    consulta_rol = select(Rol).where(
        Rol.id == datos_usuario.id_rol
    )

    rol = session.exec(consulta_rol).first()

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="El rol no existe"
        )

    nuevo_usuario = Usuario(
        username=datos_usuario.username,
        nombre=datos_usuario.nombre,
        correo=datos_usuario.correo,
        password=datos_usuario.password,
        id_rol=datos_usuario.id_rol
    )

    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)

    return nuevo_usuario


@router.put("/{usuario_id}", response_model=Usuario)
def actualizar_usuario(
    usuario_id: int,
    datos_usuario: UsuarioUpdate,
    session: Session = Depends(get_session)
):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if datos_usuario.username:
        consulta_username = select(Usuario).where(
            Usuario.username == datos_usuario.username,
            Usuario.id != usuario_id
        )

        usuario_existente = session.exec(
            consulta_username
        ).first()

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="El username ya existe"
            )

    if datos_usuario.id_rol:
        consulta_rol = select(Rol).where(
            Rol.id == datos_usuario.id_rol
        )

        rol = session.exec(consulta_rol).first()

        if not rol:
            raise HTTPException(
                status_code=404,
                detail="El rol no existe"
            )

    datos = datos_usuario.model_dump(
        exclude_unset=True
    )

    for campo, valor in datos.items():
        setattr(usuario, campo, valor)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.patch("/{usuario_id}", response_model=Usuario)
def actualizar_usuario_parcial(
    usuario_id: int,
    datos_usuario: UsuarioPatch,
    session: Session = Depends(get_session)
):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    datos = datos_usuario.model_dump(
        exclude_unset=True
    )

    if "username" in datos:
        consulta_username = select(Usuario).where(
            Usuario.username == datos["username"],
            Usuario.id != usuario_id
        )

        usuario_existente = session.exec(
            consulta_username
        ).first()

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="El username ya existe"
            )

    if "id_rol" in datos:
        consulta_rol = select(Rol).where(
            Rol.id == datos["id_rol"]
        )

        rol = session.exec(consulta_rol).first()

        if not rol:
            raise HTTPException(
                status_code=404,
                detail="El rol no existe"
            )

    for campo, valor in datos.items():
        setattr(usuario, campo, valor)

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    usuario = session.get(Usuario, usuario_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    session.delete(usuario)
    session.commit()

    return {
        "mensaje": "Usuario eliminado correctamente"
    }