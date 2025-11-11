"""
Configuración de la base de datos SQLite.
Gestiona la conexión y las sesiones de la base de datos.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models import Base
import os

# URL de conexión a SQLite
# Usa variable de entorno o usa ruta por defecto
# Para Docker: sqlite:///./data/tasks.db (con volumen persistente)
# Para local: sqlite:///./tasks.db
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

# Motor de base de datos
# check_same_thread=False permite usar SQLite en múltiples threads (necesario para FastAPI)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Inicializa la base de datos creando todas las tablas.
    Se ejecuta al iniciar la aplicación.
    """
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Generador de sesiones de base de datos para inyección de dependencias.
    Garantiza que la sesión se cierre después de cada request.
    
    Yields:
        Session: Sesión de SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
