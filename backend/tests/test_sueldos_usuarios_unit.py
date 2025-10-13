# backend/tests/test_sueldos_usuarios_unit.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

# Repositorios mínimos para los tests de sueldos
class SueldoRepositoryTest:
    def __init__(self, db):
        self.db = db
    # Métodos mínimos compatibles con los casos de uso y el test
    def create_or_update(self, user_id, cantidad, mes, anio):
        sueldo = self.db.query(SueldoORM).filter(SueldoORM.user_id == user_id, SueldoORM.mes == mes, SueldoORM.anio == anio).first()
        if sueldo:
            sueldo.cantidad = cantidad
        else:
            sueldo = SueldoORM(user_id=user_id, cantidad=cantidad, mes=mes, anio=anio)
            self.db.add(sueldo)
        self.db.commit()
        self.db.refresh(sueldo)
        return sueldo
    def get_by_user_and_month(self, user_id, mes, anio):
        return self.db.query(SueldoORM).filter(SueldoORM.user_id == user_id, SueldoORM.mes == mes, SueldoORM.anio == anio).first()
    # Aliases compatibles con casos de uso de la capa aplicación
    def upsert_by_period(self, sueldo_entidad):
        return self.create_or_update(sueldo_entidad.user_id, sueldo_entidad.cantidad, sueldo_entidad.mes, sueldo_entidad.anio)
    def find_by_user_and_period(self, user_id, mes, anio):
        return self.get_by_user_and_month(user_id, mes, anio)

class UsuarioRepositoryTest:
    def __init__(self, db):
        self.db = db
    def find_by_id(self, user_id):
        return self.db.query(UsuarioORM).filter(UsuarioORM.id == user_id).first()
from app.infrastructure.config.database import Base
from app.infrastructure.database.models import UsuarioORM, SueldoORM
from app.application.use_cases.usuario.crear_usuario import CrearUsuarioUseCase
from app.application.use_cases.usuario.perfil_usuario import PerfilUsuarioUseCase
from app.application.use_cases.sueldo.crear_sueldo import CrearSueldoUseCase
from app.application.use_cases.sueldo.obtener_sueldo import ObtenerSueldoUseCase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import hashlib

# Configuración de BD en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    # Limpiar usuarios y sueldos antes de cada test
    session.query(SueldoORM).delete()
    session.query(UsuarioORM).delete()
    session.commit()
    yield session
    session.close()

@pytest.fixture
def user_email():
    return "testuser@correo.com"

@pytest.fixture
def user_password():
    return "testpass123"

@pytest.fixture
def user_id(db, user_email, user_password):
    usecase = CrearUsuarioUseCase(db)
    usuario = usecase.execute(email=user_email, password=user_password)
    return usuario.id

def test_crear_usuario_unit(db, user_email, user_password):
    usecase = CrearUsuarioUseCase(db)
    usuario = usecase.execute(email=user_email, password=user_password)
    assert usuario.id is not None
    assert usuario.email == user_email
    # Verificar que el hash es válido usando verify_password (más robusto)
    from app.auth import verify_password
    assert verify_password(user_password, usuario.hashed_password)
    assert usuario.is_active is True

def test_perfil_usuario_unit(db, user_id, user_email):
    usecase = PerfilUsuarioUseCase(db)
    usuario = usecase.execute(user_id=user_id)
    assert usuario.id == user_id
    assert usuario.email == user_email
    assert usuario.is_active is True

def test_crear_sueldo_unit(db, user_id):
    sueldo_repo = SueldoRepositoryTest(db)
    usuario_repo = UsuarioRepositoryTest(db)
    usecase = CrearSueldoUseCase(sueldo_repo, usuario_repo)
    sueldo = usecase.execute(user_id=user_id, cantidad=1500.0, mes=10, anio=2025)
    assert sueldo.id is not None
    assert sueldo.cantidad == 1500.0
    assert sueldo.mes == 10
    assert sueldo.anio == 2025
    assert sueldo.user_id == user_id

def test_obtener_sueldo_unit(db, user_id):
    sueldo_repo = SueldoRepositoryTest(db)
    usuario_repo = UsuarioRepositoryTest(db)
    usecase_create = CrearSueldoUseCase(sueldo_repo, usuario_repo)
    usecase_create.execute(user_id=user_id, cantidad=2000.0, mes=9, anio=2025)
    usecase_get = ObtenerSueldoUseCase(sueldo_repo, usuario_repo)
    sueldo = usecase_get.execute(user_id=user_id, mes=9, anio=2025)
    assert sueldo is not None
    assert sueldo.cantidad == 2000.0
    assert sueldo.mes == 9
    assert sueldo.anio == 2025
    assert sueldo.user_id == user_id
