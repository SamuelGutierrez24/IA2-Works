"""
Configuración de fixtures para pytest.
Define recursos reutilizables para todas las pruebas.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from database import get_db
from models import Base

# URL de base de datos en memoria (temporal, se destruye al terminar)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """
    Crea un motor de base de datos temporal en memoria para cada test.
    Se destruye automáticamente al finalizar.
    """
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Crea una sesión de base de datos para cada test.
    Automáticamente hace rollback después de cada prueba.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente de pruebas de FastAPI con base de datos temporal.
    Sobreescribe la dependencia get_db para usar la BD en memoria.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_task_data():
    """Datos de ejemplo para crear tareas en las pruebas."""
    return {
        "title": "Tarea de prueba",
        "description": "Esta es una descripción de prueba",
        "completed": False
    }


@pytest.fixture
def multiple_tasks_data():
    """Conjunto de múltiples tareas para pruebas de listado."""
    return [
        {
            "title": "Primera tarea",
            "description": "Descripción 1",
            "completed": False
        },
        {
            "title": "Segunda tarea",
            "description": "Descripción 2",
            "completed": True
        },
        {
            "title": "Tercera tarea",
            "description": "Descripción 3",
            "completed": False
        }
    ]
