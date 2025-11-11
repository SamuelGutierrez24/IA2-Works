"""
Pruebas de integración para los endpoints de la API (main.py).
Prueba el comportamiento completo de la API HTTP.
"""

import pytest
from fastapi import status


class TestRootEndpoint:
    """Pruebas para el endpoint raíz."""
    
    def test_root_returns_welcome_message(self, client):
        """Debe retornar mensaje de bienvenida."""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "Bienvenido" in data["message"]
        assert data["version"] == "1.0.0"


class TestListTasks:
    """Pruebas para GET /tasks."""
    
    def test_list_tasks_empty(self, client):
        """Debe retornar lista vacía cuando no hay tareas."""
        response = client.get("/tasks")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
    
    def test_list_tasks_with_data(self, client, sample_task_data):
        """Debe retornar todas las tareas existentes."""
        # Crear 2 tareas
        client.post("/tasks", json=sample_task_data)
        client.post("/tasks", json={"title": "Segunda tarea", "completed": True})
        
        response = client.get("/tasks")
        
        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert len(tasks) == 2
        assert tasks[0]["title"] == sample_task_data["title"]
        assert tasks[1]["title"] == "Segunda tarea"
    
    def test_list_tasks_pagination(self, client, multiple_tasks_data):
        """Debe respetar parámetros de paginación."""
        # Crear múltiples tareas
        for task_data in multiple_tasks_data:
            client.post("/tasks", json=task_data)
        
        # Solicitar con paginación
        response = client.get("/tasks?skip=1&limit=2")
        
        assert response.status_code == status.HTTP_200_OK
        tasks = response.json()
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Segunda tarea"


