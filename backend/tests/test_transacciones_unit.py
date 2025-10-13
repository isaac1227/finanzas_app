# backend/tests/test_transacciones_unit.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from app.infrastructure.config.database import SessionLocal, Base
from app.infrastructure.database.models import TransaccionORM, UsuarioORM
from app.application.use_cases.transaccion.crear_transaccion import CrearTransaccionUseCase
from app.application.use_cases.transaccion.obtener_transacciones import ObtenerTransaccionesUseCase
from app.application.use_cases.transaccion.actualizar_transaccion import ActualizarTransaccionUseCase
from app.application.use_cases.transaccion.eliminar_transaccion import EliminarTransaccionUseCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuración de BD en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    # Limpiar usuarios y transacciones antes de cada test
    session.query(TransaccionORM).delete()
    session.query(UsuarioORM).delete()
    session.commit()
    # Crear usuario de prueba
    usuario = UsuarioORM(email="test@correo.com", hashed_password="1234")
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    yield session
    session.close()

@pytest.fixture
def user_id(db):
    usuario = db.query(UsuarioORM).filter_by(email="test@correo.com").first()
    return usuario.id

def test_crear_transaccion_unit(db, user_id):
    usecase = CrearTransaccionUseCase(db)
    transaccion = usecase.execute(user_id=user_id, tipo="gasto", cantidad=100.0, descripcion="unit test")
    assert transaccion.id is not None
    assert transaccion.tipo == "gasto"
    assert transaccion.cantidad == 100.0
    assert transaccion.descripcion == "unit test"

def test_obtener_transacciones_unit(db, user_id):
    usecase_create = CrearTransaccionUseCase(db)
    usecase_create.execute(user_id=user_id, tipo="ingreso", cantidad=200.0, descripcion="ingreso test")
    usecase_create.execute(user_id=user_id, tipo="gasto", cantidad=50.0, descripcion="gasto test")
    usecase_get = ObtenerTransaccionesUseCase(db)
    transacciones = usecase_get.execute(user_id=user_id)
    assert len(transacciones) == 2
    tipos = [t.tipo for t in transacciones]
    assert "ingreso" in tipos
    assert "gasto" in tipos

def test_actualizar_transaccion_unit(db, user_id):
    usecase_create = CrearTransaccionUseCase(db)
    transaccion = usecase_create.execute(user_id=user_id, tipo="gasto", cantidad=80.0, descripcion="original")
    usecase_update = ActualizarTransaccionUseCase(db)
    transaccion_actualizada = usecase_update.execute(user_id=user_id, transaccion_id=transaccion.id, tipo="ingreso", cantidad=120.0, descripcion="actualizada")
    assert transaccion_actualizada.tipo == "ingreso"
    assert transaccion_actualizada.cantidad == 120.0
    assert transaccion_actualizada.descripcion == "actualizada"

def test_eliminar_transaccion_unit(db, user_id):
    usecase_create = CrearTransaccionUseCase(db)
    transaccion = usecase_create.execute(user_id=user_id, tipo="gasto", cantidad=60.0, descripcion="para eliminar")
    usecase_delete = EliminarTransaccionUseCase(db)
    transaccion_eliminada = usecase_delete.execute(user_id=user_id, transaccion_id=transaccion.id)
    assert transaccion_eliminada.id == transaccion.id
    # Verificar que ya no existe
    transacciones = db.query(TransaccionORM).filter_by(id=transaccion.id).all()
    assert len(transacciones) == 0
