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

def test_crear_transaccion_con_fecha_custom(db):
    fecha_custom = datetime(2025, 8, 20)
    transaccion_data = schemas.TransaccionCreate(tipo="gasto", cantidad=50.0)
    
    transaccion = crud.crear_transaccion(db, transaccion_data, fecha_custom=fecha_custom)
    
    assert transaccion.fecha.month == 8
    assert transaccion.fecha.day == 20

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

def test_actualizar_transaccion(db):
    # Arrange
    transaccion_data = schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=50.0,
        descripcion="Transacción a actualizar"
    )

    transaccion = crud.crear_transaccion(db, transaccion_data)

    transaccion_update = schemas.TransaccionUpdate(
        tipo="ingreso",
        cantidad=150.0,
        descripcion="Transacción actualizada"
    )

    crud.actualizar_transaccion(db, transaccion.id, transaccion_update)

    # Assert
    transaccion_actualizada = crud.obtener_transacciones(db, skip=0, limit=100)[0]
    assert transaccion_actualizada.tipo == "ingreso"
    assert transaccion_actualizada.cantidad == 150.0
    assert transaccion_actualizada.descripcion == "Transacción actualizada"

def test_actualizar_transaccion_inexistente(db):
    update_data = schemas.TransaccionUpdate(cantidad=100.0)
    resultado = crud.actualizar_transaccion(db, 999, update_data)
    assert resultado is None

def test_eliminar_transaccion(db):
    transaccion_data = schemas.TransaccionCreate(
        tipo="gasto",
        cantidad=70.0,
        descripcion="Transacción a eliminar"
    )

    transaccion = crud.crear_transaccion(db, transaccion_data)
    transaccion_eliminada = crud.eliminar_transaccion(db, transaccion.id)
    transacciones_restantes = crud.obtener_transacciones(db)

    assert transaccion_eliminada.id == transaccion.id
    assert len(transacciones_restantes) == 0

def test_eliminar_transaccion_inexistente(db):
    resultado = crud.eliminar_transaccion(db, 999)
    assert resultado is None

def test_crear_o_actualizar_sueldo(db):
    sueldo_data = schemas.SueldoCreate(
        cantidad=1500.0,
        mes=9,
        anio=2025
    )

    sueldo = crud.crear_o_actualizar_sueldo(db, sueldo_data)

    assert sueldo.cantidad == 1500.0
    assert sueldo.mes == 9
    assert sueldo.anio == 2025

    # Actualizar el mismo mes/año
    sueldo_data_update = schemas.SueldoCreate(
        cantidad=1800.0,
        mes=9,
        anio=2025
    )

    sueldo_actualizado = crud.crear_o_actualizar_sueldo(db, sueldo_data_update)

    assert sueldo_actualizado.id == sueldo.id
    assert sueldo_actualizado.cantidad == 1800.0

def test_obtener_sueldo_mes(db):
    sueldo_data = schemas.SueldoCreate(
        cantidad=1500.0,
        mes=10,
        anio=2025
    )

    crud.crear_o_actualizar_sueldo(db, sueldo_data)

    sueldo_obtenido = crud.obtener_sueldo_mes(db, mes=10, anio=2025)

    assert sueldo_obtenido is not None
    assert sueldo_obtenido.cantidad == 1500.0
    assert sueldo_obtenido.mes == 10
    assert sueldo_obtenido.anio == 2025

def test_obtener_sueldos(db):
    sueldo1 = schemas.SueldoCreate(
        cantidad=1500,
        mes=9,
        anio=2025
    )

    sueldo2 = schemas.SueldoCreate(
        cantidad=1600,
        mes=10,
        anio=2025
    )

    crud.crear_o_actualizar_sueldo(db, sueldo1)
    crud.crear_o_actualizar_sueldo(db, sueldo2)

    sueldos = crud.obtener_sueldos(db)

    assert len(sueldos) == 2
    assert sueldos[0].cantidad == 1600
    assert sueldos[1].cantidad == 1500
    assert sueldos[0].mes == 10
    assert sueldos[1].mes == 9

def test_obtener_sueldo_mes_no_existe(db):
    sueldo_obtenido = crud.obtener_sueldo_mes(db, mes=11, anio=2025)
    assert sueldo_obtenido is None

def test_obtener_sueldos_vacio(db):
    sueldos = crud.obtener_sueldos(db)
    assert len(sueldos) == 0

def test_obtener_transacciones_filtrado_mes_anio(db):
    # Crear transacciones en diferentes meses
    t1 = schemas.TransaccionCreate(tipo="gasto", cantidad=100.0)
    t2 = schemas.TransaccionCreate(tipo="ingreso", cantidad=200.0)
    
    crud.crear_transaccion(db, t1, fecha_custom=datetime(2025, 9, 15))
    crud.crear_transaccion(db, t2, fecha_custom=datetime(2025, 10, 15))
    
    # Solo septiembre
    trans_sep = crud.obtener_transacciones(db, mes=9, anio=2025)
    assert len(trans_sep) == 1
    assert trans_sep[0].cantidad == 100.0