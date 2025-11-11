"""
API REST para gestión de tareas usando FastAPI.
Punto de entrada principal de la aplicación.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import crud
import schemas
from database import get_db, init_db

# Crear instancia de la aplicación
app = FastAPI(
    title="Tasks API",
    description="API REST para gestión de tareas (TODO List)",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    """Evento que se ejecuta al iniciar la aplicación."""
    init_db()  # Crea las tablas si no existen


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz con información básica de la API."""
    return {
        "message": "Bienvenido a Tasks API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/tasks", response_model=List[schemas.TaskResponse], tags=["Tasks"])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas las tareas con paginación opcional.
    
    - **skip**: Número de registros a omitir (default: 0)
    - **limit**: Número máximo de registros (default: 100)
    """
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una tarea específica por su ID.
    
    - **task_id**: ID de la tarea
    """
    task = crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return task


@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"]
)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea.
    
    - **title**: Título de la tarea (obligatorio)
    - **description**: Descripción opcional
    - **completed**: Estado inicial (default: false)
    """
    return crud.create_task(db=db, task=task)


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task_full(
    task_id: int,
    task: schemas.TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Actualiza completamente una tarea (PUT - requiere todos los campos).
    
    - **task_id**: ID de la tarea a actualizar
    - **task**: Nuevos datos completos de la tarea
    """
    # Convertimos TaskCreate a TaskUpdate para la actualización
    task_update = schemas.TaskUpdate(**task.model_dump())
    updated_task = crud.update_task(db, task_id=task_id, task_update=task_update)
    
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return updated_task


@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task_partial(
    task_id: int,
    task: schemas.TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza parcialmente una tarea (PATCH - solo campos proporcionados).
    
    - **task_id**: ID de la tarea a actualizar
    - **task**: Campos a actualizar (todos opcionales)
    """
    updated_task = crud.update_task(db, task_id=task_id, task_update=task)
    
    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Elimina una tarea.
    
    - **task_id**: ID de la tarea a eliminar
    """
    deleted = crud.delete_task(db, task_id=task_id)
    
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada"
        )
    return None


# Para ejecutar: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