class TestGetTask:
    """Pruebas para GET /tasks/{task_id}."""
    
    def test_get_existing_task(self, client, sample_task_data):
        """Debe retornar la tarea si existe."""
        # Crear tarea
        create_response = client.post("/tasks", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Obtener tarea
        response = client.get(f"/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == sample_task_data["title"]
        assert task["description"] == sample_task_data["description"]
    
    def test_get_nonexistent_task(self, client):
        """Debe retornar 404 si la tarea no existe."""
        response = client.get("/tasks/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "no encontrada" in response.json()["detail"]


class TestCreateTask:
    """Pruebas para POST /tasks."""
    
    def test_create_task_success(self, client, sample_task_data):
        """Debe crear una tarea correctamente."""
        response = client.post("/tasks", json=sample_task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        task = response.json()
        assert task["id"] is not None
        assert task["title"] == sample_task_data["title"]
        assert task["description"] == sample_task_data["description"]
        assert task["completed"] == sample_task_data["completed"]
        assert "created_at" in task
    
    def test_create_task_minimal_data(self, client):
        """Debe crear tarea solo con título."""
        minimal_data = {"title": "Solo título"}
        
        response = client.post("/tasks", json=minimal_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        task = response.json()
        assert task["title"] == "Solo título"
        assert task["description"] is None
        assert task["completed"] is False
    
    def test_create_task_missing_title(self, client):
        """Debe retornar error 422 si falta el título."""
        invalid_data = {"description": "Sin título", "completed": False}
        
        response = client.post("/tasks", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_title_too_long(self, client):
        """Debe retornar error si el título excede el límite."""
        invalid_data = {
            "title": "x" * 201,  # Más de 200 caracteres
            "completed": False
        }
        
        response = client.post("/tasks", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_create_task_empty_title(self, client):
        """Debe retornar error si el título está vacío."""
        invalid_data = {"title": "", "completed": False}
        
        response = client.post("/tasks", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUpdateTaskFull:
    """Pruebas para PUT /tasks/{task_id} (actualización completa)."""
    
    def test_update_task_full_success(self, client, sample_task_data):
        """Debe actualizar todos los campos de una tarea."""
        # Crear tarea
        create_response = client.post("/tasks", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Actualizar completamente
        update_data = {
            "title": "Título actualizado",
            "description": "Descripción actualizada",
            "completed": True
        }
        
        response = client.put(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["title"] == "Título actualizado"
        assert task["description"] == "Descripción actualizada"
        assert task["completed"] is True
        assert "updated_at" in task
    
    def test_update_nonexistent_task_full(self, client):
        """Debe retornar 404 al actualizar tarea inexistente."""
        update_data = {"title": "Nuevo", "completed": False}
        
        response = client.put("/tasks/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateTaskPartial:
    """Pruebas para PATCH /tasks/{task_id} (actualización parcial)."""
    
    def test_update_task_only_completed(self, client, sample_task_data):
        """Debe actualizar solo el estado de completado."""
        # Crear tarea
        create_response = client.post("/tasks", json=sample_task_data)
        task_id = create_response.json()["id"]
        original_title = sample_task_data["title"]
        
        # Actualizar solo completed
        update_data = {"completed": True}
        
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["completed"] is True
        assert task["title"] == original_title  # No debe cambiar
    
    def test_update_task_only_title(self, client, sample_task_data):
        """Debe actualizar solo el título."""
        # Crear tarea
        create_response = client.post("/tasks", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Actualizar solo título
        update_data = {"title": "Nuevo título"}
        
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["title"] == "Nuevo título"
        assert task["completed"] == sample_task_data["completed"]  # No debe cambiar
    
    def test_update_task_multiple_fields(self, client, sample_task_data):
        """Debe actualizar múltiples campos sin afectar los demás."""
        # Crear tarea
        create_response = client.post("/tasks", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Actualizar título y completed
        update_data = {
            "title": "Título parcial",
            "completed": True
        }
        
        response = client.patch(f"/tasks/{task_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        task = response.json()
        assert task["title"] == "Título parcial"
        assert task["completed"] is True
        assert task["description"] == sample_task_data["description"]  # No debe cambiar
    
    def test_update_nonexistent_task_partial(self, client):
        """Debe retornar 404 al actualizar parcialmente tarea inexistente."""
        update_data = {"completed": True}
        
        response = client.patch("/tasks/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteTask:
    """Pruebas para DELETE /tasks/{task_id}."""
    
    def test_delete_task_success(self, client, sample_task_data):
        """Debe eliminar una tarea existente."""
        # Crear tarea
        create_response = client.post("/tasks", json=sample_task_data)
        task_id = create_response.json()["id"]
        
        # Eliminar tarea
        response = client.delete(f"/tasks/{task_id}")
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que ya no existe
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_nonexistent_task(self, client):
        """Debe retornar 404 al eliminar tarea inexistente."""
        response = client.delete("/tasks/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_removes_from_list(self, client, multiple_tasks_data):
        """Debe eliminar la tarea de la lista general."""
        # Crear múltiples tareas
        task_ids = []
        for task_data in multiple_tasks_data:
            response = client.post("/tasks", json=task_data)
            task_ids.append(response.json()["id"])
        
        # Eliminar la segunda tarea
        client.delete(f"/tasks/{task_ids[1]}")
        
        # Verificar que solo quedan 2 tareas
        list_response = client.get("/tasks")
        tasks = list_response.json()
        assert len(tasks) == 2
        assert task_ids[1] not in [t["id"] for t in tasks]


class TestEndToEndWorkflow:
    """Pruebas de flujo completo (end-to-end)."""
    
    def test_complete_task_lifecycle(self, client):
        """
        Prueba el ciclo de vida completo de una tarea:
        Crear -> Leer -> Actualizar -> Eliminar
        """
        # 1. Crear tarea
        create_data = {
            "title": "Estudiar FastAPI",
            "description": "Completar tutorial oficial",
            "completed": False
        }
        create_response = client.post("/tasks", json=create_data)
        assert create_response.status_code == status.HTTP_201_CREATED
        task_id = create_response.json()["id"]
        
        # 2. Leer tarea
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        assert get_response.json()["title"] == "Estudiar FastAPI"
        
        # 3. Actualizar tarea (marcar como completada)
        patch_response = client.patch(
            f"/tasks/{task_id}",
            json={"completed": True}
        )
        assert patch_response.status_code == status.HTTP_200_OK
        assert patch_response.json()["completed"] is True
        
        # 4. Eliminar tarea
        delete_response = client.delete(f"/tasks/{task_id}")
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT
        
        # 5. Verificar que ya no existe
        final_get = client.get(f"/tasks/{task_id}")
        assert final_get.status_code == status.HTTP_404_NOT_FOUND
    
    def test_multiple_tasks_management(self, client):
        """Prueba la gestión de múltiples tareas simultáneamente."""
        # Crear 3 tareas
        tasks_data = [
            {"title": "Tarea 1", "completed": False},
            {"title": "Tarea 2", "completed": False},
            {"title": "Tarea 3", "completed": False}
        ]
        
        task_ids = []
        for task_data in tasks_data:
            response = client.post("/tasks", json=task_data)
            task_ids.append(response.json()["id"])
        
        # Verificar que todas existen
        list_response = client.get("/tasks")
        assert len(list_response.json()) == 3
        
        # Marcar la segunda como completada
        client.patch(f"/tasks/{task_ids[1]}", json={"completed": True})
        
        # Verificar estado
        task2 = client.get(f"/tasks/{task_ids[1]}").json()
        assert task2["completed"] is True
        
        # Eliminar la primera
        client.delete(f"/tasks/{task_ids[0]}")
        
        # Verificar que solo quedan 2
        final_list = client.get("/tasks").json()
        assert len(final_list) == 2
