from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from .database import Base
import datetime

class Transaccion(Base):
    __tablename__ = "transacciones"
    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String)  # "ingreso" o "gasto"
    cantidad = Column(Float)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    descripcion = Column(String)

class Sueldo(Base):
    __tablename__ = "sueldos"
    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    mes = Column(Integer, nullable=False)  # 1-12
    anio = Column(Integer, nullable=False)
    
    # Constraint único: solo un sueldo por mes/año
    __table_args__ = (UniqueConstraint('mes', 'anio', name='unique_sueldo_mes_anio'),)
