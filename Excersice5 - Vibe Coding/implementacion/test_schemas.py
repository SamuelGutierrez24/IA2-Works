"""
Pruebas para los esquemas de validación (schemas.py).
Valida que Pydantic aplique correctamente las restricciones.
"""

import pytest
from pydantic import ValidationError
from schemas import TaskCreate, TaskUpdate, TaskResponse
from datetime import datetime


class TestTaskCreateSchema:
    """Pruebas para el esquema TaskCreate."""
    
    def test_valid_task_create(self):
        """Debe validar correctamente datos válidos."""
        data = {
            "title": "Nueva tarea",
            "description": "Descripción válida",
            "completed": False
        }
        
        task = TaskCreate(**data)
        
        assert task.title == "Nueva tarea"
        assert task.description == "Descripción válida"
        assert task.completed is False
    
    def test_task_create_with_defaults(self):
        """Debe usar valores por defecto cuando no se proporcionan."""
        data = {"title": "Solo título"}
        
        task = TaskCreate(**data)
        
        assert task.title == "Solo título"
        assert task.description is None
        assert task.completed is False
    
    def test_task_create_missing_title(self):
        """Debe fallar si falta el título."""
        data = {"description": "Sin título"}
        
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**data)
        
        assert "title" in str(exc_info.value)
    
    def test_task_create_title_too_long(self):
        """Debe fallar si el título excede 200 caracteres."""
        data = {"title": "x" * 201}
        
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**data)
        
        assert "title" in str(exc_info.value)
    
    def test_task_create_empty_title(self):
        """Debe fallar si el título está vacío."""
        data = {"title": ""}
        
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**data)
        
        assert "title" in str(exc_info.value)
    
    def test_task_create_description_too_long(self):
        """Debe fallar si la descripción excede 500 caracteres."""
        data = {
            "title": "Título válido",
            "description": "x" * 501
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**data)
        
        assert "description" in str(exc_info.value)
    
    def test_task_create_invalid_completed_type(self):
        """Debe fallar si completed no es booleano."""
        data = {
            "title": "Título",
            "completed": "no es booleano"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(**data)
        
        assert "completed" in str(exc_info.value)


class TestTaskUpdateSchema:
    """Pruebas para el esquema TaskUpdate."""
    
    def test_task_update_all_optional(self):
        """Debe permitir actualizar cualquier campo individualmente."""
        # Solo título
        update1 = TaskUpdate(title="Nuevo título")
        assert update1.title == "Nuevo título"
        assert update1.description is None
        assert update1.completed is None
        
        # Solo completed
        update2 = TaskUpdate(completed=True)
        assert update2.title is None
        assert update2.completed is True
    
    def test_task_update_empty_valid(self):
        """Debe permitir crear esquema sin ningún campo."""
        update = TaskUpdate()
        
        assert update.title is None
        assert update.description is None
        assert update.completed is None
    
    def test_task_update_validation_still_applies(self):
        """Debe seguir validando los campos proporcionados."""
        with pytest.raises(ValidationError):
            TaskUpdate(title="x" * 201)  # Muy largo
        
        with pytest.raises(ValidationError):
            TaskUpdate(title="")  # Vacío


class TestTaskResponseSchema:
    """Pruebas para el esquema TaskResponse."""
    
    def test_task_response_from_dict(self):
        """Debe crear respuesta desde diccionario."""
        data = {
            "id": 1,
            "title": "Tarea de respuesta",
            "description": "Descripción",
            "completed": True,
            "created_at": datetime.now(),
            "updated_at": None
        }
        
        response = TaskResponse(**data)
        
        assert response.id == 1
        assert response.title == "Tarea de respuesta"
        assert isinstance(response.created_at, datetime)
    
    def test_task_response_requires_id(self):
        """Debe requerir ID (campo obligatorio en respuesta)."""
        data = {
            "title": "Sin ID",
            "completed": False,
            "created_at": datetime.now()
        }
        
        with pytest.raises(ValidationError) as exc_info:
            TaskResponse(**data)
        
        assert "id" in str(exc_info.value)
