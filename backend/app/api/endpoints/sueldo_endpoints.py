"""
Endpoints de Sueldos y Balance
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ...application.dtos.common_dtos import SueldoCreateDTO, SueldoResponseDTO, BalanceResponseDTO
from ...domain.entities.usuario import Usuario
from ..dependencies.auth import get_current_user_from_token
from ..dependencies.container import (
    get_crear_sueldo_use_case,
    get_obtener_sueldo_use_case,
    get_obtener_sueldos_use_case,
    get_calcular_balance_use_case,
    get_actualizar_sueldo_use_case
)

router = APIRouter(prefix="/sueldos", tags=["sueldos"])


@router.post("/", response_model=SueldoResponseDTO)
def crear_o_actualizar_sueldo(
    request: SueldoCreateDTO,
    current_user: Usuario = Depends(get_current_user_from_token),
    crear_sueldo_uc = Depends(get_crear_sueldo_use_case)
):
    """Crear o actualizar sueldo del usuario"""
    try:
        sueldo = crear_sueldo_uc.execute(user_id=current_user.id, cantidad=request.cantidad, mes=request.mes, anio=request.anio)
        return SueldoResponseDTO(
            id=sueldo.id,
            cantidad=sueldo.cantidad,
            mes=sueldo.mes,
            anio=sueldo.anio,
            fecha=sueldo.fecha,
            user_id=sueldo.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{anio}/{mes}", response_model=SueldoResponseDTO)
def obtener_sueldo_mes(
    anio: int,
    mes: int,
    current_user: Usuario = Depends(get_current_user_from_token),
    obtener_sueldo_uc = Depends(get_obtener_sueldo_use_case)
):
    """Obtener sueldo de un mes específico"""
    sueldo = obtener_sueldo_uc.execute(user_id=current_user.id, mes=mes, anio=anio)
    if sueldo is None:
        raise HTTPException(status_code=404, detail=f"Sueldo no encontrado para el mes {mes} de {anio}")
    return SueldoResponseDTO(
        id=sueldo.id,
        cantidad=sueldo.cantidad,
        mes=sueldo.mes,
        anio=sueldo.anio,
        fecha=sueldo.fecha,
        user_id=sueldo.user_id
    )

@router.get("/", response_model=List[SueldoResponseDTO])
def obtener_sueldos(
    skip: int = 0,
    limit: int = 100,
    current_user: Usuario = Depends(get_current_user_from_token),
    obtener_sueldos_uc = Depends(get_obtener_sueldos_use_case)
):
    """Obtener todos los sueldos del usuario"""
    sueldos = obtener_sueldos_uc.execute(user_id=current_user.id, skip=skip, limit=limit)
    return [
        SueldoResponseDTO(
            id=s.id,
            cantidad=s.cantidad,
            mes=s.mes,
            anio=s.anio,
            fecha=s.fecha,
            user_id=s.user_id
        ) for s in sueldos
    ]

@router.get("/balance", response_model=BalanceResponseDTO)
def obtener_saldo_total(
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    current_user: Usuario = Depends(get_current_user_from_token),
    calcular_balance_uc = Depends(get_calcular_balance_use_case)
):
    """Obtener saldo total del usuario para un mes/año"""
    saldo = calcular_balance_uc.execute(user_id=current_user.id, mes=mes, anio=anio)
    return saldo

@router.put("/", response_model=SueldoResponseDTO)
def actualizar_sueldo(
    request: SueldoCreateDTO,
    current_user: Usuario = Depends(get_current_user_from_token),
    actualizar_sueldo_uc = Depends(get_actualizar_sueldo_use_case)
):
    """Actualizar sueldo del usuario"""
    try:
        sueldo = actualizar_sueldo_uc.execute(user_id=current_user.id, cantidad=request.cantidad, mes=request.mes, anio=request.anio)
        return SueldoResponseDTO(
            id=sueldo.id,
            cantidad=sueldo.cantidad,
            mes=sueldo.mes,
            anio=sueldo.anio,
            fecha=sueldo.fecha,
            user_id=sueldo.user_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
