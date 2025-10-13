"""
Repositorio concreto SQLAlchemy para Usuario
Implementa la interfaz UsuarioRepositoryInterface usando PostgreSQL
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from ...domain.repositories.usuario_repository import UsuarioRepositoryInterface
from ...domain.entities.usuario import Usuario
from .models import UsuarioORM


class SQLUsuarioRepository(UsuarioRepositoryInterface):
    def create(self, email: str, hashed_password: str, is_active: bool = True):
        usuario_orm = UsuarioORM(email=email, hashed_password=hashed_password, is_active=is_active)
        self.session.add(usuario_orm)
        self.session.commit()
        self.session.refresh(usuario_orm)
        print(f"DEBUG USUARIO ORM: id={usuario_orm.id}, email={usuario_orm.email}, created_at={usuario_orm.created_at}")
        return self._to_domain(usuario_orm)
    """
    Implementación concreta del repositorio de usuarios usando SQLAlchemy + PostgreSQL
    Actúa como "traductor" entre entidades de dominio y modelos ORM
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, usuario: Usuario) -> Usuario:
        """Guardar usuario - convierte de dominio a ORM y viceversa"""
        # Convertir entidad de dominio → modelo ORM
        usuario_orm = self._to_orm(usuario)
        
        # Guardar en PostgreSQL
        self.session.add(usuario_orm)
        self.session.commit()
        self.session.refresh(usuario_orm)
        
        # Convertir modelo ORM → entidad de dominio
        return self._to_domain(usuario_orm)
    
    def find_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Buscar usuario por ID"""
        usuario_orm = self.session.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        
        if usuario_orm is None:
            return None
            
        return self._to_domain(usuario_orm)
    
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Buscar usuario por email"""
        usuario_orm = self.session.query(UsuarioORM).filter(UsuarioORM.email == email).first()
        
        if usuario_orm is None:
            return None
            
        return self._to_domain(usuario_orm)
    
    def find_all(self) -> List[Usuario]:
        """Obtener todos los usuarios"""
        usuarios_orm = self.session.query(UsuarioORM).all()
        return [self._to_domain(usuario_orm) for usuario_orm in usuarios_orm]
    
    def update(self, usuario: Usuario) -> Usuario:
        """Actualizar usuario existente"""
        usuario_orm = self.session.query(UsuarioORM).filter(UsuarioORM.id == usuario.id).first()
        
        if usuario_orm is None:
            raise ValueError(f"Usuario con ID {usuario.id} no encontrado")
        
        # Actualizar campos
        usuario_orm.email = usuario.email
        usuario_orm.hashed_password = usuario.hashed_password
        usuario_orm.is_active = usuario.is_active
        
        self.session.commit()
        self.session.refresh(usuario_orm)
        
        return self._to_domain(usuario_orm)
    
    def delete(self, usuario_id: int) -> bool:
        """Eliminar usuario por ID"""
        usuario_orm = self.session.query(UsuarioORM).filter(UsuarioORM.id == usuario_id).first()
        
        if usuario_orm is None:
            return False
        
        self.session.delete(usuario_orm)
        self.session.commit()
        return True
    
    def exists_by_email(self, email: str) -> bool:
        """Verificar si existe usuario con email"""
        count = self.session.query(UsuarioORM).filter(UsuarioORM.email == email).count()
        return count > 0
    
    # ========== MÉTODOS DE CONVERSIÓN ==========
    
    def _to_orm(self, usuario: Usuario) -> UsuarioORM:
        """Convertir entidad de dominio → modelo ORM"""
        return UsuarioORM(
            id=usuario.id,
            email=usuario.email,
            hashed_password=usuario.hashed_password,
            is_active=usuario.is_active,
            created_at=usuario.created_at
        )
    
    def _to_domain(self, usuario_orm: UsuarioORM) -> Usuario:
        """Convertir modelo ORM → entidad de dominio"""
        return Usuario(
            id=usuario_orm.id,
            email=usuario_orm.email,
            hashed_password=usuario_orm.hashed_password,
            is_active=usuario_orm.is_active,
            created_at=usuario_orm.created_at
        )