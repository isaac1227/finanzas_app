"""
Caso de uso: Actualizar sueldo
"""

from app.infrastructure.database.models import SueldoORM
from app.infrastructure.config.database import SessionLocal

from app.domain.repositories.sueldo_repository import SueldoRepositoryInterface
from app.domain.repositories.usuario_repository import UsuarioRepositoryInterface
from app.domain.entities.sueldo import Sueldo
from typing import Optional

class ActualizarSueldoUseCase:
    def __init__(self, sueldo_repository: SueldoRepositoryInterface, usuario_repository: UsuarioRepositoryInterface):
        self.sueldo_repository = sueldo_repository
        self.usuario_repository = usuario_repository

    def execute(self, user_id: int, cantidad: Optional[float] = None, mes: Optional[int] = None, anio: Optional[int] = None) -> Sueldo:
        usuario = self.usuario_repository.find_by_id(user_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        sueldo = self.sueldo_repository.find_by_user_and_period(user_id, mes, anio)
        if not sueldo:
            raise ValueError("Sueldo no encontrado para el periodo especificado")
        if cantidad is not None:
            sueldo.cantidad = cantidad
        if mes is not None:
            sueldo.mes = mes
        if anio is not None:
            sueldo.anio = anio
        updated_sueldo = self.sueldo_repository.update(sueldo)
        return updated_sueldo