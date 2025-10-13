"""
Interface abstracta para TransaccionRepository
Define el contrato que deben cumplir las implementaciones concretas
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.transaccion import Transaccion


class TransaccionRepositoryInterface(ABC):
    """
    Contrato abstracto para repositorio de transacciones
    """
    
    @abstractmethod
    def save(self, transaccion: Transaccion) -> Transaccion:
        """Guardar transacción en almacenamiento"""
        pass
    
    @abstractmethod
    def find_by_id(self, transaccion_id: int) -> Optional[Transaccion]:
        """Buscar transacción por ID"""
        pass
    
    @abstractmethod
    def find_all_by_user(self, user_id: int) -> List[Transaccion]:
        """Obtener todas las transacciones de un usuario"""
        pass
    
    @abstractmethod
    def find_by_user_and_month(self, user_id: int, mes: Optional[int] = None, anio: Optional[int] = None) -> List[Transaccion]:
        """Buscar transacciones de usuario filtradas por mes/año"""
        pass
    
    @abstractmethod
    def update(self, transaccion: Transaccion) -> Transaccion:
        """Actualizar transacción existente"""
        pass
    
    @abstractmethod
    def delete(self, transaccion_id: int) -> bool:
        """Eliminar transacción por ID"""
        pass
    
    @abstractmethod
    def get_balance_by_user(self, user_id: int) -> float:
        """Calcular balance total del usuario"""
        pass
    
    @abstractmethod
    def get_ingresos_by_user(self, user_id: int, mes: Optional[int] = None, anio: Optional[int] = None) -> float:
        """Sumar ingresos del usuario en período"""
        pass
    
    @abstractmethod
    def get_gastos_by_user(self, user_id: int, mes: Optional[int] = None, anio: Optional[int] = None) -> float:
        """Sumar gastos del usuario en período"""
        pass