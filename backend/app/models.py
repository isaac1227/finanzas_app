from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)  # Email único para login
    hashed_password = Column(String, nullable=False)  # Contraseña hasheada (nunca guardamos la real)
    is_active = Column(Boolean, default=True)  # Por si queremos desactivar usuarios
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relaciones - un usuario tiene muchas transacciones y sueldos
    transacciones = relationship("Transaccion", back_populates="usuario")
    sueldos = relationship("Sueldo", back_populates="usuario")

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    descripcion = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # ← NUEVO: cada transacción pertenece a un usuario
    
    # Relación inversa
    usuario = relationship("Usuario", back_populates="transacciones")

class Sueldo(Base):
    __tablename__ = "sueldos" 
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # ← NUEVO: cada sueldo pertenece a un usuario
    
    # Cambiar constraint para incluir user_id (un usuario puede tener un sueldo por mes/año)
    __table_args__ = (UniqueConstraint('mes', 'anio', 'user_id', name='uq_mes_anio_user'),)
    
    # Relación inversa
    usuario = relationship("Usuario", back_populates="sueldos")
