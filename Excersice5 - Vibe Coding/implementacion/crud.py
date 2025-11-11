"""
Operaciones CRUD (Create, Read, Update, Delete) para tareas.
Lógica de acceso a datos separada de los endpoints.
"""

from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate
from typing import List, Optional


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    """
    Obtiene todas las tareas con paginación.
    
    Args:
        db: Sesión de base de datos
        skip: Número de registros a omitir (para paginación)
        limit: Número máximo de registros a devolver
        
    Returns:
        Lista de tareas
    """
    return db.query(Task).offset(skip).limit(limit).all()


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """
    Obtiene una tarea específica por ID.
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea
        
    Returns:
        Tarea si existe, None en caso contrario
    """
    return db.query(Task).filter(Task.id == task_id).first()


def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Crea una nueva tarea en la base de datos.
    
    Args:
        db: Sesión de base de datos
        task: Datos de la tarea a crear
        
    Returns:
        Tarea creada con su ID asignado
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)  # Refresca para obtener el ID y timestamps
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """
    Actualiza una tarea existente (actualización parcial permitida).
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a actualizar
        task_update: Datos a actualizar (solo los campos proporcionados)
        
    Returns:
        Tarea actualizada si existe, None en caso contrario
    """
    db_task = get_task(db, task_id)
    if db_task is None:
        return None
    
    # Actualiza solo los campos que fueron proporcionados
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Elimina una tarea de la base de datos.
    
    Args:
        db: Sesión de base de datos
        task_id: ID de la tarea a eliminar
        
    Returns:
        True si se eliminó, False si no existía
    """
    db_task = get_task(db, task_id)
    if db_task is None:
        return False
    
    db.delete(db_task)
    db.commit()
    return True
