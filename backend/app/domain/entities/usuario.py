"""
Entidad Usuario - Modelo de dominio puro sin dependencias de framework
"""
from datetime import datetime
from typing import Optional, List


class Usuario:
    """
    Entidad de dominio Usuario que representa el concepto de negocio
    sin dependencias de SQLAlchemy ni otras librerías externas
    """
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        id: Optional[int] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        transacciones: Optional[List] = None,
        sueldos: Optional[List] = None
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.transacciones = transacciones or []
        self.sueldos = sueldos or []
        
        # Validaciones de dominio
        self._validate()
    
    def _validate(self):
        """Validaciones de reglas de negocio"""
        if not self.email or "@" not in self.email:
            raise ValueError("Email inválido")
        
        if not self.hashed_password:
            raise ValueError("Contraseña hasheada requerida")
    
    def is_email_valid(self) -> bool:
        """Regla de negocio: validar formato de email"""
        return "@" in self.email and "." in self.email
    
    def activate(self):
        """Regla de negocio: activar usuario"""
        self.is_active = True
    
    def deactivate(self):
        """Regla de negocio: desactivar usuario"""
        self.is_active = False
    
    def __repr__(self):
        return f"Usuario(id={self.id}, email={self.email}, active={self.is_active})"