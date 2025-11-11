# 🐳 Guía de Despliegue con Docker

Documentación completa para desplegar **QuickTask API** usando Docker y Docker Compose.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Arquitectura](#arquitectura)
- [Archivos de Configuración](#archivos-de-configuración)
- [Despliegue Local](#despliegue-local)
- [Comandos Útiles](#comandos-útiles)
- [Verificación y Pruebas](#verificación-y-pruebas)
- [Troubleshooting](#troubleshooting)
- [Producción](#producción)

---

## 🔧 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

### Windows

1. **Docker Desktop for Windows**
   - Descarga: https://www.docker.com/products/docker-desktop
   - Versión mínima: 20.10+
   - Incluye Docker Compose automáticamente

2. **Verificar instalación:**
```powershell
docker --version
docker-compose --version
```

**Salida esperada:**
```
Docker version 24.0.0, build xxxxxx
Docker Compose version v2.20.0
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────┐
│         Host (Windows/Mac/Linux)        │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │   Docker Container: quicktask-api │ │
│  │                                   │ │
│  │   ┌─────────────────────────┐    │ │
│  │   │   FastAPI Application   │    │ │
│  │   │   (uvicorn server)      │    │ │
│  │   │   Port: 8000            │    │ │
│  │   └─────────────────────────┘    │ │
│  │              │                    │ │
│  │              ▼                    │ │
│  │   ┌─────────────────────────┐    │ │
│  │   │  SQLite Database        │    │ │
│  │   │  /app/data/tasks.db     │    │ │
│  │   └─────────────────────────┘    │ │
│  │              │                    │ │
│  └──────────────┼────────────────────┘ │
│                 │                       │
│                 ▼                       │
│      ┌─────────────────────┐           │
│      │  Volume: db_data    │           │
│      │  (Persistencia)     │           │
│      └─────────────────────┘           │
│                                         │
│  localhost:8000 ◄────────────────────┐ │
└───────────────────────────────────────┼─┘
                                        │
                              ┌─────────▼────────┐
                              │  Browser/Client  │
                              │  HTTP Requests   │
                              └──────────────────┘
```

---

## 📁 Archivos de Configuración

### 1. `Dockerfile`

Define cómo construir la imagen Docker:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Características:**
- ✅ Imagen base ligera (`slim`)
- ✅ Caché de dependencias optimizado
- ✅ Variables de entorno configuradas
- ✅ Puerto 8000 expuesto

### 2. `docker-compose.yml`

Orquesta el despliegue:

```yaml
version: '3.8'

services:
  api:
    container_name: quicktask-api
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app                    # Código fuente
      - db_data:/app/data         # Base de datos persistente
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    restart: unless-stopped

volumes:
  db_data:
```

**Características:**
- ✅ Hot-reload activado (desarrollo)
- ✅ Persistencia de BD con volúmenes
- ✅ Reinicio automático
- ✅ Healthcheck incluido

### 3. `.dockerignore`

Excluye archivos innecesarios del contexto de build:

```
__pycache__/
*.pyc
venv/
.env
*.db
.pytest_cache/
```

---

## 🚀 Despliegue Local

### Opción 1: Con Docker Compose (Recomendado)

#### Paso 1: Construir y levantar el contenedor

```powershell
docker-compose up --build
```

**Primera vez:** Construye la imagen y levanta el contenedor  
**Siguientes veces:** Solo levanta el contenedor

#### Paso 2: Verificar que está corriendo

En otra terminal:
```powershell
docker ps
```

**Salida esperada:**
```
CONTAINER ID   IMAGE                  STATUS        PORTS                    NAMES
abc123def456   implementacion-api     Up 10 seconds 0.0.0.0:8000->8000/tcp  quicktask-api
```

#### Paso 3: Acceder a la API

- **API Root**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

#### Paso 4: Detener el contenedor

```powershell
# Detener (mantiene volúmenes)
docker-compose down

# Detener y eliminar volúmenes (datos se pierden)
docker-compose down -v
```

---

### Opción 2: Solo con Docker

#### Paso 1: Construir la imagen

```powershell
docker build -t quicktask-api:latest .
```

#### Paso 2: Crear volumen para persistencia

```powershell
docker volume create quicktask_db
```

#### Paso 3: Ejecutar el contenedor

```powershell
docker run -d `
  --name quicktask-api `
  -p 8000:8000 `
  -v ${PWD}:/app `
  -v quicktask_db:/app/data `
  quicktask-api:latest
```

#### Paso 4: Ver logs

```powershell
docker logs -f quicktask-api
```

#### Paso 5: Detener y eliminar

```powershell
docker stop quicktask-api
docker rm quicktask-api
```

---

## 🛠️ Comandos Útiles

### Ver logs en tiempo real

```powershell
# Con docker-compose
docker-compose logs -f

# Con docker
docker logs -f quicktask-api
```

### Ejecutar en modo detached (background)

```powershell
docker-compose up -d
```

### Reconstruir imagen forzadamente

```powershell
docker-compose build --no-cache
docker-compose up
```

### Acceder al shell del contenedor

```powershell
# Con docker-compose
docker-compose exec api bash

# Con docker
docker exec -it quicktask-api bash
```

**Dentro del contenedor:**
```bash
# Ver estructura de archivos
ls -la

# Ver base de datos
ls -la data/

# Salir
exit
```

### Ver uso de recursos

```powershell
docker stats quicktask-api
```

### Limpiar todo (contenedores, imágenes, volúmenes)

```powershell
# ⚠️ CUIDADO: Elimina TODO (incluye datos)
docker-compose down -v --rmi all
```

---

## ✅ Verificación y Pruebas

### 1. **Verificar que la API responde**

```powershell
# Endpoint raíz
curl http://localhost:8000/

# Con PowerShell
Invoke-WebRequest -Uri http://localhost:8000/ | Select-Object -ExpandProperty Content
```

**Respuesta esperada:**
```json
{
  "message": "Bienvenido a Tasks API",
  "docs": "/docs",
  "version": "1.0.0"
}
```

### 2. **Crear una tarea de prueba**

```powershell
curl -X POST http://localhost:8000/tasks `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Tarea desde Docker",
    "description": "Probando la API containerizada",
    "completed": false
  }'
```

### 3. **Listar todas las tareas**

```powershell
curl http://localhost:8000/tasks
```

### 4. **Verificar persistencia**

```powershell
# Detener contenedor
docker-compose down

# Volver a levantar
docker-compose up -d

# Listar tareas (deben seguir existiendo)
curl http://localhost:8000/tasks
```

✅ Si las tareas persisten, la configuración de volúmenes funciona correctamente.

### 5. **Verificar hot-reload (desarrollo)**

1. Modifica `main.py` (cambia el mensaje de bienvenida)
2. Guarda el archivo
3. Los logs mostrarán: `Detected file change, reloading...`
4. Refresca http://localhost:8000/ para ver los cambios

---

## 🐛 Troubleshooting

### Problema 1: Puerto 8000 ya está en uso

**Error:**
```
Error starting userland proxy: listen tcp 0.0.0.0:8000: bind: address already in use
```

**Solución:**
```powershell
# Ver qué proceso usa el puerto 8000
netstat -ano | findstr :8000

# Detener el proceso (reemplaza PID)
taskkill /PID <número> /F

# O cambiar el puerto en docker-compose.yml
ports:
  - "8001:8000"  # Cambia a puerto 8001
```

### Problema 2: Cambios en el código no se reflejan

**Solución:**
```powershell
# Reconstruir sin caché
docker-compose build --no-cache
docker-compose up
```

### Problema 3: No se crean las tablas de BD

**Solución:**
```powershell
# Eliminar volumen y recrear
docker-compose down -v
docker-compose up
```

### Problema 4: "Module not found"

**Causa:** Dependencias no instaladas

**Solución:**
```powershell
# Reconstruir imagen
docker-compose build
docker-compose up
```

### Problema 5: Permisos en volúmenes (Linux/Mac)

**Error:**
```
Permission denied: '/app/data/tasks.db'
```

**Solución:**
```bash
# Dar permisos al directorio
chmod -R 777 data/
```

---

## 🌐 Despliegue en Producción

### Cambios necesarios para producción:

#### 1. **Dockerfile de producción**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

# Sin --reload en producción
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### 2. **docker-compose.prod.yml**

```yaml
version: '3.8'

services:
  api:
    image: quicktask-api:prod
    ports:
      - "80:8000"
    volumes:
      - db_data:/app/data
    environment:
      - ENVIRONMENT=production
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 512M

volumes:
  db_data:
```

#### 3. **Ejecutar en producción**

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 Mejores Prácticas

### ✅ Desarrollo

- [x] Hot-reload activado
- [x] Código montado como volumen
- [x] Logs en tiempo real
- [x] Base de datos persistente

### ✅ Producción

- [ ] Desactivar hot-reload
- [ ] Múltiples workers (4+)
- [ ] Usuario no-root
- [ ] Límites de recursos
- [ ] Healthchecks configurados
- [ ] Variables de entorno desde archivos `.env`
- [ ] Logs centralizados
- [ ] HTTPS con reverse proxy (Nginx/Traefik)

---

## 🎯 Flujo de Trabajo Completo

### Para desarrollo diario:

```powershell
# 1. Levantar contenedor
docker-compose up

# 2. Desarrollar (hot-reload automático)
# Edita archivos, los cambios se reflejan automáticamente

# 3. Probar en http://localhost:8000/docs

# 4. Detener cuando termines
# Ctrl+C en la terminal donde corre docker-compose
```

### Para pruebas completas:

```powershell
# 1. Levantar en background
docker-compose up -d

# 2. Ejecutar tests
docker-compose exec api pytest -v

# 3. Ver logs
docker-compose logs -f

# 4. Detener
docker-compose down
```

---

## 📚 Recursos Adicionales

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Best Practices for Python Docker Images](https://docs.docker.com/language/python/build-images/)

---

## 🎉 Resumen Ejecutivo

### Comando rápido para empezar:

```powershell
# Construir y ejecutar
docker-compose up --build

# En otra terminal, probar
curl http://localhost:8000/docs
```

### Ventajas del despliegue con Docker:

✅ **Portabilidad**: Corre igual en cualquier sistema  
✅ **Aislamiento**: No contamina el sistema host  
✅ **Reproducibilidad**: Mismo entorno siempre  
✅ **Escalabilidad**: Fácil de replicar  
✅ **Persistencia**: Datos seguros en volúmenes  

---

## 🔐 Seguridad

### Para producción, considera:

1. **No exponer puerto 8000 directamente** - Usa reverse proxy
2. **Usuario no-root** en el contenedor
3. **Variables sensibles** en `.env` (no en el código)
4. **Escanear imagen** con `docker scan`
5. **Actualizar dependencias** regularmente
6. **Limitar recursos** del contenedor

```powershell
# Escanear vulnerabilidades
docker scan quicktask-api:latest
```

---

**¡Tu API está lista para desplegarse con Docker! 🚀**
