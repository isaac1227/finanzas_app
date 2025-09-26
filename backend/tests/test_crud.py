# backend/tests/test_crud.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas
from datetime import datetime

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_crear_transaccion(db):
    # Arrange
    transaccion_data = schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=50.0,
        descripcion="Test transacción"
    )
    
    # Act
    transaccion = crud.crear_transaccion(db, transaccion_data)
    
    # Assert
    assert transaccion.tipo == "gasto"
    assert transaccion.cantidad == 50.0
    assert transaccion.descripcion == "Test transacción"
    assert transaccion.id is not None

def test_obtener_transacciones_vacio(db):
    transaccion = crud.obtener_transacciones(db)

    assert len(transaccion) == 0


def test_obtener_transacciones_con_datos(db):
    # Arrange
    transaccion_data = schemas.TransaccionCreate(
        tipo="ingreso",
        cantidad=100.0,
        descripcion="Test ingreso"
    )

    crud.crear_transaccion(db, transaccion_data)

    transacciones = crud.obtener_transacciones(db)

    assert len(transacciones) == 1
    assert transacciones[0].tipo == "ingreso"
    assert transacciones[0].cantidad == 100.0
    assert transacciones[0].descripcion == "Test ingreso"

def test_obtener_transacciones_totales_mes_sin_incluir_mes_anio(db):
    "Obtener totales de ingresos y gastos del mes sin incluir mes/año específicos"
    transaccion1 = schemas.TransaccionCreate(
        tipo="ingreso",
        cantidad=200.0,
        descripcion="Ingreso 1"
    )

    transaccion2 = schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=80.0,
        descripcion="Gasto 1"
    )

    crud.crear_transaccion(db, transaccion1)
    crud.crear_transaccion(db, transaccion2)

    ingresos, gastos = crud.obtener_transacciones_totales_mes(db, mes=None, anio=None)

    assert ingresos == 200.0
    assert gastos == 80.0

def test_obtener_transacciones_totales_mes(db):
    "Obtener totales de ingresos y gastos del mes específico"
    transaccion1 = schemas.TransaccionCreate(
        tipo="ingreso",
        cantidad=200.0,
        descripcion="Ingreso 1"
    )

    transaccion2 = schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=80.0,
        descripcion="Gasto 1"
    )

    crud.crear_transaccion(db, transaccion1, fecha_custom=datetime(2025, 9, 15))
    crud.crear_transaccion(db, transaccion2, fecha_custom=datetime(2025, 10, 20))

    ingresos, gastos = crud.obtener_transacciones_totales_mes(db, mes=9, anio=2025)
    ingresos_oct, gastos_oct = crud.obtener_transacciones_totales_mes(db, mes=10, anio=2025)

    assert ingresos == 200.0
    assert gastos_oct == 80.0
    assert gastos == 0.0
    assert ingresos_oct == 0.0