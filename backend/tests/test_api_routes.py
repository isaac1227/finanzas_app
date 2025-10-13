# backend/tests/test_api_routes.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- AUTH ---
def test_register_and_login():
    # Email único por test
    email = f"apiuser_{os.urandom(4).hex()}@correo.com"
    # Registro
    response = client.post("/auth/register", json={"email": email, "password": "apipass123"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["is_active"] is True
    # Login (OAuth2PasswordRequestForm)
    response = client.post("/auth/token", data={"username": email, "password": "apipass123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token
    # Perfil
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    perfil = response.json()
    assert perfil["email"] == email

# --- SUELDOS ---
def test_sueldo_routes():
    email = f"sueldo_{os.urandom(4).hex()}@correo.com"
    # Registro y login para obtener token
    client.post("/auth/register", json={"email": email, "password": "sueldo123"})
    login = client.post("/auth/token", data={"username": email, "password": "sueldo123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Crear sueldo
    response = client.post("/sueldos/", json={"cantidad": 2500.0, "mes": 10, "anio": 2025}, headers=headers)
    assert response.status_code == 200
    sueldo = response.json()
    assert sueldo["cantidad"] == 2500.0
    assert sueldo["mes"] == 10
    assert sueldo["anio"] == 2025
    # Obtener sueldo
    response = client.get("/sueldos/2025/10", headers=headers)
    assert response.status_code == 200
    sueldo = response.json()
    assert sueldo["cantidad"] == 2500.0
    assert sueldo["mes"] == 10
    assert sueldo["anio"] == 2025

# --- TRANSACCIONES ---
def test_transaccion_routes():
    email = f"trans_{os.urandom(4).hex()}@correo.com"
    # Registro y login para obtener token
    client.post("/auth/register", json={"email": email, "password": "trans123"})
    login = client.post("/auth/token", data={"username": email, "password": "trans123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Crear transacción
    response = client.post("/transacciones/", json={"tipo": "gasto", "cantidad": 100.0, "descripcion": "api test"}, headers=headers)
    assert response.status_code == 200
    trans = response.json()
    assert trans["tipo"] == "gasto"
    assert trans["cantidad"] == 100.0
    assert trans["descripcion"] == "api test"
    trans_id = trans["id"]
    # Obtener transacciones
    response = client.get("/transacciones/", headers=headers)
    assert response.status_code == 200
    transacciones = response.json()
    assert any(t["id"] == trans_id for t in transacciones)
    # Actualizar transacción
    response = client.put(f"/transacciones/{trans_id}", json={"cantidad": 150.0}, headers=headers)
    assert response.status_code == 200
    trans_upd = response.json()
    assert trans_upd["cantidad"] == 150.0
    # Eliminar transacción
    response = client.delete(f"/transacciones/{trans_id}", headers=headers)
    # La API puede devolver 204 No Content (estándar) o 200 con cuerpo
    assert response.status_code in (200, 204)
    if response.status_code == 200:
        result = response.json()
        # Acepta respuesta con id o un detail informativo
        assert result.get("id") == trans_id or result.get("detail")
    # Verificar que ya no aparece en el listado
    check = client.get("/transacciones/", headers=headers)
    assert check.status_code == 200
    assert not any(t["id"] == trans_id for t in check.json())
