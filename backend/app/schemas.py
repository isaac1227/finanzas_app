from pydantic import BaseModel, validator
from datetime import datetime

class TransaccionBase(BaseModel):
    tipo: str
    cantidad: float
    descripcion: str | None = None

    @validator("cantidad")
    def cantidad_positiva(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser un número positivo")
        return v

    @validator("descripcion")
    def descripcion_obligatoria_gasto(cls, v, values):
        if values.get("tipo") == "gasto" and (v is None or v.strip() == ""):
            raise ValueError("La descripción es obligatoria para gastos")
        return v

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
