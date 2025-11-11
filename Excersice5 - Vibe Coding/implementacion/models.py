"""
Modelos de base de datos usando SQLAlchemy.
Define la estructura de la tabla 'tasks' en SQLite.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Base para todos los modelos ORM
Base = declarative_base()


class Task(Base):
    """
    Modelo de tarea.
    
    Atributos:
        id: Identificador único autoincrementable
        title: Título de la tarea (obligatorio)
        description: Descripción detallada (opcional)
        completed: Estado de completado (por defecto False)
        created_at: Fecha de creación (automática)
        updated_at: Fecha de última actualización (automática)
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', completed={self.completed})>"
