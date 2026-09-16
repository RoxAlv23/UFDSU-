import os

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer


load_dotenv()


SECRET_KEY_TOKEN = os.getenv(
    "SECRET_KEY_TOKEN",
    "MiClaveSecretaTemporal"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="oauth/login"
)


def crear_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        payload=to_encode,
        key=SECRET_KEY_TOKEN,
        algorithm=ALGORITHM
    )

    return token


def decodificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY_TOKEN,
            algorithms=[ALGORITHM]
        )

        return payload

    except jwt.PyJWTError:
        return None