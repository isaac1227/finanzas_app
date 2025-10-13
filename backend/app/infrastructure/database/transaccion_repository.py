"""
Repositorio concreto SQLAlchemy para Transaccion
Implementa la interfaz TransaccionRepositoryInterface usando PostgreSQL
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from ...domain.repositories.transaccion_repository import TransaccionRepositoryInterface
from ...domain.entities.transaccion import Transaccion
from .models import TransaccionORM


class SQLTransaccionRepository(TransaccionRepositoryInterface):
    """
    Implementación concreta del repositorio de transacciones usando SQLAlchemy + PostgreSQL
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, transaccion: Transaccion) -> Transaccion:
        """Guardar transacción"""
        transaccion_orm = self._to_orm(transaccion)
        self.session.add(transaccion_orm)
        self.session.commit()
        self.session.refresh(transaccion_orm)
        return self._to_domain(transaccion_orm)
    
    def find_by_id(self, transaccion_id: int) -> Optional[Transaccion]:
        """Buscar transacción por ID"""
        transaccion_orm = self.session.query(TransaccionORM).filter(TransaccionORM.id == transaccion_id).first()
        return self._to_domain(transaccion_orm) if transaccion_orm else None
    
    def find_all_by_user(self, user_id: int) -> List[Transaccion]:
        """Obtener todas las transacciones de un usuario"""
        transacciones_orm = self.session.query(TransaccionORM).filter(TransaccionORM.user_id == user_id).all()
        return [self._to_domain(t) for t in transacciones_orm]
    
    def find_by_user_and_month(self, user_id: int, mes: Optional[int] = None, anio: Optional[int] = None) -> List[Transaccion]:
        """Buscar transacciones filtradas por mes/año"""
        query = self.session.query(TransaccionORM).filter(TransaccionORM.user_id == user_id)
        
        if mes:
            query = query.filter(extract('month', TransaccionORM.fecha) == mes)
        if anio:
            query = query.filter(extract('year', TransaccionORM.fecha) == anio)
            
        transacciones_orm = query.all()
        return [self._to_domain(t) for t in transacciones_orm]
    
    def update(self, transaccion: Transaccion) -> Transaccion:
        """Actualizar transacción existente"""
        transaccion_orm = self.session.query(TransaccionORM).filter(TransaccionORM.id == transaccion.id).first()
        if not transaccion_orm:
            raise ValueError(f"Transacción con ID {transaccion.id} no encontrada")
            
        transaccion_orm.tipo = transaccion.tipo
        transaccion_orm.cantidad = transaccion.cantidad
        transaccion_orm.descripcion = transaccion.descripcion
        
        self.session.commit()
        return self._to_domain(transaccion_orm)
    
    def delete(self, transaccion_id: int) -> bool:
        """Eliminar transacción por ID"""
        transaccion_orm = self.session.query(TransaccionORM).filter(TransaccionORM.id == transaccion_id).first()
        if not transaccion_orm:
            return False
            
        self.session.delete(transaccion_orm)
        self.session.commit()
        return True
    
    def get_balance_by_user(self, user_id: int) -> float:
        """Calcular balance total del usuario"""
        ingresos = self.get_ingresos_by_user(user_id)
        gastos = self.get_gastos_by_user(user_id)
        return ingresos - gastos
    
    def get_ingresos_by_user(self, user_id: int, mes: Optional[int] = None, anio: Optional[int] = None) -> float:
        """Sumar ingresos del usuario en período"""
        query = self.session.query(func.sum(TransaccionORM.cantidad)).filter(
            TransaccionORM.user_id == user_id,
            TransaccionORM.tipo == "ingreso"
        )
        
        if mes:
            query = query.filter(extract('month', TransaccionORM.fecha) == mes)
        if anio:
            query = query.filter(extract('year', TransaccionORM.fecha) == anio)
            
        result = query.scalar()
        return result or 0.0
    
    def get_gastos_by_user(self, user_id: int, mes: Optional[int] = None, anio: Optional[int] = None) -> float:
        """Sumar gastos del usuario en período"""
        query = self.session.query(func.sum(TransaccionORM.cantidad)).filter(
            TransaccionORM.user_id == user_id,
            TransaccionORM.tipo == "gasto"
        )
        
        if mes:
            query = query.filter(extract('month', TransaccionORM.fecha) == mes)
        if anio:
            query = query.filter(extract('year', TransaccionORM.fecha) == anio)
            
        result = query.scalar()
        return result or 0.0
    
    # ========== MÉTODOS DE CONVERSIÓN ==========
    
    def _to_orm(self, transaccion: Transaccion) -> TransaccionORM:
        """Convertir entidad de dominio → modelo ORM"""
        return TransaccionORM(
            id=transaccion.id,
            tipo=transaccion.tipo,
            cantidad=transaccion.cantidad,
            user_id=transaccion.user_id,
            fecha=transaccion.fecha,
            descripcion=transaccion.descripcion
        )
    
    def _to_domain(self, transaccion_orm: TransaccionORM) -> Transaccion:
        """Convertir modelo ORM → entidad de dominio"""
        return Transaccion(
            id=transaccion_orm.id,
            tipo=transaccion_orm.tipo,
            cantidad=transaccion_orm.cantidad,
            user_id=transaccion_orm.user_id,
            fecha=transaccion_orm.fecha,
            descripcion=transaccion_orm.descripcion
        )