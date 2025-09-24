from pydantic import BaseModel
from datetime import datetime

class TransaccionBase(BaseModel):
    tipo: str
    cantidad: float
    descripcion: str | None = None

class TransaccionCreate(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True

class TransaccionUpdate(BaseModel):
    tipo: str | None = None
    cantidad: float | None = None
    descripcion: str | None = None

class TransaccionDelete(BaseModel):
    id: int
    
    class Config:
        orm_mode = True

# Schemas para Sueldo
class SueldoBase(BaseModel):
    cantidad: float
    mes: int
    anio: int

class SueldoCreate(SueldoBase):
    pass

class Sueldo(SueldoBase):
    id: int
    fecha: datetime

    class Config:
        orm_mode = True
