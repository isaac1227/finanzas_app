import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from datetime import datetime

# Cliente de prueba para FastAPI
client = TestClient(app)

def test_root_endpoint():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenido a tu app de finanzas"}

# Tests de Transacciones
def test_crear_transaccion():
    """Test crear transacción via API"""
    transaccion_data = {
        "tipo": "gasto",
        "cantidad": 50.0,
        "descripcion": "Transacción de prueba"
    }
    response = client.post("/transacciones", json=transaccion_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == transaccion_data["tipo"]
    assert data["cantidad"] == transaccion_data["cantidad"]
    assert data["descripcion"] == transaccion_data["descripcion"]
    assert "id" in data
    assert "fecha" in data

def test_crear_transaccion_con_fecha():
    """Test crear transacción con fecha específica"""
    transaccion_data = {
        "tipo": "ingreso",
        "cantidad": 150.0,
        "descripcion": "Ingreso con fecha",
        "fecha": "2025-09-15T14:30:00"
    }
    
    response = client.post("/transacciones", json=transaccion_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "ingreso"
    assert data["cantidad"] == 150.0
    assert "2025-09-15" in data["fecha"]

def test_obtener_transacciones():
    """Test obtener lista de transacciones"""
    # Crear una transacción primero
    client.post("/transacciones", json={
        "tipo": "gasto",
        "cantidad": 25.0,
        "descripcion": "Test obtener"
    })
    
    response = client.get("/transacciones")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obtener_transacciones_con_filtros():
    """Test obtener transacciones filtradas por mes/año"""
    response = client.get("/transacciones?mes=9&anio=2025")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_actualizar_transaccion():
    """Test actualizar transacción existente"""
    # Crear transacción
    create_response = client.post("/transacciones", json={
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
    response = client.put(f"/transacciones/{transaccion_id}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["tipo"] == "ingreso"
    assert data["cantidad"] == 200.0
    assert data["descripcion"] == "Actualizada"
    assert data["id"] == transaccion_id

def test_actualizar_transaccion_inexistente():
    """Test actualizar transacción que no existe"""
    update_data = {
        "tipo": "gasto",
        "cantidad": 50.0
    }
    response = client.put("/transacciones/999", json=update_data)
    
    assert response.status_code == 404
    assert "no encontrada" in response.json()["detail"].lower()

def test_eliminar_transaccion():
    """Test eliminar transacción"""
    # Crear transacción
    create_response = client.post("/transacciones", json={
        "tipo": "gasto",
        "cantidad": 30.0,
        "descripcion": "Para eliminar"
    })
    transaccion_id = create_response.json()["id"]
    
    # Eliminar
    response = client.delete(f"/transacciones/{transaccion_id}")
    
    assert response.status_code == 200
    data = response.json()

def test_eliminar_transaccion_inexistente():
    """Test eliminar transacción que no existe"""
    response = client.delete("/transacciones/999")
    
    assert response.status_code == 404
    assert "Transacción no encontrada" in response.json()["detail"]

# Tests de Sueldos
def test_crear_sueldo():
    """Test crear sueldo via API"""
    sueldo_data = {
        "cantidad": 2500.0,
        "mes": 9,
        "anio": 2025
    }
    
    response = client.post("/sueldos", json=sueldo_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 2500.0
    assert data["mes"] == 9
    assert data["anio"] == 2025
    assert "id" in data

def test_obtener_sueldo_especifico():
    """Test obtener sueldo de mes/año específico"""
    # Crear sueldo primero
    client.post("/sueldos", json={
        "cantidad": 1800.0,
        "mes": 10,
        "anio": 2025
    })
    
    response = client.get("/sueldos/2025/10")
    
    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 1800.0
    assert data["mes"] == 10
    assert data["anio"] == 2025

def test_obtener_sueldo_inexistente():
    """Test obtener sueldo que no existe"""
    response = client.get("/sueldos/2025/12")

    assert response.status_code == 404
    data = response.json()
    assert "no encontrado" in data["detail"].lower()
    assert "12" in data["detail"]  # Verificar que incluye el mes
    assert "2025" in data["detail"]  # Verificar que incluye el año

def test_obtener_todos_los_sueldos():
    """Test obtener lista de todos los sueldos"""
    response = client.get("/sueldos")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_actualizar_sueldo_existente():
    """Test actualizar sueldo del mismo mes/año"""
    # Crear sueldo
    client.post("/sueldos", json={
        "cantidad": 2000.0,
        "mes": 11,
        "anio": 2025
    })
    
    # Actualizar mismo mes/año
    response = client.post("/sueldos", json={
        "cantidad": 2200.0,
        "mes": 11,
        "anio": 2025
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["cantidad"] == 2200.0  # Valor actualizado

# Tests de validación
def test_crear_transaccion_datos_invalidos():
    """Test crear transacción con datos inválidos"""
    # Cantidad negativa
    response = client.post("/transacciones", json={
        "tipo": "gasto",  # ← Corregir: era "gasta" 
        "cantidad": -50.0,
        "descripcion": "Cantidad negativa"
    })
    
    assert response.status_code == 422

def test_crear_transaccion_tipo_invalido():
    """Test crear transacción con tipo inválido"""
    response = client.post("/transacciones", json={
        "tipo": "invalido",
        "cantidad": 50.0,
        "descripcion": "Tipo inválido"
    })
    
    assert response.status_code == 422

def test_crear_sueldo_datos_invalidos():
    """Test crear sueldo con datos inválidos"""
    # Mes inválido
    response = client.post("/sueldos", json={
        "cantidad": 2000.0,
        "mes": 13,  # Mes inválido
        "anio": 2025
    })
    
    assert response.status_code == 422

# Tests de casos edge
def test_transacciones_sin_descripcion():
    """Test crear transacción sin descripción (permitido)"""
    response = client.post("/transacciones", json={
        "tipo": "ingreso",
        "cantidad": 100.0
        # Sin descripción - debería funcionar
    })
    
    assert response.status_code == 200  
    data = response.json()
    assert data["descripcion"] is None

def test_obtener_transacciones_con_limite():
    """Test obtener transacciones con parámetros limit/skip"""
    # Crear varias transacciones
    for i in range(5):
        client.post("/transacciones", json={
            "tipo": "gasto",
            "cantidad": 10.0 + i,
            "descripcion": f"Transacción {i}"
        })
    
    # Obtener con límite
    response = client.get("/transacciones?skip=2&limit=2")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2