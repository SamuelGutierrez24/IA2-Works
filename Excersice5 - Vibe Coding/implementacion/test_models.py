"""
Pruebas para los modelos de datos (models.py).
Valida la estructura y comportamiento de los modelos ORM.
"""

import pytest
from datetime import datetime
from models import Task


class TestTaskModel:
    """Pruebas para el modelo Task."""
    
    def test_create_task_with_all_fields(self, db_session):
        """Debe crear una tarea con todos los campos."""
        task = Task(
            title="Tarea completa",
            description="Descripción detallada",
            completed=True
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.id is not None
        assert task.title == "Tarea completa"
        assert task.description == "Descripción detallada"
        assert task.completed is True
        assert task.created_at is not None
        assert isinstance(task.created_at, datetime)
    
    def test_create_task_minimal(self, db_session):
        """Debe crear una tarea solo con título."""
        task = Task(title="Título mínimo")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.id is not None
        assert task.title == "Título mínimo"
        assert task.description is None
        assert task.completed is False  # Valor por defecto
    
    def test_task_created_at_auto_generated(self, db_session):
        """Debe generar automáticamente created_at."""
        task = Task(title="Test timestamp")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        assert task.created_at is not None
        assert isinstance(task.created_at, datetime)
    
    def test_task_updated_at_on_modification(self, db_session):
        """Debe actualizar updated_at al modificar la tarea."""
        task = Task(title="Original")
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        # Modificar tarea
        task.title = "Modificado"
        db_session.commit()
        db_session.refresh(task)
        
        assert task.updated_at is not None
        assert isinstance(task.updated_at, datetime)
    
    def test_task_repr(self, db_session):
        """Debe tener una representación legible."""
        task = Task(title="Test repr", completed=False)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        repr_string = repr(task)
        assert "Task" in repr_string
        assert str(task.id) in repr_string
        assert "Test repr" in repr_string
