# Usa una imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos de requisitos de la aplicación en el directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias necesarias (aprovechando el caché de Docker)
RUN pip install --no-cache-dir -r requirements.txt

# Instalar Uvicorn para servir la aplicación FastAPI
RUN pip install --no-cache-dir uvicorn

# Copiar todos los archivos de la aplicación en el contenedor
COPY . .

# Exponer el puerto que utilizará la aplicación
EXPOSE 8000

# Variables de entorno para configurar FastAPI
ENV FASTAPI_ENV=production

# Añadir una variable de entorno de Python para evitar la creación de archivos pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Añadir una variable de entorno de Python para hacer los logs sin buffer
ENV PYTHONUNBUFFERED=1

# Limpiar archivos temporales (opcional para reducir el tamaño de la imagen)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

