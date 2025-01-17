from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from .config import settings
from .api.endpoints import creatures, payments
from .database import Base, engine
from .models import Creature, Client, Wheel, Book, Scene

def create_app() -> FastAPI:
    app = FastAPI(
        title="Magical Creatures API",
        description="API for managing magical creatures",
        version="1.0.0"
    )

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Dependency para obtener la sesión de base de datos
    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = SessionLocal()
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response

    # Inicializar la base de datos
    init_db()

    # Incluir routers
    app.include_router(creatures.router, prefix="/api", tags=["creatures"])
    app.include_router(payments.router, prefix="/api/payments", tags=["payments"])

    # Agregar headers de seguridad
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        for key, value in settings.SECURITY_HEADERS.items():
            response.headers[key] = value
        return response

    @app.get("/")
    async def root():
        return {"message": "Welcome to Magical Creatures API"}

    return app

# Crear la instancia de la aplicación
app = create_app()

