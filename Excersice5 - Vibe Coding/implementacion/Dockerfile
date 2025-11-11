# Usa imagen oficial de Python 3.11 slim (más ligera)
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Establece variables de entorno
# Previene que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que la salida de Python se envíe directamente al terminal
ENV PYTHONUNBUFFERED=1

# Copia el archivo de dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación al contenedor
COPY . .

# Crea directorio para la base de datos si no existe
RUN mkdir -p /app/data

# Expone el puerto 8000 (puerto por defecto de FastAPI)
EXPOSE 8000

# Define el comando por defecto para ejecutar la aplicación
# --host 0.0.0.0 permite conexiones desde fuera del contenedor
# --port 8000 especifica el puerto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
