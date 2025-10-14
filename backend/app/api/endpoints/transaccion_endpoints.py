"""
Transaccion Controller - Endpoints de transacciones
Solo coordinan entre DTOs y Use Cases
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from ...application.dtos.common_dtos import TransaccionCreateDTO, TransaccionResponseDTO, BalanceRequestDTO, TransaccionUpdateDTO
from ...application.use_cases.transaccion.crear_transaccion import CrearTransaccionUseCase
from ...application.use_cases.balance.calcular_balance import CalcularBalanceUseCase
from ...application.use_cases.transaccion.obtener_transacciones import ObtenerTransaccionesUseCase
from ...application.use_cases.transaccion.actualizar_transaccion import ActualizarTransaccionUseCase
from ...application.use_cases.transaccion.eliminar_transaccion import EliminarTransaccionUseCase
from ...domain.entities.usuario import Usuario
from ..dependencies.container import get_crear_transaccion_use_case, get_calcular_balance_use_case, get_obtener_transacciones_use_case, get_actualizar_transaccion_use_case, get_eliminar_transaccion_use_case
from ..dependencies.auth import get_current_user_from_token

router = APIRouter(prefix="/transacciones", tags=["transacciones"])



@router.post("/", response_model=TransaccionResponseDTO)
def crear_transaccion(
    request: TransaccionCreateDTO,
    current_user: Usuario = Depends(get_current_user_from_token),  # JWT auth
    crear_transaccion_uc: CrearTransaccionUseCase = Depends(get_crear_transaccion_use_case)
):
    """
    Crear nueva transacción
    Controller que solo coordina DTO → Use Case → Response
    """
    try:
        # Ejecutar caso de uso
        transaccion = crear_transaccion_uc.execute(
            user_id=current_user.id,
            tipo=request.tipo,
            cantidad=request.cantidad,
            descripcion=request.descripcion,
            fecha=request.fecha
        )
        
        # Convertir a DTO de respuesta
        return TransaccionResponseDTO(
            id=transaccion.id,
            tipo=transaccion.tipo,
            cantidad=transaccion.cantidad,
            fecha=transaccion.fecha,
            descripcion=transaccion.descripcion,
            user_id=transaccion.user_id
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/balance")
def obtener_balance(
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    current_user: Usuario = Depends(get_current_user_from_token),
    calcular_balance_uc: CalcularBalanceUseCase = Depends(get_calcular_balance_use_case)
):
    """
    Obtener balance financiero del usuario
    """
    try:
        # Ejecutar caso de uso
        balance = calcular_balance_uc.execute(
            user_id=current_user.id,
            mes=mes,
            anio=anio
        )
        
        return balance
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[TransaccionResponseDTO])
def obtener_transacciones(
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    current_user: Usuario = Depends(get_current_user_from_token),
    obtener_transacciones_uc: ObtenerTransaccionesUseCase = Depends(get_obtener_transacciones_use_case)
):
    """
    Obtener transacciones del usuario con filtros opcionales
    """
    try:
        # Ejecutar caso de uso
        transacciones = obtener_transacciones_uc.execute(
            user_id=current_user.id,
            mes=mes,
            anio=anio
        )
        
        # Convertir a lista de DTOs de respuesta
        return [
            TransaccionResponseDTO(
                id=t.id,
                tipo=t.tipo,
                cantidad=t.cantidad,
                fecha=t.fecha,
                descripcion=t.descripcion,
                user_id=t.user_id
            ) for t in transacciones
        ]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{transaccion_id}", response_model=TransaccionResponseDTO)
def actualizar_transaccion(
    transaccion_id: int,
    request: TransaccionUpdateDTO,
    current_user: Usuario = Depends(get_current_user_from_token),  # JWT auth
    actualizar_transaccion_uc: ActualizarTransaccionUseCase = Depends(get_actualizar_transaccion_use_case)
):
    """
    Actualizar transacción existente
    """
    try:
        # Ejecutar caso de uso
        transaccion = actualizar_transaccion_uc.execute(
            user_id=current_user.id,
            transaccion_id=transaccion_id,
            tipo=request.tipo,
            cantidad=request.cantidad,
            descripcion=request.descripcion,
            fecha=request.fecha
        )

        return TransaccionResponseDTO(
            id=transaccion.id,
            tipo=transaccion.tipo,
            cantidad=transaccion.cantidad,
            fecha=transaccion.fecha,
            descripcion=transaccion.descripcion,
            user_id=transaccion.user_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transaccion(
    transaccion_id: int,
    current_user: Usuario = Depends(get_current_user_from_token),  # JWT auth
    eliminar_transaccion_uc: EliminarTransaccionUseCase = Depends(get_eliminar_transaccion_use_case)
):
    """
    Eliminar transacción existente
    """
    try:
        # Ejecutar caso de uso
        eliminar_transaccion_uc.execute(
            user_id=current_user.id,
            transaccion_id=transaccion_id
        )

        return {"detail": "Transacción eliminada exitosamente"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
