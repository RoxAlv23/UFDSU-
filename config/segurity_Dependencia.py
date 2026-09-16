from typing import Annotated

from fastapi import Depends, HTTPException, status

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from config.segurity import (
    oauth2_scheme,
    decodificar_token
)


OAuth2FormDeDependencia = Annotated[
    OAuth2PasswordRequestForm,
    Depends()
]


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    payload = decodificar_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    return payload


Token_Dependencia = Annotated[
    dict,
    Depends(get_current_user)
]

def verificar_rol(token: dict, roles_permitidos: list[int]):
    id_rol = token.get("id_rol")

    if id_rol not in roles_permitidos:
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos para realizar esta acción"
        )

    return token