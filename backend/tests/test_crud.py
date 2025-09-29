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

def test_crear_transaccion(db, sample_transaccion):
    """Test crear transacción básica"""
    transaccion = crud.crear_transaccion(db, sample_transaccion)
    
    assert transaccion.tipo == "gasto"
    assert transaccion.cantidad == 50.0
    assert transaccion.descripcion == "Transacción de prueba"
    assert transaccion.id is not None

def test_crear_transaccion_con_fecha_custom(db, sample_transaccion, fecha_septiembre):
    """Test crear transacción con fecha específica"""
    transaccion = crud.crear_transaccion(db, sample_transaccion, fecha_custom=fecha_septiembre)
    
    assert transaccion.fecha.month == 9
    assert transaccion.fecha.day == 15
    assert transaccion.cantidad == 50.0

def test_obtener_transacciones_vacio(db):
    """Test obtener transacciones cuando no hay ninguna"""
    transacciones = crud.obtener_transacciones(db)
    assert len(transacciones) == 0

def test_obtener_multiples_transacciones_con_datos(db, transacciones_multiples):
    """Test obtener transacciones cuando hay múltiples datos"""
    transacciones = crud.obtener_transacciones(db)
    
    assert len(transacciones) == 3
    tipos = [t.tipo for t in transacciones]
    assert "ingreso" in tipos
    assert "gasto" in tipos

def test_obtener_transacciones_totales_mes_sin_incluir_mes_anio(db):
    """Obtener totales de ingresos y gastos del mes sin incluir mes/año específicos"""
    ingresos, gastos = crud.obtener_transacciones_totales_mes(db)
    assert ingresos == 0.0
    assert gastos == 0.0

def test_obtener_transacciones_totales_mes(db):
    """Obtener totales de ingresos y gastos del mes específico"""
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

def test_actualizar_transaccion(db, sample_transaccion):
    """Test actualizar una transacción existente"""
    # Arrange - Crear transacción original
    transaccion = crud.crear_transaccion(db, sample_transaccion)

    # Datos actualizados
    transaccion_update = schemas.TransaccionUpdate(
        tipo="ingreso",
        cantidad=150.0,
        descripcion="Transacción actualizada"
    )

    # Act
    transaccion_actualizada = crud.actualizar_transaccion(db, transaccion.id, transaccion_update)

    # Assert
    assert transaccion_actualizada.tipo == "ingreso"
    assert transaccion_actualizada.cantidad == 150.0
    assert transaccion_actualizada.descripcion == "Transacción actualizada"
    assert transaccion_actualizada.id == transaccion.id

def test_actualizar_transaccion_inexistente(db):
    """Test actualizar transacción que no existe"""
    update_data = schemas.TransaccionUpdate(cantidad=100.0)
    resultado = crud.actualizar_transaccion(db, 999, update_data)
    assert resultado is None

def test_eliminar_transaccion(db, sample_transaccion):
    """Test eliminar una transacción"""
    # Arrange - Crear transacción
    transaccion = crud.crear_transaccion(db, sample_transaccion)

    # Act
    transaccion_eliminada = crud.eliminar_transaccion(db, transaccion.id)

    # Assert
    assert transaccion_eliminada.id == transaccion.id
    transacciones_restantes = crud.obtener_transacciones(db)
    assert len(transacciones_restantes) == 0

def test_eliminar_transaccion_inexistente(db):
    """Test eliminar transacción que no existe"""
    resultado = crud.eliminar_transaccion(db, 999)
    assert resultado is None

def test_crear_o_actualizar_sueldo(db, sample_sueldo):
    """Test crear y actualizar sueldo"""
    # Crear sueldo
    sueldo = crud.crear_o_actualizar_sueldo(db, sample_sueldo)
    
    assert sueldo.cantidad == 2000.0
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

def test_obtener_sueldo_mes(db, sample_sueldo):
    """Test obtener sueldo de un mes específico"""
    sueldo_data = crud.crear_o_actualizar_sueldo(db, sample_sueldo)
    sueldo_obtenido = crud.obtener_sueldo_mes(db, mes=9, anio=2025)

    assert sueldo_obtenido is not None
    assert sueldo_obtenido.cantidad == 2000.0
    assert sueldo_obtenido.mes == 9
    assert sueldo_obtenido.anio == 2025

def test_obtener_sueldos(db):
    """Test obtener lista de sueldos ordenada"""
    sueldo1 = schemas.SueldoCreate(cantidad=1500, mes=9, anio=2025)
    sueldo2 = schemas.SueldoCreate(cantidad=1600, mes=10, anio=2025)

    crud.crear_o_actualizar_sueldo(db, sueldo1)
    crud.crear_o_actualizar_sueldo(db, sueldo2)

    sueldos = crud.obtener_sueldos(db)

    assert len(sueldos) == 2
    # Verificar orden (más reciente primero)
    assert sueldos[0].cantidad == 1600
    assert sueldos[1].cantidad == 1500
    assert sueldos[0].mes == 10
    assert sueldos[1].mes == 9

def test_obtener_sueldo_mes_no_existe(db):
    """Test obtener sueldo de un mes que no existe"""
    sueldo_obtenido = crud.obtener_sueldo_mes(db, mes=11, anio=2025)
    assert sueldo_obtenido is None

def test_obtener_sueldos_vacio(db):
    """Test obtener sueldos cuando no hay ninguno"""
    sueldos = crud.obtener_sueldos(db)
    assert len(sueldos) == 0

def test_obtener_transacciones_filtrado_mes_anio(db):
    """Test filtrar transacciones por mes y año específicos"""
    # Crear transacciones en diferentes meses
    t1 = schemas.TransaccionCreate(tipo="gasto", cantidad=100.0, descripcion="Septiembre")
    t2 = schemas.TransaccionCreate(tipo="ingreso", cantidad=200.0, descripcion="Octubre")
    
    crud.crear_transaccion(db, t1, fecha_custom=datetime(2025, 9, 15))
    crud.crear_transaccion(db, t2, fecha_custom=datetime(2025, 10, 15))
    
    # Solo septiembre
    trans_sep = crud.obtener_transacciones(db, mes=9, anio=2025)
    assert len(trans_sep) == 1
    assert trans_sep[0].cantidad == 100.0
    assert trans_sep[0].descripcion == "Septiembre"
    
    # Solo octubre
    trans_oct = crud.obtener_transacciones(db, mes=10, anio=2025)
    assert len(trans_oct) == 1
    assert trans_oct[0].cantidad == 200.0
    assert trans_oct[0].descripcion == "Octubre"