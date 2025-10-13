"""
Container de Inyección de Dependencias
Configura y conecta todas las capas de Clean Architecture
"""
from sqlalchemy.orm import Session
from fastapi import Depends

# Infrastructure imports
from ...infrastructure.config.database import get_db
from ...infrastructure.database.usuario_repository import SQLUsuarioRepository
from ...infrastructure.database.transaccion_repository import SQLTransaccionRepository
from ...infrastructure.database.sueldo_repository import SQLSueldoRepository

# Application imports  
from ...application.use_cases.usuario.crear_usuario import CrearUsuarioUseCase
from ...application.use_cases.usuario.login_usuario import LoginUsuarioUseCase
from ...application.use_cases.usuario.perfil_usuario import PerfilUsuarioUseCase
from ...application.use_cases.transaccion.crear_transaccion import CrearTransaccionUseCase
from ...application.use_cases.transaccion.obtener_transacciones import ObtenerTransaccionesUseCase
from ...application.use_cases.balance.calcular_balance import CalcularBalanceUseCase
from ...application.use_cases.transaccion.actualizar_transaccion import ActualizarTransaccionUseCase
from ...application.use_cases.transaccion.eliminar_transaccion import EliminarTransaccionUseCase
from ...application.use_cases.sueldo.crear_sueldo import CrearSueldoUseCase
from ...application.use_cases.sueldo.obtener_sueldo import ObtenerSueldoUseCase
from ...application.use_cases.sueldo.obtener_sueldos import ObtenerSueldosUseCase
from ...application.use_cases.sueldo.actualizar_sueldo import ActualizarSueldoUseCase


# ========== REPOSITORY DEPENDENCIES ==========

def get_usuario_repository(db: Session = Depends(get_db)) -> SQLUsuarioRepository:
    """Inyectar repositorio de usuarios"""
    return SQLUsuarioRepository(db)

def get_transaccion_repository(db: Session = Depends(get_db)) -> SQLTransaccionRepository:
    """Inyectar repositorio de transacciones"""
    return SQLTransaccionRepository(db)

def get_sueldo_repository(db: Session = Depends(get_db)) -> SQLSueldoRepository:
    """Inyectar repositorio de sueldos"""
    return SQLSueldoRepository(db)


# ========== USE CASE DEPENDENCIES ==========

def get_crear_usuario_use_case(
    usuario_repo = Depends(get_usuario_repository),
    sueldo_repo = Depends(get_sueldo_repository)
) -> CrearUsuarioUseCase:
    """Inyectar caso de uso CrearUsuario"""
    return CrearUsuarioUseCase(usuario_repo, sueldo_repo)

def get_login_usuario_use_case(
    usuario_repo = Depends(get_usuario_repository)
) -> LoginUsuarioUseCase:
    """Inyectar caso de uso LoginUsuario"""
    return LoginUsuarioUseCase(usuario_repo)

def get_perfil_usuario_use_case(
    usuario_repo = Depends(get_usuario_repository)
) -> PerfilUsuarioUseCase:
    """Inyectar caso de uso PerfilUsuario"""
    return PerfilUsuarioUseCase(usuario_repo)

def get_crear_transaccion_use_case():
    """Inyectar caso de uso CrearTransaccion"""
    return CrearTransaccionUseCase()

def get_obtener_transacciones_use_case():
    """Inyectar caso de uso ObtenerTransacciones"""
    return ObtenerTransaccionesUseCase()

def get_actualizar_transaccion_use_case():
    """Inyectar caso de uso ActualizarTransaccion"""
    return ActualizarTransaccionUseCase()

def get_eliminar_transaccion_use_case():
    """Inyectar caso de uso EliminarTransaccion"""
    return EliminarTransaccionUseCase()

def get_calcular_balance_use_case():
    """Inyectar caso de uso CalcularBalance"""
    return CalcularBalanceUseCase()

def get_crear_sueldo_use_case(
    sueldo_repo = Depends(get_sueldo_repository),
    usuario_repo = Depends(get_usuario_repository)
) -> CrearSueldoUseCase:
    """Inyectar caso de uso CrearSueldo"""
    return CrearSueldoUseCase(sueldo_repo, usuario_repo)

def get_obtener_sueldo_use_case(
    sueldo_repo = Depends(get_sueldo_repository),
    usuario_repo = Depends(get_usuario_repository)
) -> ObtenerSueldoUseCase:
    """Inyectar caso de uso ObtenerSueldo"""
    return ObtenerSueldoUseCase(sueldo_repo, usuario_repo)

def get_obtener_sueldos_use_case(
    sueldo_repo = Depends(get_sueldo_repository),
    usuario_repo = Depends(get_usuario_repository)
) -> ObtenerSueldosUseCase:
    """Inyectar caso de uso ObtenerSueldos"""
    return ObtenerSueldosUseCase(sueldo_repo, usuario_repo)

def get_actualizar_sueldo_use_case(
    sueldo_repo = Depends(get_sueldo_repository),
    usuario_repo = Depends(get_usuario_repository)
) -> ActualizarSueldoUseCase:
    """Inyectar caso de uso ActualizarSueldo"""
    return ActualizarSueldoUseCase(sueldo_repo, usuario_repo)