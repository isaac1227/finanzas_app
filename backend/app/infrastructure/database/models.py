"""
Modelos SQLAlchemy - Infrastructure Layer
Estos modelos son específicos para PostgreSQL y se usan solo en infrastructure
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..config.database import Base
import datetime


class UsuarioORM(Base):
    """
    Modelo SQLAlchemy para Usuario - solo para persistencia
    Se mapea con la entidad domain.entities.Usuario
    """
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relaciones SQLAlchemy
    transacciones = relationship("TransaccionORM", back_populates="usuario")
    sueldos = relationship("SueldoORM", back_populates="usuario")


class TransaccionORM(Base):
    """
    Modelo SQLAlchemy para Transaccion - solo para persistencia
    """
    __tablename__ = "transacciones"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    descripcion = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Relación inversa
    usuario = relationship("UsuarioORM", back_populates="transacciones")


class SueldoORM(Base):
    """
    Modelo SQLAlchemy para Sueldo - solo para persistencia
    """
    __tablename__ = "sueldos"
    
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    # Constraint único por usuario/mes/año
    __table_args__ = (UniqueConstraint('mes', 'anio', 'user_id', name='uq_mes_anio_user'),)
    
    # Relación inversa
    usuario = relationship("UsuarioORM", back_populates="sueldos")