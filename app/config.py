from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Configuración de Base de Datos
    DATABASE: str = os.getenv('DATABASE', '')
    DB_USER: str = os.getenv('DB_USER', '')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', '')
    DB_HOST: str = os.getenv('DB_HOST', '')
    DEV_DB_HOST: str = os.getenv('DEV_DB_HOST', '')
    TEST_DB_HOST: str = os.getenv('TEST_DB_HOST', '')

    # Configuración común
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    
    # Configuración de servicios externos
    STRIPE_SECRET_KEY: str = os.getenv('STRIPE_SECRET_KEY', '')
    OPENAI_ORG_ID: str = os.getenv('OPENAI_ORG_ID', '')
    OPENAI_PROJECT_ID: str = os.getenv('OPENAI_PROJECT_ID', '')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')

    # Nuevas configuraciones
    FASTAPI_ENV: str = os.getenv('FASTAPI_ENV', 'development')
    IMAGE_SIZE: str = os.getenv('IMAGE_SIZE', '1024x1024')
    FASTAPI_HOST: str = os.getenv('FASTAPI_HOST', '0.0.0.0')
    FASTAPI_PORT: int = int(os.getenv('FASTAPI_PORT', '8000'))

    # Configuración de seguridad
    SECURITY_HEADERS: Dict[str, str] = {
        'Content-Security-Policy': "default-src 'self'",
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Frame-Options': 'DENY',
        'X-Content-Type-Options': 'nosniff',
        'Referrer-Policy': 'no-referrer'
    }

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # This will ignore any extra env vars not defined in the class

    @classmethod
    def parse_env_var(cls, field_name: str, raw_val: str):
        # Ignore Docker-specific variables
        if field_name in ["BACKEND_APP", "BACKEND_DOMAIN", "DOCKER_APP_ROUTER", 
                          "PGADMIN_APP_ROUTER", "BACKEND_APP_SERVICE", "PGADMIN_APP_SERVICE",
                          "PGADMIN_DEFAULT_EMAIL", "PGADMIN_DEFAULT_PASSWORD", "PGADMIN_DOMAIN"]:
            return None
        return raw_val  # Return the value as-is for other variables

class DevelopmentSettings(Settings):
    DEBUG: bool = True

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DEV_DB_HOST}/{self.DATABASE}"

class TestingSettings(Settings):
    TESTING: bool = True
    WTF_CSRF_ENABLED: bool = False

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.TEST_DB_HOST}/{self.DATABASE}"

class ProductionSettings(Settings):
    DEBUG: bool = False
    SESSION_COOKIE_SECURE: bool = True
    REMEMBER_COOKIE_SECURE: bool = True
    PREFERRED_URL_SCHEME: str = 'https'
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DATABASE}"

@lru_cache()
def get_settings(env: str = os.getenv("FASTAPI_ENV", "development")) -> Settings:
    settings_map = {
        "development": DevelopmentSettings,
        "testing": TestingSettings,
        "production": ProductionSettings
    }
    settings_class = settings_map.get(env, DevelopmentSettings)
    return settings_class()

# Instancia de configuración para usar en la aplicación
settings = get_settings()

