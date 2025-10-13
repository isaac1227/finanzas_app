"""
Dependencia de autenticación para Clean Architecture
Extrae el usuario actual desde JWT token
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from ...auth import verify_token
from ..dependencies.container import get_usuario_repository
from ...infrastructure.database.usuario_repository import SQLUsuarioRepository
from ...domain.entities.usuario import Usuario

security = HTTPBearer()


def get_current_user_from_token(
    credentials = Depends(security),
    usuario_repo: SQLUsuarioRepository = Depends(get_usuario_repository)
) -> Usuario:
    """
    Extraer usuario completo del JWT token para Clean Architecture
    Retorna el objeto Usuario completo
    """
    # Extraer el token de las credenciales Bearer
    token = credentials.credentials
    
    # Verificar el token (usando función existente de auth.py)
    token_data = verify_token(token)
    
    # Buscar el usuario usando el repositorio
    usuario = usuario_repo.find_by_email(email=token_data["email"])
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return usuario  # Devolvemos el objeto Usuario completo