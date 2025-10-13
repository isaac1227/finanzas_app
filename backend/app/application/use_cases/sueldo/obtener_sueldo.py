# Caso de uso básico para obtener sueldo de un mes/año
from app.infrastructure.database.models import SueldoORM
from app.infrastructure.config.database import SessionLocal

class ObtenerSueldoUseCase:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def execute(self, user_id: int, mes: int, anio: int):
        return self.db.query(SueldoORM).filter(SueldoORM.user_id == user_id, SueldoORM.mes == mes, SueldoORM.anio == anio).first()
"""
Caso de uso: Obtener sueldo de un mes
"""
from app.domain.repositories.sueldo_repository import SueldoRepositoryInterface
from app.domain.repositories.usuario_repository import UsuarioRepositoryInterface
from app.domain.entities.sueldo import Sueldo

class ObtenerSueldoUseCase:
    def __init__(self, sueldo_repository: SueldoRepositoryInterface, usuario_repository: UsuarioRepositoryInterface):
        self.sueldo_repository = sueldo_repository
        self.usuario_repository = usuario_repository

    def execute(self, user_id: int, mes: int, anio: int) -> Sueldo:
        usuario = self.usuario_repository.find_by_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        sueldo = self.sueldo_repository.find_by_user_and_period(user_id, mes, anio)
        return sueldo
