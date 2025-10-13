"""
Auth Controller - Endpoints de autenticación
Solo coordinan entre DTOs y Use Cases
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...application.dtos.common_dtos import UserCreateDTO, UserLoginDTO, TokenResponseDTO, UserResponseDTO
from ...application.use_cases.usuario.crear_usuario import CrearUsuarioUseCase
from ...application.use_cases.usuario.login_usuario import LoginUsuarioUseCase
from ...application.use_cases.usuario.perfil_usuario import PerfilUsuarioUseCase
from ...domain.entities.usuario import Usuario
from ..dependencies.auth import get_current_user_from_token
from ..dependencies.container import get_crear_usuario_use_case, get_login_usuario_use_case, get_perfil_usuario_use_case

router = APIRouter(prefix="/auth", tags=["auth"])



@router.post("/register", response_model=UserResponseDTO)
def register(
    request: UserCreateDTO,
    crear_usuario_uc: CrearUsuarioUseCase = Depends(get_crear_usuario_use_case)
):
    """
    Registrar nuevo usuario
    Controller que solo coordina DTO → Use Case → Response
    """
    try:
        # Ejecutar caso de uso
        usuario = crear_usuario_uc.execute(request.email, request.password)
        
        # Convertir a DTO de respuesta
        return UserResponseDTO(
            id=usuario.id,
            email=usuario.email,
            is_active=usuario.is_active,
            created_at=usuario.created_at
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponseDTO)
def login(
    request: UserLoginDTO,
    login_uc: LoginUsuarioUseCase = Depends(get_login_usuario_use_case)
):
    """
    Autenticar usuario y generar JWT
    """
    try:
        # Ejecutar caso de uso
        token_data = login_uc.execute(request.email, request.password)
        
        # Devolver token como DTO
        return TokenResponseDTO(**token_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/token", response_model=TokenResponseDTO)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    login_uc: LoginUsuarioUseCase = Depends(get_login_usuario_use_case)
):
    """
    Endpoint compatible con OAuth2PasswordRequestForm (FastAPI docs)
    """
    try:
        # Usar el formulario OAuth2 pero mismo use case
        token_data = login_uc.execute(form_data.username, form_data.password)
        return TokenResponseDTO(**token_data)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

@router.get("/me", response_model=UserResponseDTO)
def obtener_perfil(
    current_user: Usuario = Depends(get_current_user_from_token)
):
    """
    Obtener perfil del usuario autenticado
    """
    try:
        return UserResponseDTO(
            id=current_user.id,
            email=current_user.email,
            is_active=current_user.is_active,
            created_at=current_user.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )