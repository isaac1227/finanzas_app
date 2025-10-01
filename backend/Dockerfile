# 🐍 Backend Dockerfile - FastAPI + PostgreSQL
FROM python:3.11-slim

# 📋 Metadatos
LABEL maintainer="isaac1227"
LABEL description="Finanzas App - Backend API con FastAPI"
LABEL version="1.0.0"

# 🔧 Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# 📂 Crear directorio de trabajo
WORKDIR /app

# 📦 Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 📥 Copiar archivos de dependencias primero (para cache layer)
COPY requirements.txt .

# 🔧 Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 📁 Copiar código fuente
COPY . .

# 👤 Crear usuario no-root para seguridad
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 🌐 Exponer puerto
EXPOSE 8000

# 🏥 Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# 🚀 Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]