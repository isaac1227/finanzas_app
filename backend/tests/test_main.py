import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from datetime import datetime

def test_root_endpoint(client_with_test_db):
    """Test del endpoint raíz"""
    response = client_with_test_db.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a tu app de finanzas"}

# Tests de Transacciones
def test_crear_transaccion(client_with_test_db):
    """Test crear transacción via API"""
    transaccion_data = {
        "tipo": "gasto",
        "cantidad": 50.0,
        "descripcion": "Transacción de prueba"
    }
    response = client_with_test_db.post("/transacciones", json=transaccion_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == transaccion_data["tipo"]
    assert data["cantidad"] == transaccion_data["cantidad"]
    assert data["descripcion"] == transaccion_data["descripcion"]
    assert "id" in data
    assert "fecha" in data

def test_crear_transaccion_con_fecha(client_with_test_db):
    """Test crear transacción con fecha específica"""
    transaccion_data = {
        "tipo": "ingreso",
        "cantidad": 150.0,
        "descripcion": "Ingreso con fecha",
        "fecha": "2025-09-15T14:30:00"
    }
    
    response = client_with_test_db.post("/transacciones", json=transaccion_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "ingreso"
    assert data["cantidad"] == 150.0
    assert "2025-09-15" in data["fecha"]

def test_obtener_transacciones(client_with_test_db):
    """Test obtener lista de transacciones"""
    # Crear una transacción primero
    client_with_test_db.post("/transacciones", json={
        "tipo": "gasto",
        "cantidad": 25.0,
        "descripcion": "Test obtener"
    })
    
    response = client_with_test_db.get("/transacciones")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obtener_transacciones_con_filtros(client_with_test_db):
    """Test obtener transacciones filtradas por mes/año"""
    response = client_with_test_db.get("/transacciones?mes=9&anio=2025")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_actualizar_transaccion(client_with_test_db):
    """Test actualizar transacción existente"""
    # Crear transacción
    create_response = client_with_test_db.post("/transacciones", json={
        "tipo": "gasto",
        "cantidad": 100.0,
        "descripcion": "Original"
    })
    transaccion_id = create_response.json()["id"]
    
    # Actualizar
    update_data = {
        "tipo": "ingreso",
        "cantidad": 200.0,
        "descripcion": "Actualizada"
    }
    response = client_with_test_db.put(f"/transacciones/{transaccion_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "ingreso"
    assert data["cantidad"] == 200.0
    assert data["descripcion"] == "Actualizada"
    assert data["id"] == transaccion_id

def test_actualizar_transaccion_inexistente(client_with_test_db):
    """Test actualizar transacción que no existe"""
    update_data = {
        "tipo": "gasto",
        "cantidad": 50.0
    }
    response = client_with_test_db.put("/transacciones/999", json=update_data)
    
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"].lower()

def test_eliminar_transaccion(client_with_test_db):
    """Test eliminar transacción"""
    # Crear transacción
    create_response = client_with_test_db.post("/transacciones", json={
        "tipo": "gasto",
        "cantidad": 30.0,
        "descripcion": "Para eliminar"
    })
    transaccion_id = create_response.json()["id"]
    
    # Eliminar
    response = client_with_test_db.delete(f"/transacciones/{transaccion_id}")
    
    assert response.status_code == 200
    data = response.json()

def test_eliminar_transaccion_inexistente(client_with_test_db):
    """Test eliminar transacción que no existe"""
    response = client_with_test_db.delete("/transacciones/999")
    
    assert response.status_code == 404
    assert "Transacción no encontrada" in response.json()["detail"]

# Tests de Sueldos
def test_crear_sueldo(client_with_test_db):
    """Test crear sueldo via API"""
    sueldo_data = {
        "cantidad": 2500.0,
        "mes": 9,
        "anio": 2025
    }
    
    response = client_with_test_db.post("/sueldos", json=sueldo_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 2500.0
    assert data["mes"] == 9
    assert data["anio"] == 2025
    assert "id" in data

def test_obtener_sueldo_especifico(client_with_test_db):
    """Test obtener sueldo de mes/año específico"""
    # Crear sueldo primero
    client_with_test_db.post("/sueldos", json={
        "cantidad": 1800.0,
        "mes": 10,
        "anio": 2025
    })
    
    response = client_with_test_db.get("/sueldos/2025/10")
    
    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 1800.0
    assert data["mes"] == 10
    assert data["anio"] == 2025

def test_obtener_sueldo_inexistente(client_with_test_db):
    """Test obtener sueldo que no existe"""
    response = client_with_test_db.get("/sueldos/2025/12")

    assert response.status_code == 404
    data = response.json()
    assert "no encontrado" in data["detail"].lower()
    assert "12" in data["detail"]  # Verificar que incluye el mes
    assert "2025" in data["detail"]  # Verificar que incluye el año

def test_obtener_todos_los_sueldos(client_with_test_db):
    """Test obtener lista de todos los sueldos"""
    response = client_with_test_db.get("/sueldos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_actualizar_sueldo_existente(client_with_test_db):
    """Test actualizar sueldo del mismo mes/año"""
    # Crear sueldo
    client_with_test_db.post("/sueldos", json={
        "cantidad": 2000.0,
        "mes": 11,
        "anio": 2025
    })
    
    # Actualizar mismo mes/año
    response = client_with_test_db.post("/sueldos", json={
        "cantidad": 2200.0,
        "mes": 11,
        "anio": 2025
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 2200.0  # Valor actualizado

# Tests de validación
def test_crear_transaccion_datos_invalidos(client_with_test_db):
    """Test crear transacción con datos inválidos"""
    # Cantidad negativa
    response = client_with_test_db.post("/transacciones", json={
        "tipo": "gasto",  # ← Corregir: era "gasta" 
        "cantidad": -50.0,
        "descripcion": "Cantidad negativa"
    })
    
    assert response.status_code == 422

def test_crear_transaccion_tipo_invalido(client_with_test_db):
    """Test crear transacción con tipo inválido"""
    response = client_with_test_db.post("/transacciones", json={
        "tipo": "invalido",
        "cantidad": 50.0,
        "descripcion": "Tipo inválido"
    })
    
    assert response.status_code == 422

def test_crear_sueldo_datos_invalidos(client_with_test_db):
    """Test crear sueldo con datos inválidos"""
    # Mes inválido
    response = client_with_test_db.post("/sueldos", json={
        "cantidad": 2000.0,
        "mes": 13,  # Mes inválido
        "anio": 2025
    })
    
    assert response.status_code == 422

# Tests de casos edge
def test_transacciones_sin_descripcion(client_with_test_db):
    """Test crear transacción sin descripción (permitido)"""
    response = client_with_test_db.post("/transacciones", json={
        "tipo": "ingreso",
        "cantidad": 100.0
        # Sin descripción - debería funcionar
    })
    
    assert response.status_code == 200  
    data = response.json()
    assert data["descripcion"] is None

def test_obtener_transacciones_con_limite(client_with_test_db):
    """Test obtener transacciones con parámetros limit/skip"""
    # Crear varias transacciones
    for i in range(5):
        client_with_test_db.post("/transacciones", json={
            "tipo": "gasto",
            "cantidad": 10.0 + i,
            "descripcion": f"Transacción {i}"
        })
    
    # Obtener con límite
    response = client_with_test_db.get("/transacciones?skip=2&limit=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2

def test_verificar_bd_funciona(client_with_test_db, test_db):
    """Test para verificar que la BD funciona correctamente"""
    from sqlalchemy import text
    
    # 1. Verificar BD vacía
    count = test_db.execute(text("SELECT COUNT(*) FROM transacciones")).scalar()
    print(f"📊 BD inicial: {count} transacciones")
    assert count == 0
    
    # 2. Crear via API
    response = client_with_test_db.post("/transacciones", json={
        "tipo": "gasto",
        "cantidad": 100.0,
        "descripcion": "Test API"
    })
    
    print(f"🌐 API Response: {response.status_code}")
    assert response.status_code == 200
    
    # 3. Verificar en BD
    count = test_db.execute(text("SELECT COUNT(*) FROM transacciones")).scalar()
    print(f"📊 BD después API: {count} transacciones")
    assert count == 1
    
    print("✅ BD SQLite temporal funciona correctamente!")