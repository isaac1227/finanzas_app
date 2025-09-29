from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from .database import Base
import datetime

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    descripcion = Column(String, nullable=True)

class Sueldo(Base):
    __tablename__ = "sueldos" 
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Float, nullable=False)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    
    __table_args__ = (UniqueConstraint('mes', 'anio', name='uq_mes_anio'),)
