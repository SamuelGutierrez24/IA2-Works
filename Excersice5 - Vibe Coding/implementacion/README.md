# Tasks API - FastAPI

API REST completa para gestión de tareas (TODO List) implementada con FastAPI, SQLAlchemy y SQLite.

## 📋 Características

- ✅ CRUD completo para tareas
- ✅ Validación de datos con Pydantic
- ✅ Persistencia con SQLite
- ✅ Documentación interactiva automática (Swagger/OpenAPI)
- ✅ Estructura de proyecto clara y escalable

## 🗂️ Estructura del Proyecto

```
implementacion/
├── main.py           # Punto de entrada, definición de endpoints
├── models.py         # Modelos ORM (SQLAlchemy)
├── schemas.py        # Esquemas de validación (Pydantic)
├── crud.py           # Operaciones de base de datos
├── database.py       # Configuración de BD
├── requirements.txt  # Dependencias
└── README.md         # Este archivo
```

## 🚀 Instalación

### 1. Crear entorno virtual (recomendado)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install -r requirements.txt
```

## ▶️ Ejecución

```powershell
uvicorn main:app --reload
```

La API estará disponible en: `http://localhost:8000`

- **Documentación interactiva (Swagger)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## 📡 Endpoints

### 1. **GET /** - Información de la API
```bash
curl http://localhost:8000/
```

**Respuesta:**
```json
{
  "message": "Bienvenido a Tasks API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

---

### 2. **GET /tasks** - Listar todas las tareas

```bash
curl http://localhost:8000/tasks
```

**Parámetros opcionales:**
- `skip`: Número de registros a omitir (paginación)
- `limit`: Número máximo de registros (default: 100)

**Ejemplo con paginación:**
```bash
curl "http://localhost:8000/tasks?skip=0&limit=10"
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "title": "Completar documentación",
    "description": "Escribir README completo",
    "completed": false,
    "created_at": "2025-11-11T10:30:00",
    "updated_at": null
  }
]
```

---

### 3. **GET /tasks/{task_id}** - Obtener una tarea específica

```bash
curl http://localhost:8000/tasks/1
```

**Respuesta exitosa (200):**
```json
{
  "id": 1,
  "title": "Completar documentación",
  "description": "Escribir README completo",
  "completed": false,
  "created_at": "2025-11-11T10:30:00",
  "updated_at": null
}
```

**Error si no existe (404):**
```json
{
  "detail": "Tarea con ID 999 no encontrada"
}
```

---

### 4. **POST /tasks** - Crear una nueva tarea

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Aprender FastAPI",
    "description": "Estudiar documentación oficial",
    "completed": false
  }'
```

**Campos:**
- `title` (obligatorio): Título de la tarea (1-200 caracteres)
- `description` (opcional): Descripción detallada (máx. 500 caracteres)
- `completed` (opcional): Estado inicial (default: false)

**Respuesta (201 Created):**
```json
{
  "id": 2,
  "title": "Aprender FastAPI",
  "description": "Estudiar documentación oficial",
  "completed": false,
  "created_at": "2025-11-11T11:00:00",
  "updated_at": null
}
```

---

### 5. **PUT /tasks/{task_id}** - Actualizar tarea completa

Actualiza todos los campos de una tarea (requiere enviar todos los campos).

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Documentación completada",
    "description": "README finalizado y revisado",
    "completed": true
  }'
```

**Respuesta (200):**
```json
{
  "id": 1,
  "title": "Documentación completada",
  "description": "README finalizado y revisado",
  "completed": true,
  "created_at": "2025-11-11T10:30:00",
  "updated_at": "2025-11-11T12:00:00"
}
```

---

### 6. **PATCH /tasks/{task_id}** - Actualizar parcialmente

Actualiza solo los campos proporcionados (actualización parcial).

**Ejemplo 1: Marcar como completada**
```bash
curl -X PATCH http://localhost:8000/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

**Ejemplo 2: Cambiar solo el título**
```bash
curl -X PATCH http://localhost:8000/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{"title": "Nuevo título"}'
```

**Respuesta (200):**
```json
{
  "id": 2,
  "title": "Nuevo título",
  "description": "Estudiar documentación oficial",
  "completed": true,
  "created_at": "2025-11-11T11:00:00",
  "updated_at": "2025-11-11T12:15:00"
}
```

---

### 7. **DELETE /tasks/{task_id}** - Eliminar una tarea

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

**Respuesta exitosa (204 No Content):**
Sin contenido en el cuerpo de la respuesta.

**Error si no existe (404):**
```json
{
  "detail": "Tarea con ID 999 no encontrada"
}
```

---

## 🧪 Ejemplos de Uso Completo

### Flujo típico de uso:

```bash
# 1. Crear tres tareas
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Comprar ingredientes", "description": "Leche, pan, huevos"}'

curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudiar Python", "completed": false}'

curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Hacer ejercicio", "description": "Gimnasio a las 6pm"}'

# 2. Listar todas las tareas
curl http://localhost:8000/tasks

# 3. Obtener tarea específica
curl http://localhost:8000/tasks/2

# 4. Marcar como completada
curl -X PATCH http://localhost:8000/tasks/2 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# 5. Actualizar descripción
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"description": "Leche, pan, huevos, mantequilla"}'

# 6. Eliminar tarea
curl -X DELETE http://localhost:8000/tasks/3

# 7. Verificar lista actualizada
curl http://localhost:8000/tasks
```

---

## 📊 Base de Datos

La aplicación utiliza SQLite con el archivo `tasks.db` que se crea automáticamente al iniciar.

**Esquema de la tabla `tasks`:**

| Campo       | Tipo      | Descripción                    |
|-------------|-----------|--------------------------------|
| id          | INTEGER   | Primary Key (autoincremental)  |
| title       | VARCHAR   | Título (obligatorio, máx. 200) |
| description | VARCHAR   | Descripción (opcional, máx. 500)|
| completed   | BOOLEAN   | Estado (default: false)        |
| created_at  | DATETIME  | Fecha de creación (automática) |
| updated_at  | DATETIME  | Fecha de actualización         |

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI** (0.104.1): Framework web moderno y rápido
- **SQLAlchemy** (2.0.23): ORM para Python
- **Pydantic** (2.5.0): Validación de datos
- **Uvicorn** (0.24.0): Servidor ASGI
- **SQLite**: Base de datos embebida

---

## 📝 Notas de Desarrollo

### Diferencia entre PUT y PATCH:
- **PUT**: Actualización completa (requiere todos los campos)
- **PATCH**: Actualización parcial (solo campos proporcionados)

### Validaciones implementadas:
- Título obligatorio (1-200 caracteres)
- Descripción opcional (máx. 500 caracteres)
- Validación automática de tipos por Pydantic
- Timestamps automáticos (created_at, updated_at)

### Características adicionales:
- Documentación automática en `/docs`
- Paginación en listado de tareas
- Manejo de errores con códigos HTTP apropiados
- Separación clara de responsabilidades (MVC pattern)

---

## 🎯 Próximos Pasos (Mejoras Futuras)

- [ ] Autenticación y autorización (JWT)
- [ ] Filtros y búsqueda de tareas
- [ ] Tests unitarios y de integración
- [ ] Docker y docker-compose
- [ ] Migraciones con Alembic
- [ ] Ordenamiento por fecha/prioridad
- [ ] Categorías o etiquetas para tareas

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
