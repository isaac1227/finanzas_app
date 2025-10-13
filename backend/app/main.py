"""
FastAPI Main Application - Clean Architecture
Configuración principal de la app con estructura por capas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Infrastructure imports  
from .infrastructure.config.database import engine
from .infrastructure.database.models import Base

# API imports
from .api import endpoints

# Crear tablas en desarrollo (mantener temporalmente)
#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# ========== APP CONFIGURATION ==========

app = FastAPI(
    title="Finanzas App - Clean Architecture",
    description="API de gestión financiera personal con arquitectura limpia",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "persistAuthorization": True,  # 🔑 Mantiene el token automáticamente
        "displayRequestDuration": True,  # Muestra duración de requests
        "tryItOutEnabled": True,  # Habilita "Try it out" por defecto
    }
)

# ========== MIDDLEWARE ==========

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== ROUTES ==========

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Finanzas App - Clean Architecture",
        "version": "2.0.0",
        "architecture": "Domain-Driven Design",
        "docs": "/docs"
    }

# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "architecture_layers": [
            "🟡 Domain (Entities + Repositories + Services)",
            "🟠 Application (Use Cases + DTOs)", 
            "🔵 Infrastructure (Database + External)",
            "🟢 API (Controllers + Dependencies)"
        ]
    }


# ========== ROUTERS ===========

# Incluir todos los routers modulares
app.include_router(endpoints.auth_endpoints.router)
app.include_router(endpoints.transaccion_endpoints.router)
app.include_router(endpoints.sueldo_endpoints.router)