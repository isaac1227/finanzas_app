# Ejemplo básico de caso de uso para crear usuario
# Adaptación Clean Architecture: usar repositorio

from app.auth import get_password_hash
from app.infrastructure.database.sueldo_repository import SQLSueldoRepository
from app.infrastructure.database.usuario_repository import SQLUsuarioRepository
from sqlalchemy.orm import Session

class CrearUsuarioUseCase:
    def __init__(self, usuario_repository=None, sueldo_repository=None, db_session: Session | None = None):
        """
        Permite dos modos de inicialización:
        - Inyección de repositorios (modo producción via container)
        - Pasando una sesión de DB directamente (modo tests heredados)
        """
        # Caso 1: repositorios provistos explícitamente (camino principal)
        if usuario_repository is not None and sueldo_repository is not None:
            self.usuario_repository = usuario_repository
            self.sueldo_repository = sueldo_repository
            return

        # Caso 2: compatibilidad con tests: primer argumento es una Session
        if isinstance(usuario_repository, Session) and sueldo_repository is None and db_session is None:
            db = usuario_repository
            self.usuario_repository = SQLUsuarioRepository(db)
            self.sueldo_repository = SQLSueldoRepository(db)
            return

        # Caso 3: se pasó db_session por keyword
        if db_session is not None:
            self.usuario_repository = SQLUsuarioRepository(db_session)
            self.sueldo_repository = SQLSueldoRepository(db_session)
            return

        # Caso 4: fallback - crear nuestra propia sesión (no ideal para tests, pero seguro)
        try:
            from app.infrastructure.config.database import SessionLocal
            db = SessionLocal()
            self.usuario_repository = SQLUsuarioRepository(db)
            self.sueldo_repository = SQLSueldoRepository(db)
        except Exception:
            # Si por algún motivo no podemos crear sesión aquí, mejor fallar explícitamente
            raise TypeError("CrearUsuarioUseCase requiere repositorios o una sesión de base de datos")

    def execute(self, email: str, password: str):
        # Verificar si el usuario ya existe
        usuario_existente = self.usuario_repository.find_by_email(email)
        if usuario_existente:
            raise ValueError("El email ya está registrado")
        
        # Hash seguro para la contraseña
        hashed_password = get_password_hash(password)
        
        # Crear entidad de dominio Usuario
        usuario = self.usuario_repository.create(email=email, hashed_password=hashed_password, is_active=True)
        return usuario
