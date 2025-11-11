"""
Pruebas unitarias para las operaciones CRUD (crud.py).
Prueba la lógica de negocio de forma aislada.
"""

import pytest
from models import Task
from schemas import TaskCreate, TaskUpdate
import crud


class TestGetTasks:
    """Pruebas para obtener lista de tareas."""
    
    def test_get_empty_tasks(self, db_session):
        """Debe retornar lista vacía cuando no hay tareas."""
        tasks = crud.get_tasks(db_session)
        assert tasks == []
        assert len(tasks) == 0
    
    def test_get_tasks_returns_all(self, db_session):
        """Debe retornar todas las tareas existentes."""
        # Crear tareas directamente en BD
        task1 = Task(title="Tarea 1", description="Desc 1", completed=False)
        task2 = Task(title="Tarea 2", description="Desc 2", completed=True)
        db_session.add_all([task1, task2])
        db_session.commit()
        
        tasks = crud.get_tasks(db_session)
        
        assert len(tasks) == 2
        assert tasks[0].title == "Tarea 1"
        assert tasks[1].title == "Tarea 2"
    
    def test_get_tasks_pagination(self, db_session):
        """Debe respetar parámetros de paginación."""
        # Crear 5 tareas
        for i in range(5):
            task = Task(title=f"Tarea {i}", completed=False)
            db_session.add(task)
        db_session.commit()
        
        # Obtener solo 3 tareas, saltando las 2 primeras
        tasks = crud.get_tasks(db_session, skip=2, limit=3)
        
        assert len(tasks) == 3
        assert tasks[0].title == "Tarea 2"


class TestGetTask:
    """Pruebas para obtener una tarea específica."""
    
    def test_get_existing_task(self, db_session):
        """Debe retornar la tarea si existe."""
        task = Task(title="Mi tarea", description="Descripción", completed=False)
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        
        retrieved_task = crud.get_task(db_session, task.id)
        
        assert retrieved_task is not None
        assert retrieved_task.id == task.id
        assert retrieved_task.title == "Mi tarea"
    
    def test_get_nonexistent_task(self, db_session):
        """Debe retornar None si la tarea no existe."""
        task = crud.get_task(db_session, 999)
        assert task is None


class TestCreateTask:
    """Pruebas para creación de tareas."""
    
    def test_create_task_success(self, db_session):
        """Debe crear una tarea correctamente."""
        task_data = TaskCreate(
            title="Nueva tarea",
            description="Descripción de la nueva tarea",
            completed=False
        )
        
        created_task = crud.create_task(db_session, task_data)
        
        assert created_task.id is not None
        assert created_task.title == "Nueva tarea"
        assert created_task.description == "Descripción de la nueva tarea"
        assert created_task.completed is False
        assert created_task.created_at is not None
    
    def test_create_task_without_description(self, db_session):
        """Debe crear tarea sin descripción (campo opcional)."""
        task_data = TaskCreate(title="Solo título", completed=False)
        
        created_task = crud.create_task(db_session, task_data)
        
        assert created_task.id is not None
        assert created_task.title == "Solo título"
        assert created_task.description is None
    
    def test_create_task_defaults_to_incomplete(self, db_session):
        """Debe usar False como valor por defecto para completed."""
        task_data = TaskCreate(title="Tarea por defecto")
        
        created_task = crud.create_task(db_session, task_data)
        
        assert created_task.completed is False


class TestUpdateTask:
    """Pruebas para actualización de tareas."""
    
    def test_update_task_all_fields(self, db_session):
        """Debe actualizar todos los campos correctamente."""
        # Crear tarea inicial
        task = Task(title="Título original", description="Descripción original", completed=False)
        db_session.add(task)
        db_session.commit()
        task_id = task.id
        
        # Actualizar todos los campos
        update_data = TaskUpdate(
            title="Título actualizado",
            description="Descripción actualizada",
            completed=True
        )
        
        updated_task = crud.update_task(db_session, task_id, update_data)
        
        assert updated_task is not None
        assert updated_task.title == "Título actualizado"
        assert updated_task.description == "Descripción actualizada"
        assert updated_task.completed is True
        assert updated_task.updated_at is not None
    
    def test_update_task_partial(self, db_session):
        """Debe actualizar solo los campos proporcionados."""
        # Crear tarea inicial
        task = Task(title="Original", description="Descripción original", completed=False)
        db_session.add(task)
        db_session.commit()
        task_id = task.id
        
        # Actualizar solo el estado
        update_data = TaskUpdate(completed=True)
        
        updated_task = crud.update_task(db_session, task_id, update_data)
        
        assert updated_task.completed is True
        assert updated_task.title == "Original"  # No debe cambiar
        assert updated_task.description == "Descripción original"  # No debe cambiar
    
    def test_update_nonexistent_task(self, db_session):
        """Debe retornar None al intentar actualizar tarea inexistente."""
        update_data = TaskUpdate(title="Nuevo título")
        
        result = crud.update_task(db_session, 999, update_data)
        
        assert result is None


class TestDeleteTask:
    """Pruebas para eliminación de tareas."""
    
    def test_delete_existing_task(self, db_session):
        """Debe eliminar una tarea existente."""
        task = Task(title="Tarea a eliminar", completed=False)
        db_session.add(task)
        db_session.commit()
        task_id = task.id
        
        result = crud.delete_task(db_session, task_id)
        
        assert result is True
        
        # Verificar que ya no existe
        deleted_task = crud.get_task(db_session, task_id)
        assert deleted_task is None
    
    def test_delete_nonexistent_task(self, db_session):
        """Debe retornar False al intentar eliminar tarea inexistente."""
        result = crud.delete_task(db_session, 999)
        assert result is False
