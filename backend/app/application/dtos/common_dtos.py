"""
DTOs - Data Transfer Objects
Objetos para transferir datos entre capas de la aplicación
"""
from pydantic import BaseModel, EmailStr, Field
# ========== BALANCE RESPONSE DTO ==========
class BalanceResponseDTO(BaseModel):
    saldo_total: float
    saldo_transacciones: float
    saldo_sueldo: float
    mes: int
    anio: int
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoTransaccion(str, Enum):
    """Enum para tipos de transacción válidos"""
    INGRESO = "ingreso"
    GASTO = "gasto"


class UserCreateDTO(BaseModel):
    """DTO para crear usuario"""
    email: EmailStr = Field(
        description="Email único del usuario",
        example="usuario@ejemplo.com"
    )
    password: str = Field(
        min_length=6,
        description="Contraseña (mínimo 6 caracteres)",
        example="mipassword123"
    )


class UserLoginDTO(BaseModel):
    """DTO para login de usuario"""
    email: EmailStr = Field(
        description="Email del usuario registrado",
        example="usuario@ejemplo.com"
    )
    password: str = Field(
        description="Contraseña del usuario",
        example="mipassword123"
    )


class TransaccionCreateDTO(BaseModel):
    """DTO para crear transacción"""
    tipo: TipoTransaccion = Field(
        default=TipoTransaccion.GASTO,
        description="Tipo de transacción: ingreso o gasto",
        example="gasto"
    )
    cantidad: float = Field(
        gt=0,
        description="Cantidad de la transacción (debe ser positiva)",
        example=50.0
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Descripción opcional de la transacción",
        example="Compra en supermercado"
    )
    fecha: Optional[str] = Field(
        default=None,
        description="Fecha de la transacción en formato YYYY-MM-DD",
        example="2024-11-15"
    )


class SueldoCreateDTO(BaseModel):
    """DTO para crear/actualizar sueldo"""
    cantidad: float = Field(
        gt=0,
        description="Cantidad del sueldo (debe ser positiva)",
        example=2000.0
    )
    mes: int = Field(
        ge=1, le=12,
        description="Mes del sueldo (1-12)",
        example=10
    )
    anio: int = Field(
        ge=2020, le=2030,
        description="Año del sueldo",
        example=2025
    )


class BalanceRequestDTO(BaseModel):
    """DTO para solicitar balance"""
    mes: Optional[int] = None
    anio: Optional[int] = None


# ========== RESPONSE DTOs ==========

class UserResponseDTO(BaseModel):
    """DTO de respuesta para usuario"""
    id: int
    email: str
    is_active: bool
    created_at: datetime


class TransaccionResponseDTO(BaseModel):
    """DTO de respuesta para transacción"""
    id: int
    tipo: TipoTransaccion
    cantidad: float
    fecha: datetime
    descripcion: Optional[str] = None
    user_id: int


class SueldoResponseDTO(BaseModel):
    """DTO de respuesta para sueldo"""
    id: int
    cantidad: float
    mes: int
    anio: int
    fecha: datetime
    user_id: int


class TokenResponseDTO(BaseModel):
    """DTO de respuesta para token JWT"""
    access_token: str
    token_type: str

# ========== UPDATE DTOs ==========

class TransaccionUpdateDTO(BaseModel):
    """DTO para actualizar transacción"""
    tipo: Optional[TipoTransaccion] = Field(
        default=None,
        description="Tipo de transacción: ingreso o gasto",
        example="gasto"
    )
    cantidad: Optional[float] = Field(
        default=None,
        gt=0,
        description="Cantidad de la transacción (debe ser positiva)",
        example=50.0
    )
    descripcion: Optional[str] = Field(
        default=None,
        description="Descripción opcional de la transacción",
        example="Compra en supermercado"
    )
    fecha: Optional[datetime] = Field(
        default=None,
        description="Fecha de la transacción (ISO 8601)",
        example="2023-10-05T14:48:00.000Z"
    )