import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app
from app import crud, schemas
from datetime import datetime

# ========== FIXTURES PARA TEST_CRUD (BD directa) ==========
@pytest.fixture
def db():
    """Fixture para tests de CRUD (acceso directo a BD)"""
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture  
def client_with_test_db(test_db):
    """Cliente que usa BD de test en lugar de la real"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

# ========== FIXTURES DE DATOS (para ambos tipos de test) ==========
@pytest.fixture
def sample_transaccion():
    """Fixture con datos de transacción (para test_crud.py)"""
    return schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=50.0,
        descripcion="Transacción de prueba"
    )

@pytest.fixture
def sample_transaccion_dict():
    """Fixture con datos de transacción como dict (para test_main.py)"""
    return {
        "tipo": "gasto",
        "cantidad": 50.0,
        "descripcion": "Transacción de prueba"
    }

@pytest.fixture
def sample_sueldo():
    """Fixture con datos de sueldo (para test_crud.py)"""
    return schemas.SueldoCreate(
        cantidad=2000.0,
        mes=9,
        anio=2025
    )

@pytest.fixture
def sample_sueldo_dict():
    """Fixture con datos de sueldo como dict (para test_main.py)"""
    return {
        "cantidad": 2000.0,
        "mes": 9,
        "anio": 2025
    }

@pytest.fixture
def fecha_septiembre():
    """Fixture con fecha de septiembre para tests"""
    return datetime(2025, 9, 15, 12, 0, 0)

@pytest.fixture
def transacciones_multiples(db, fecha_septiembre):
    """Fixture que crea varias transacciones de ejemplo (para test_crud.py)"""
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