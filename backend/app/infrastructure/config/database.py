"""
Configuración de base de datos - Infrastructure Layer
Esta configuración específica usa PostgreSQL + SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de BD - específico para PostgreSQL
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos ORM (solo para infrastructure)
Base = declarative_base()


def get_db():
    """
    Dependencia para inyectar sesión en endpoints FastAPI
    Se usará en la capa API para obtener conexión a BD
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()