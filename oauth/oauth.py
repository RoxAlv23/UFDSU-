from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session, select

from config.session_dependencia import get_session

from config.segurity import crear_token

from config.segurity_Dependencia import (
    OAuth2FormDeDependencia
)

from models.usuario import Usuario

from lib.pwd import verify_password


router = APIRouter(
    prefix="/oauth",
    tags=["Autenticación"]
)


@router.post("/login")
def login(
    form_data: OAuth2FormDeDependencia,
    session: Session = Depends(get_session)
):
    usuario = session.exec(
        select(Usuario).where(
            Usuario.username == form_data.username
        )
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o contraseña incorrectos"
        )

    password_correcta = verify_password(
        form_data.password,
        usuario.password
    )

    if not password_correcta:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username o contraseña incorrectos"
        )

    token = crear_token({
        "id": usuario.id,
        "username": usuario.username,
        "id_rol": usuario.id_rol
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }