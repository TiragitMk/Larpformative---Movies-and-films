"""
Incluye todos los routers del programa y CORS del servidor de FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.fastapi_routers import films_rt, comments_rt, ratings_rt, users_rt

app = FastAPI(title="Cine API")

app.include_router(films_rt.router)
app.include_router(comments_rt.router)
app.include_router(ratings_rt.router)
app.include_router(users_rt.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # origen (protocolo, dominio, puerto) del frontend
    allow_methods=["*"],
    allow_headers=["*"],  # necesario para la cabecera Authorization de la fase 2, hay que permitir cabeceras.
)