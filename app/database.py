from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear el motor de la base de datos
engine = create_engine(settings.DATABASE_URL)

# Crear una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base declarativa
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def db_initialize():
    inspector = inspect(engine)
    metadata = MetaData()

    try:
        # Importar los modelos aquí para evitar la importación circular
        from app.models.models import Wheel

        # Verificar si hay tablas existentes
        table_names = inspector.get_table_names()

        if table_names:
            logger.info(f"Tablas existentes: {table_names}")
            
            # Eliminar todas las tablas existentes de manera segura
            Base.metadata.drop_all(bind=engine)
            logger.info("Todas las tablas han sido eliminadas correctamente.")

        # Crear todas las tablas de nuevo
        Base.metadata.create_all(bind=engine)
        logger.info("Todas las tablas han sido creadas correctamente.")

        # Verificar si la tabla Wheel está vacía e inicializarla con datos
        with SessionLocal() as session:
            if session.query(Wheel).count() == 0:
                logger.info("Inicializando la tabla Wheel con datos por defecto...")
                for i in range(1, 500):  # Cambia a 1 millón si es necesario
                    wheel_entry = Wheel(numero=i)
                    session.add(wheel_entry)
                session.commit()
                logger.info("Datos iniciales en Wheel agregados correctamente.")
            else:
                logger.info("La tabla Wheel ya tiene datos, no se requieren inicializaciones.")

    except SQLAlchemyError as sae:
        logger.error(f"Error de SQLAlchemy al modificar la base de datos: {str(sae)}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al modificar la base de datos: {str(e)}")
        raise

# Función para inicializar la base de datos (puede ser llamada desde main.py)
def init_db():
    db_initialize()

