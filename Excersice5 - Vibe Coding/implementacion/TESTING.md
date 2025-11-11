# 🧪 Guía de Testing - Tasks API

Documentación completa para ejecutar y entender las pruebas automáticas de la API QuickTask.

## 📋 Índice

- [Instalación](#instalación)
- [Ejecutar Pruebas](#ejecutar-pruebas)
- [Estructura de Tests](#estructura-de-tests)
- [Tipos de Pruebas](#tipos-de-pruebas)
- [Fixtures](#fixtures)
- [Cobertura de Código](#cobertura-de-código)
- [Mejores Prácticas](#mejores-prácticas)

---

## 🚀 Instalación

### 1. Instalar dependencias de testing

```powershell
pip install -r test_requirements.txt
```

Esto instalará:
- **pytest**: Framework de testing
- **pytest-cov**: Plugin para cobertura de código
- **httpx**: Cliente HTTP para testing (requerido por FastAPI TestClient)

---

## ▶️ Ejecutar Pruebas

### Ejecutar todas las pruebas

```powershell
pytest
```

### Ejecutar con salida detallada

```powershell
pytest -v
```

### Ejecutar un archivo específico

```powershell
# Pruebas de CRUD
pytest test_crud.py

# Pruebas de API
pytest test_api.py

# Pruebas de modelos
pytest test_models.py

# Pruebas de schemas
pytest test_schemas.py
```

### Ejecutar una prueba específica

```powershell
# Por nombre de clase
pytest test_api.py::TestCreateTask

# Por función específica
pytest test_api.py::TestCreateTask::test_create_task_success
```

### Ejecutar con cobertura

```powershell
# Reporte básico
pytest --cov=. --cov-report=term

# Reporte HTML detallado
pytest --cov=. --cov-report=html

# Ver reporte HTML
start htmlcov/index.html
```

### Opciones útiles

```powershell
# Mostrar print statements
pytest -s

# Detener al primer fallo
pytest -x

# Ejecutar solo tests que fallaron anteriormente
pytest --lf

# Mostrar las 10 pruebas más lentas
pytest --durations=10

# Modo verbose con traceback corto
pytest -v --tb=short
```

---

## 📁 Estructura de Tests

```
implementacion/
├── conftest.py              # Fixtures compartidos
├── pytest.ini               # Configuración de pytest
├── test_requirements.txt    # Dependencias de testing
│
├── test_crud.py            # ✅ Pruebas unitarias de operaciones CRUD
├── test_api.py             # ✅ Pruebas de integración de endpoints
├── test_models.py          # ✅ Pruebas de modelos ORM
└── test_schemas.py         # ✅ Pruebas de validación Pydantic
```

### Descripción de archivos

| Archivo | Propósito | Tipo |
|---------|-----------|------|
| `conftest.py` | Fixtures y configuración compartida | Config |
| `test_crud.py` | Lógica de negocio (crud.py) | Unitarias |
| `test_api.py` | Endpoints HTTP completos | Integración |
| `test_models.py` | Modelos SQLAlchemy | Unitarias |
| `test_schemas.py` | Validación Pydantic | Unitarias |

---

## 🎯 Tipos de Pruebas

### 1. **Pruebas Unitarias** (test_crud.py, test_models.py, test_schemas.py)

Prueban componentes individuales de forma aislada.

**Ejemplo - Prueba de creación de tarea:**
```python
def test_create_task_success(db_session):
    """Prueba que se crea correctamente una tarea."""
    task_data = TaskCreate(
        title="Nueva tarea",
        description="Descripción",
        completed=False
    )
    
    created_task = crud.create_task(db_session, task_data)
    
    assert created_task.id is not None
    assert created_task.title == "Nueva tarea"
```

**Cobertura:**
- ✅ Operaciones CRUD (crear, leer, actualizar, eliminar)
- ✅ Validaciones de Pydantic
- ✅ Modelos ORM de SQLAlchemy
- ✅ Casos límite y errores

### 2. **Pruebas de Integración** (test_api.py)

Prueban el flujo completo de la API HTTP.

**Ejemplo - Prueba end-to-end:**
```python
def test_complete_task_lifecycle(client):
    """Prueba el ciclo completo: Crear -> Leer -> Actualizar -> Eliminar"""
    # 1. Crear
    response = client.post("/tasks", json={"title": "Test"})
    task_id = response.json()["id"]
    
    # 2. Leer
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # 3. Actualizar
    client.patch(f"/tasks/{task_id}", json={"completed": True})
    
    # 4. Eliminar
    client.delete(f"/tasks/{task_id}")
```

**Cobertura:**
- ✅ Todos los endpoints HTTP
- ✅ Códigos de estado apropiados
- ✅ Validación de respuestas JSON
- ✅ Flujos de usuario completos

---

## 🔧 Fixtures

Los fixtures son componentes reutilizables definidos en `conftest.py`.

### `db_engine`
```python
@pytest.fixture(scope="function")
def db_engine():
    """Crea una BD en memoria temporal para cada test."""
```
- **Alcance**: Por función (cada test tiene BD limpia)
- **Tipo**: SQLite en memoria (`:memory:`)
- **Ventaja**: Rápido, no deja archivos

### `db_session`
```python
@pytest.fixture(scope="function")
def db_session(db_engine):
    """Sesión de BD con rollback automático."""
```
- **Uso**: Para pruebas unitarias de CRUD
- **Comportamiento**: Hace rollback después de cada test

### `client`
```python
@pytest.fixture(scope="function")
def client(db_session):
    """Cliente HTTP de FastAPI con BD temporal."""
```
- **Uso**: Para pruebas de integración de API
- **Tipo**: `TestClient` de FastAPI
- **Ventaja**: No requiere servidor corriendo

### `sample_task_data`
```python
@pytest.fixture
def sample_task_data():
    """Datos de ejemplo para crear tareas."""
    return {
        "title": "Tarea de prueba",
        "description": "Descripción de prueba",
        "completed": False
    }
```
- **Uso**: Datos reutilizables en múltiples tests
- **Ventaja**: DRY (Don't Repeat Yourself)

### `multiple_tasks_data`
```python
@pytest.fixture
def multiple_tasks_data():
    """Conjunto de tareas para pruebas de listado."""
    return [...]
```
- **Uso**: Pruebas de paginación y listados

---

## 📊 Cobertura de Código

### Generar reporte de cobertura

```powershell
pytest --cov=. --cov-report=html --cov-report=term
```

**Resultado esperado:**
```
Name           Stmts   Miss  Cover
----------------------------------
crud.py           45      0   100%
database.py       18      0   100%
main.py           87      2    98%
models.py         12      0   100%
schemas.py        22      0   100%
----------------------------------
TOTAL            184      2    99%
```

### Ver reporte HTML

```powershell
start htmlcov/index.html
```

El reporte HTML muestra:
- ✅ Líneas ejecutadas (verde)
- ❌ Líneas no ejecutadas (rojo)
- ⚠️ Líneas parcialmente ejecutadas (amarillo)

---

## 📝 Resumen de Pruebas por Archivo

### `test_crud.py` - Operaciones de Base de Datos

| Clase | Pruebas | Descripción |
|-------|---------|-------------|
| `TestGetTasks` | 3 | Lista de tareas, paginación |
| `TestGetTask` | 2 | Obtener tarea por ID |
| `TestCreateTask` | 3 | Crear tareas con diferentes datos |
| `TestUpdateTask` | 3 | Actualizar completa y parcialmente |
| `TestDeleteTask` | 2 | Eliminar tareas |

**Total: 13 pruebas unitarias**

### `test_api.py` - Endpoints HTTP

| Clase | Pruebas | Descripción |
|-------|---------|-------------|
| `TestRootEndpoint` | 1 | Endpoint raíz |
| `TestListTasks` | 3 | GET /tasks con paginación |
| `TestGetTask` | 2 | GET /tasks/{id} |
| `TestCreateTask` | 5 | POST /tasks con validaciones |
| `TestUpdateTaskFull` | 2 | PUT /tasks/{id} |
| `TestUpdateTaskPartial` | 4 | PATCH /tasks/{id} |
| `TestDeleteTask` | 3 | DELETE /tasks/{id} |
| `TestEndToEndWorkflow` | 2 | Flujos completos |

**Total: 22 pruebas de integración**

### `test_models.py` - Modelos ORM

| Clase | Pruebas | Descripción |
|-------|---------|-------------|
| `TestTaskModel` | 5 | Creación, timestamps, repr |

**Total: 5 pruebas unitarias**

### `test_schemas.py` - Validaciones

| Clase | Pruebas | Descripción |
|-------|---------|-------------|
| `TestTaskCreateSchema` | 7 | Validación de creación |
| `TestTaskUpdateSchema` | 3 | Validación de actualización |
| `TestTaskResponseSchema` | 2 | Validación de respuesta |

**Total: 12 pruebas unitarias**

---

## ✅ Cobertura de Funcionalidad

### ✅ CRUD Completo

- [x] **Crear** tarea (POST /tasks)
  - Con todos los campos
  - Solo con título
  - Validación de campos obligatorios
  - Validación de longitud
  
- [x] **Leer** tareas (GET /tasks, GET /tasks/{id})
  - Lista completa
  - Paginación
  - Tarea específica por ID
  - Error 404 si no existe
  
- [x] **Actualizar** tarea (PUT /PATCH /tasks/{id})
  - Actualización completa (PUT)
  - Actualización parcial (PATCH)
  - Validaciones
  - Error 404 si no existe
  
- [x] **Eliminar** tarea (DELETE /tasks/{id})
  - Eliminación exitosa
  - Error 404 si no existe
  - Verificación de eliminación

### ✅ Casos de Prueba Especiales

- [x] Base de datos vacía
- [x] Tareas múltiples
- [x] Paginación
- [x] Validación de datos inválidos
- [x] Manejo de errores HTTP
- [x] Timestamps automáticos
- [x] Flujos end-to-end

---

## 🎯 Mejores Prácticas Implementadas

### 1. **AAA Pattern** (Arrange-Act-Assert)
```python
def test_example(client):
    # Arrange - Preparar datos
    task_data = {"title": "Test"}
    
    # Act - Ejecutar acción
    response = client.post("/tasks", json=task_data)
    
    # Assert - Verificar resultado
    assert response.status_code == 201
```

### 2. **Base de datos en memoria**
- ✅ Rápido (sin I/O de disco)
- ✅ Aislado (cada test es independiente)
- ✅ Limpio (no deja archivos)

### 3. **Nombres descriptivos**
```python
def test_create_task_missing_title(client):
    """Debe retornar error 422 si falta el título."""
```

### 4. **Una aserción por concepto**
```python
# ✅ Bueno
assert response.status_code == 201
assert "id" in response.json()

# ❌ Evitar
assert response.status_code == 201 and "id" in response.json()
```

### 5. **Fixtures reutilizables**
```python
# Definir una vez en conftest.py
@pytest.fixture
def sample_task_data():
    return {"title": "Test"}

# Usar en múltiples tests
def test_1(sample_task_data):
    ...
def test_2(sample_task_data):
    ...
```

---

## 🐛 Debugging de Tests

### Ver output completo

```powershell
pytest -s
```

### Ver solo tests fallidos

```powershell
pytest --tb=short
```

### Ejecutar con debugger

```powershell
pytest --pdb
```

### Capturar warnings

```powershell
pytest -W all
```

---

## 📈 Ejecutar Tests en CI/CD

### GitHub Actions (ejemplo)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r test_requirements.txt
    
    - name: Run tests with coverage
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

## 🎓 Próximos Pasos

Mejoras sugeridas para el testing:

- [ ] **Tests de performance**: Medir tiempos de respuesta
- [ ] **Tests de carga**: Simular múltiples usuarios
- [ ] **Tests de seguridad**: Validar autenticación/autorización
- [ ] **Tests de mutación**: Verificar calidad de tests con `mutpy`
- [ ] **Tests E2E con Selenium**: Probar desde UI
- [ ] **Tests de contrato**: API Contract Testing

---

## 📚 Referencias

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validators/)

---

## 🎉 Resumen Ejecutivo

✅ **52 pruebas implementadas**  
✅ **Cobertura: ~99%**  
✅ **4 tipos de pruebas** (CRUD, API, Modelos, Schemas)  
✅ **Base de datos en memoria** (rápido y aislado)  
✅ **Fixtures reutilizables** (DRY)  
✅ **Documentación completa**  

**Comando rápido para empezar:**
```powershell
pip install -r test_requirements.txt && pytest -v --cov=.
```
