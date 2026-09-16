from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from config.session_dependencia import get_session
from models.usuario import Usuario
from lib.pwd import hash_password

from config.segurity_Dependencia import (
    Token_Dependencia,
    verificar_rol
)


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/")
def listar_usuarios(
    session: Session = Depends(get_session)
):
    usuarios = session.exec(
        select(Usuario)
    ).all()

    return usuarios


@router.get("/{usuario_id}")
def buscar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    usuario = session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post("/")
def crear_usuario(
    usuario: Usuario,
    session: Session = Depends(get_session)
):
    usuario_existente = session.exec(
        select(Usuario).where(
            Usuario.username == usuario.username
        )
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El username ya existe"
        )

    usuario.password = hash_password(
        usuario.password
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.put("/{usuario_id}")
def actualizar_usuario(
    usuario_id: int,
    datos: Usuario,
    session: Session = Depends(get_session)
):
    usuario = session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario_existente = session.exec(
        select(Usuario).where(
            Usuario.username == datos.username,
            Usuario.id != usuario_id
        )
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="El username ya existe"
        )

    usuario.username = datos.username
    usuario.nombre = datos.nombre
    usuario.correo = datos.correo
    usuario.id_rol = datos.id_rol

    if datos.password:
        usuario.password = hash_password(
            datos.password
        )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.patch("/{usuario_id}")
def actualizar_usuario_parcial(
    usuario_id: int,
    datos: dict,
    session: Session = Depends(get_session)
):
    usuario = session.get(
        Usuario,
        usuario_id
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if "username" in datos:
        usuario_existente = session.exec(
            select(Usuario).where(
                Usuario.username == datos["username"],
                Usuario.id != usuario_id
            )
        ).first()

        if usuario_existente:
            raise HTTPException(
                status_code=400,
                detail="El username ya existe"
            )

        usuario.username = datos["username"]

    if "nombre" in datos:
        usuario.nombre = datos["nombre"]

    if "correo" in datos:
        usuario.correo = datos["correo"]

    if "id_rol" in datos:
        usuario.id_rol = datos["id_rol"]

    if "password" in datos:
        usuario.password = hash_password(
            datos["password"]
        )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
):
    usuario = session.get(
        Usuario,
        usuario_id
    )

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