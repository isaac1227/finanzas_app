from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import Optional, List

class TransaccionBase(BaseModel):
    tipo: str
    cantidad: float = Field(..., gt=0, description="Debe ser mayor que 0") 
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None

    @validator("tipo")
    def tipo_valido(cls, v):
        if v not in ("ingreso", "gasto"):
            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'")
        return v

    @validator("cantidad")
    def cantidad_positiva(cls, v):
        if v <= 0:
            raise ValueError("La cantidad debe ser un número positivo")
        return v

    @validator("descripcion")  # ← Validación para descripción obligatoria
    def descripcion_obligatoria(cls, v):
        if not v or v.strip() == "":
            raise ValueError("La descripción es obligatoria")
        return v.strip()

class TransaccionCreate(TransaccionBase):
    pass

class Transaccion(BaseModel):  # ← Schema para respuestas (sin validaciones estrictas)
    id: int
    tipo: str
    cantidad: float
    descripcion: Optional[str] = None
    fecha: datetime  # ← No opcional porque tiene default en BD

    class Config:
        orm_mode = True  # ← Pydantic V1

class TransaccionUpdate(BaseModel):
    tipo: Optional[str] = None
    cantidad: Optional[float] = Field(None, gt=0)
    descripcion: Optional[str] = None
    fecha: Optional[datetime] = None

    @validator("tipo")
    def tipo_valido(cls, v):
        if v is not None and v not in ("ingreso", "gasto"):
            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'")
        return v

    @validator("cantidad")
    def cantidad_positiva(cls, v):
        if v is not None and v <= 0:
            raise ValueError("La cantidad debe ser un número positivo")
        return v

    @validator("descripcion")
    def descripcion_no_vacia(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("La descripción no puede estar vacía")
        return v.strip() if v else v

class TransaccionDelete(BaseModel):
    mensaje: str

# Schemas para Sueldo
class SueldoBase(BaseModel):
    cantidad: float = Field(..., gt=0, description="Debe ser mayor que 0")
    mes: int = Field(..., ge=1, le=12, description="Mes debe estar entre 1 y 12")
    anio: int = Field(..., ge=2020, description="Año debe ser mayor o igual a 2020")

    @validator("mes")
    def mes_valido(cls, v):
        if not (1 <= v <= 12):
            raise ValueError("El mes debe estar entre 1 y 12")
        return v

    @validator("anio")
    def anio_valido(cls, v):
        if v < 2020 or v > 2030:
            raise ValueError("El año debe estar entre 2020 y 2030")
        return v

class SueldoCreate(SueldoBase):
    pass

class Sueldo(BaseModel):
    id: int
    cantidad: float
    mes: int
    anio: int
    fecha: datetime  # ← No opcional porque tiene default en BD

    class Config:
        orm_mode = True  # ← Pydantic V1

# Schemas para autenticación
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str  # Contraseña en texto plano (solo para registro/login)

class UserLogin(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[str] = None
