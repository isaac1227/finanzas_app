"""
Entidad Sueldo - Modelo de dominio puro sin dependencias de framework
"""
from datetime import datetime
from typing import Optional


class Sueldo:
    """
    Entidad de dominio Sueldo que representa el concepto de negocio
    """
    
    def __init__(
        self,
        cantidad: float,
        mes: int,
        anio: int,
        user_id: int,
        id: Optional[int] = None,
        fecha: Optional[datetime] = None
    ):
        self.id = id
        self.cantidad = cantidad
        self.mes = mes
        self.anio = anio
        self.user_id = user_id
        self.fecha = fecha or datetime.utcnow()
        
        # Validaciones de dominio
        self._validate()
    
    def _validate(self):
        """Validaciones de reglas de negocio"""
        if self.cantidad <= 0:
            raise ValueError("Cantidad del sueldo debe ser positiva")
        
        if not (1 <= self.mes <= 12):
            raise ValueError("Mes debe estar entre 1 y 12")
        
        if self.anio < 2020 or self.anio > 2030:
            raise ValueError("Año debe estar en rango válido")
        
        if not self.user_id:
            raise ValueError("User ID es requerido")
    
    def get_period_key(self) -> str:
        """Regla de negocio: obtener clave única del período"""
        return f"{self.anio}-{self.mes:02d}"
    
    def is_current_month(self) -> bool:
        """Regla de negocio: verificar si es el mes actual"""
        now = datetime.utcnow()
        return self.mes == now.month and self.anio == now.year
    
    def get_formatted_period(self) -> str:
        """Regla de negocio: formato legible del período"""
        meses = [
            "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return f"{meses[self.mes]} {self.anio}"
    
    def __repr__(self):
        return f"Sueldo(id={self.id}, {self.get_formatted_period()}, cantidad={self.cantidad})"