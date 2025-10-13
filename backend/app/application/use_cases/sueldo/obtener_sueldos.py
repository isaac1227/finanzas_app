# Caso de uso básico para obtener todos los sueldos de un usuario
from app.infrastructure.database.models import SueldoORM
from app.infrastructure.config.database import SessionLocal

class ObtenerSueldosUseCase:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def execute(self, user_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(SueldoORM).filter(SueldoORM.user_id == user_id).offset(skip).limit(limit).all()
"""
Caso de uso: Obtener todos los sueldos del usuario
"""
from app.domain.repositories.sueldo_repository import SueldoRepositoryInterface
from app.domain.repositories.usuario_repository import UsuarioRepositoryInterface
from app.domain.entities.sueldo import Sueldo
from typing import List

class ObtenerSueldosUseCase:
    def __init__(self, sueldo_repository: SueldoRepositoryInterface, usuario_repository: UsuarioRepositoryInterface):
        self.sueldo_repository = sueldo_repository
        self.usuario_repository = usuario_repository

    def execute(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Sueldo]:
        usuario = self.usuario_repository.find_by_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        sueldos = self.sueldo_repository.find_all_by_user(user_id)
        return sueldos
