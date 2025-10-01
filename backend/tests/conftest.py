import pytest
import sys
import os
import tempfile
import atexit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  
from fastapi.testclient import TestClient
from datetime import datetime

# Agregar el directorio backend al path
# Desde tests/ necesitamos ir a backend/ que es el padre
backend_dir = os.path.dirname(os.path.abspath(__file__))  # tests/
backend_dir = os.path.dirname(backend_dir)  # backend/
sys.path.insert(0, backend_dir)
print(f"🔍 DEBUG: Backend dir añadido al path: {backend_dir}")

from app.database import Base, get_db
from app import models  # ← Esto registra los modelos
from app.main import app
from app import crud, schemas

# ========== BD GLOBAL PARA TODOS LOS TESTS ==========
# Crear BDD termporal para SQLite
TEST_DB_FILE = tempfile.mktemp(suffix='.db')
TEST_ENGINE = create_engine(
    f"sqlite:///{TEST_DB_FILE}", 
    connect_args={"check_same_thread": False},
    echo=False,  # Cambiar a True para debug
)

# Crea las tablas en base a la definicion de app/models.py 
Base.metadata.create_all(bind=TEST_ENGINE)
TEST_SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

# Verificar tablas
from sqlalchemy import inspect
inspector = inspect(TEST_ENGINE)
tables = inspector.get_table_names()
print(f"🔧 BD test creada con tablas: {tables}")

# Limpiar archivo temporal al finalizar
def cleanup_test_db():
    try:
        os.unlink(TEST_DB_FILE)
    except:
        pass

atexit.register(cleanup_test_db)

# ========== FIXTURES ==========
@pytest.fixture(scope="function")
def db_session():
    """Sesión de BD limpia para cada test"""
    
    # Limpiar tablas antes de cada test
    with TEST_ENGINE.connect() as conn:
        trans = conn.begin()
        try:
            conn.execute(Base.metadata.tables["transacciones"].delete())
            conn.execute(Base.metadata.tables["sueldos"].delete())
            trans.commit()
        except:
            trans.rollback()
    
    # Crear nueva sesión usando el engine global
    db = TEST_SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def db(db_session):
    """Para tests CRUD"""
    return db_session

@pytest.fixture 
def test_db(db_session):
    """Para tests API"""
    return db_session

@pytest.fixture
def client_with_test_db(db_session):
    """Cliente FastAPI con BD de test"""
    
    def override_get_db():
        """Override que devuelve la sesión del test"""
        try:
            yield db_session
        finally:
            pass  # No cerrar la sesión aquí
    
    # Aplicar override
    app.dependency_overrides[get_db] = override_get_db
    
    try:
        # Crear cliente
        with TestClient(app) as client:
            yield client
    finally:
        # Limpiar override
        app.dependency_overrides.clear()

# ========== FIXTURES DE DATOS ==========
@pytest.fixture
def sample_transaccion():
    return schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=50.0,
        descripcion="Transacción de prueba"
    )

@pytest.fixture
def sample_transaccion_dict():
    return {
        "tipo": "gasto", 
        "cantidad": 50.0,
        "descripcion": "Transacción de prueba"
    }

@pytest.fixture
def sample_sueldo():
    return schemas.SueldoCreate(
        cantidad=2000.0,
        mes=9,
        anio=2025
    )

@pytest.fixture
def sample_sueldo_dict():
    return {
        "cantidad": 2000.0,
        "mes": 9, 
        "anio": 2025
    }

@pytest.fixture
def fecha_septiembre():
    return datetime(2025, 9, 15, 12, 0, 0)

@pytest.fixture
def transacciones_multiples(db, fecha_septiembre):
    """Para tests CRUD"""
    transacciones_data = [
        schemas.TransaccionCreate(tipo="ingreso", cantidad=200.0, descripcion="Ingreso 1"),
        schemas.TransaccionCreate(tipo="gasto", cantidad=80.0, descripcion="Gasto 1"),
        schemas.TransaccionCreate(tipo="gasto", cantidad=30.0, descripcion="Gasto 2"),
    ]
    
    transacciones_creadas = []
    for t_data in transacciones_data:
        t = crud.crear_transaccion(db, t_data, fecha_custom=fecha_septiembre)
        transacciones_creadas.append(t)
    
    return transacciones_creadas