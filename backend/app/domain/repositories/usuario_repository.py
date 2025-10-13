"""
Interface abstracta para UsuarioRepository
Define el contrato que deben cumplir las implementaciones concretas
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.usuario import Usuario


class UsuarioRepositoryInterface(ABC):
    """
    Contrato abstracto para repositorio de usuarios
    Las implementaciones concretas (SQLAlchemy, MongoDB, etc.) deben seguir este contrato
    """
    
    @abstractmethod
    def save(self, usuario: Usuario) -> Usuario:
        """Guardar usuario en almacenamiento"""
        pass
    
    @abstractmethod
    def find_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Buscar usuario por ID"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Buscar usuario por email"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Usuario]:
        """Obtener todos los usuarios"""
        pass
    
    @abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        """Actualizar usuario existente"""
        pass
    
    @abstractmethod
    def delete(self, usuario_id: int) -> bool:
        """Eliminar usuario por ID"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Verificar si existe usuario con email"""
        pass