from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import SessionLocal,init_db
from app.config import get_settings
from app.api.endpoints import creatures, payments
#from app.models import Creature, Client, Wheel, Book, Scene

def create_app() -> FastAPI:
    load_dotenv()
    config_name = os.getenv('FASTAPI_ENV', 'development')
    settings = get_settings(config_name)

    app = FastAPI(
        title="Magical Creatures API",
        description="API for managing magical creatures",
        version="1.0.0"
    )

    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todos los orígenes
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos los métodos
        allow_headers=["*"],  # Permite todos los headers
    )

    ###############################################################
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
    ###############################################################

    # Inicializar la base de datos
    init_db()

    # Add this after initializing the app
    app.mount("/static", StaticFiles(directory="static"), name="static")

    # Incluir routers
    app.include_router(creatures.router, tags=["creatures"])
    app.include_router(payments.router, prefix="/payments", tags=["payments"])

    ###############################################################
    # Agregar headers de seguridad
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        for key, value in settings.SECURITY_HEADERS.items():
            response.headers[key] = value
        return response
    ###############################################################

    @app.get("/")
    async def root():
        return {"message": "Welcome to Magical Creatures API"}

    return app

app = create_app()

# Ensure the static/creatures directory exists
os.makedirs(os.path.join(os.getcwd(), 'static', 'creatures'), exist_ok=True)

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("FASTAPI_HOST", "0.0.0.0")
    port = int(os.getenv("FASTAPI_PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)

