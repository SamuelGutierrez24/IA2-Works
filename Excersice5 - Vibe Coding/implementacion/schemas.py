"""
Esquemas de validación con Pydantic.
Define la estructura de los datos de entrada/salida de la API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Esquema base con campos comunes de una tarea."""
    title: str = Field(..., min_length=1, max_length=200, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=500, description="Descripción opcional")
    completed: bool = Field(default=False, description="Estado de completado")


class TaskCreate(TaskBase):
    """Esquema para crear una nueva tarea."""
    pass


class TaskUpdate(BaseModel):
    """
    Esquema para actualizar una tarea existente.
    Todos los campos son opcionales para permitir actualizaciones parciales.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    """
    Esquema de respuesta que incluye campos adicionales de la BD.
    """
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """Configuración para permitir la conversión desde objetos ORM."""
        from_attributes = True
