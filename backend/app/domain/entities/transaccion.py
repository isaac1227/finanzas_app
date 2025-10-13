"""
Entidad Transaccion - Modelo de dominio puro sin dependencias de framework
"""
from datetime import datetime
from typing import Optional


class Transaccion:
    """
    Entidad de dominio Transaccion que representa el concepto de negocio
    """
    
    def __init__(
        self,
        tipo: str,
        cantidad: float,
        user_id: int,
        id: Optional[int] = None,
        fecha: Optional[datetime] = None,
        descripcion: Optional[str] = None
    ):
        self.id = id
        self.tipo = tipo
        self.cantidad = cantidad
        self.user_id = user_id
        self.fecha = fecha or datetime.utcnow()
        self.descripcion = descripcion
        
        # Validaciones de dominio
        self._validate()
    
    def _validate(self):
        """Validaciones de reglas de negocio"""
        if self.tipo not in ["ingreso", "gasto"]:
            raise ValueError("Tipo debe ser 'ingreso' o 'gasto'")
        
        if self.cantidad <= 0:
            raise ValueError("Cantidad debe ser positiva")
        
        if not self.user_id:
            raise ValueError("User ID es requerido")
    
    def is_ingreso(self) -> bool:
        """Regla de negocio: verificar si es ingreso"""
        return self.tipo == "ingreso"
    
    def is_gasto(self) -> bool:
        """Regla de negocio: verificar si es gasto"""
        return self.tipo == "gasto"
    
    def get_amount_with_sign(self) -> float:
        """Regla de negocio: cantidad con signo según tipo"""
        return self.cantidad if self.is_ingreso() else -self.cantidad
    
    def __repr__(self):
        return f"Transaccion(id={self.id}, tipo={self.tipo}, cantidad={self.cantidad})"