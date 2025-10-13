# Caso de uso básico para crear o actualizar sueldo
from app.infrastructure.database.models import SueldoORM
from app.infrastructure.config.database import SessionLocal

class CrearSueldoUseCase:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def execute(self, user_id: int, cantidad: float, mes: int, anio: int):
        sueldo = self.db.query(SueldoORM).filter(SueldoORM.user_id == user_id, SueldoORM.mes == mes, SueldoORM.anio == anio).first()
        if sueldo:
            sueldo.cantidad = cantidad
        else:
            sueldo = SueldoORM(user_id=user_id, cantidad=cantidad, mes=mes, anio=anio)
            self.db.add(sueldo)
        self.db.commit()
        self.db.refresh(sueldo)
        return sueldo
"""
Caso de uso: Crear o actualizar sueldo
"""
from app.domain.repositories.sueldo_repository import SueldoRepositoryInterface
from app.domain.repositories.usuario_repository import UsuarioRepositoryInterface
from app.domain.entities.sueldo import Sueldo

class CrearSueldoUseCase:
    def __init__(self, sueldo_repository: SueldoRepositoryInterface, usuario_repository: UsuarioRepositoryInterface):
        self.sueldo_repository = sueldo_repository
        self.usuario_repository = usuario_repository

    def execute(self, user_id: int, cantidad: float, mes: int, anio: int) -> Sueldo:
        usuario = self.usuario_repository.find_by_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        # Crear entidad de dominio Sueldo
        from app.domain.entities.sueldo import Sueldo
        sueldo_entidad = Sueldo(cantidad=cantidad, mes=mes, anio=anio, user_id=user_id)
        sueldo = self.sueldo_repository.upsert_by_period(sueldo_entidad)
        return sueldo
