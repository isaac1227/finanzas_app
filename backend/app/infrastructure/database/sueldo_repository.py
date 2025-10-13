"""
Repositorio concreto SQLAlchemy para Sueldo
Implementa la interfaz SueldoRepositoryInterface usando PostgreSQL
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from ...domain.repositories.sueldo_repository import SueldoRepositoryInterface
from ...domain.entities.sueldo import Sueldo
from .models import SueldoORM


class SQLSueldoRepository(SueldoRepositoryInterface):
    """
    Implementación concreta del repositorio de sueldos usando SQLAlchemy + PostgreSQL
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, sueldo: Sueldo) -> Sueldo:
        """Guardar sueldo"""
        sueldo_orm = self._to_orm(sueldo)
        self.session.add(sueldo_orm)
        self.session.commit()
        self.session.refresh(sueldo_orm)
        return self._to_domain(sueldo_orm)
    
    def find_by_id(self, sueldo_id: int) -> Optional[Sueldo]:
        """Buscar sueldo por ID"""
        sueldo_orm = self.session.query(SueldoORM).filter(SueldoORM.id == sueldo_id).first()
        return self._to_domain(sueldo_orm) if sueldo_orm else None
    
    def find_all_by_user(self, user_id: int) -> List[Sueldo]:
        """Obtener todos los sueldos de un usuario"""
        sueldos_orm = self.session.query(SueldoORM).filter(SueldoORM.user_id == user_id).all()
        return [self._to_domain(s) for s in sueldos_orm]
    
    def find_by_user_and_period(self, user_id: int, mes: int, anio: int) -> Optional[Sueldo]:
        """Buscar sueldo específico de usuario por mes/año"""
        sueldo_orm = self.session.query(SueldoORM).filter(
            SueldoORM.user_id == user_id,
            SueldoORM.mes == mes,
            SueldoORM.anio == anio
        ).first()
        
        return self._to_domain(sueldo_orm) if sueldo_orm else None
    
    def update(self, sueldo: Sueldo) -> Sueldo:
        """Actualizar sueldo existente"""
        sueldo_orm = self.session.query(SueldoORM).filter(SueldoORM.id == sueldo.id).first()
        if not sueldo_orm:
            raise ValueError(f"Sueldo con ID {sueldo.id} no encontrado")
            
        sueldo_orm.cantidad = sueldo.cantidad
        sueldo_orm.mes = sueldo.mes
        sueldo_orm.anio = sueldo.anio
        
        self.session.commit()
        return self._to_domain(sueldo_orm)
    
    def delete(self, sueldo_id: int) -> bool:
        """Eliminar sueldo por ID"""
        sueldo_orm = self.session.query(SueldoORM).filter(SueldoORM.id == sueldo_id).first()
        if not sueldo_orm:
            return False
            
        self.session.delete(sueldo_orm)
        self.session.commit()
        return True
    
    def upsert_by_period(self, sueldo: Sueldo) -> Sueldo:
        """
        Crear o actualizar sueldo según período (regla de negocio única)
        Si ya existe un sueldo para ese user/mes/año, lo actualiza
        Si no existe, crea uno nuevo
        """
        sueldo_existente_orm = self.session.query(SueldoORM).filter(
            SueldoORM.user_id == sueldo.user_id,
            SueldoORM.mes == sueldo.mes,
            SueldoORM.anio == sueldo.anio
        ).first()
        
        if sueldo_existente_orm:
            # Actualizar existente
            sueldo_existente_orm.cantidad = sueldo.cantidad
            self.session.commit()
            self.session.refresh(sueldo_existente_orm)
            return self._to_domain(sueldo_existente_orm)
        else:
            # Crear nuevo
            return self.save(sueldo)
    
    # ========== MÉTODOS DE CONVERSIÓN ==========
    
    def _to_orm(self, sueldo: Sueldo) -> SueldoORM:
        """Convertir entidad de dominio → modelo ORM"""
        return SueldoORM(
            id=sueldo.id,
            cantidad=sueldo.cantidad,
            mes=sueldo.mes,
            anio=sueldo.anio,
            user_id=sueldo.user_id,
            fecha=sueldo.fecha
        )
    
    def _to_domain(self, sueldo_orm: SueldoORM) -> Sueldo:
        """Convertir modelo ORM → entidad de dominio"""
        return Sueldo(
            id=sueldo_orm.id,
            cantidad=sueldo_orm.cantidad,
            mes=sueldo_orm.mes,
            anio=sueldo_orm.anio,
            user_id=sueldo_orm.user_id,
            fecha=sueldo_orm.fecha
        )