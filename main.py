from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.db import create_db_and_tables

from models import Categoria, Producto

from routers.categorias_router import router as categorias_router

from routers.producto_router import router as productos_router

from models import Categoria, Producto, Rol, Usuario

from routers.usuarios_router import router as usuarios_router

from oauth.oauth import router as oauth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_db_and_tables()

    yield


app = FastAPI(
    title="Comercial API",
    lifespan=lifespan
)


app.include_router(categorias_router)

app.include_router(productos_router)

app.include_router(usuarios_router)

app.include_router(oauth_router)


@app.get("/")
def inicio():

    return {
        "mensaje": "API Comercial funcionando"
    }