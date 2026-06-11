# 1. Imagen base oficial de Python (versión ligera para producción)
FROM python:3.12-slim

# 2. Evita que Python escriba archivos .pyc en el disco y asegura que los prints salgan directo a la terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instala dependencias del sistema necesarias para compilar ciertas librerías o conectar BD
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia e instala los requerimientos de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 6. Instala Gunicorn para el despliegue de producción
RUN pip install --no-cache-dir gunicorn

# 7. Copia todo el código de nuestro Prode al contenedor
COPY . /app/

# 8. Expone el puerto por donde escuchará Gunicorn
EXPOSE 8000