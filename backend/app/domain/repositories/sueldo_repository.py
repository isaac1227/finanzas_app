"""
Interface abstracta para SueldoRepository
Define el contrato que deben cumplir las implementaciones concretas
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.sueldo import Sueldo


class SueldoRepositoryInterface(ABC):
    """
    Contrato abstracto para repositorio de sueldos
    """
    
    @abstractmethod
    def save(self, sueldo: Sueldo) -> Sueldo:
        """Guardar sueldo en almacenamiento"""
        pass
    
    @abstractmethod
    def find_by_id(self, sueldo_id: int) -> Optional[Sueldo]:
        """Buscar sueldo por ID"""
        pass
    
    @abstractmethod
    def find_all_by_user(self, user_id: int) -> List[Sueldo]:
        """Obtener todos los sueldos de un usuario"""
        pass
    
    @abstractmethod
    def find_by_user_and_period(self, user_id: int, mes: int, anio: int) -> Optional[Sueldo]:
        """Buscar sueldo específico de usuario por mes/año"""
        pass
    
    @abstractmethod
    def update(self, sueldo: Sueldo) -> Sueldo:
        """Actualizar sueldo existente"""
        pass
    
    @abstractmethod
    def delete(self, sueldo_id: int) -> bool:
        """Eliminar sueldo por ID"""
        pass
    
    @abstractmethod
    def upsert_by_period(self, sueldo: Sueldo) -> Sueldo:
        """Crear o actualizar sueldo según período (regla de negocio única)"""
        pass