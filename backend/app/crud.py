from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from . import models, schemas
import datetime

def crear_transaccion(db: Session, transaccion: schemas.TransaccionCreate, user_id: int, fecha_custom: datetime.datetime = None):
    transaccion_dict = transaccion.dict()
    transaccion_dict['user_id'] = user_id  # ← NUEVO: asociar al usuario
    
    if transaccion.fecha:
        transaccion_dict['fecha'] = transaccion.fecha
    elif fecha_custom:
        transaccion_dict['fecha'] = fecha_custom
    
    db_trans = models.Transaccion(**transaccion_dict)
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return db_trans

def obtener_transacciones(db: Session, user_id: int, mes: int = None, anio: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Transaccion).filter(models.Transaccion.user_id == user_id)  # ← NUEVO: filtrar por usuario
    if mes:
        query = query.filter(extract('month', models.Transaccion.fecha) == mes)
    if anio:
        query = query.filter(extract('year', models.Transaccion.fecha) == anio)
    return query.offset(skip).limit(limit).all()

def obtener_transacciones_totales_mes(db: Session, mes: int = None, anio: int = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Transaccion)

    if mes:
        query = query.filter(extract('month', models.Transaccion.fecha) == mes)
    if anio:
        query = query.filter(extract('year', models.Transaccion.fecha) == anio)

    ingresos = query.filter(models.Transaccion.tipo == 'ingreso').with_entities(func.sum(models.Transaccion.cantidad)).scalar() or 0
    gastos = query.filter(models.Transaccion.tipo == 'gasto').with_entities(func.sum(models.Transaccion.cantidad)).scalar() or 0

    return ingresos, gastos

def actualizar_transaccion(db: Session, transaccion_id: int, transaccion: schemas.TransaccionUpdate):
    db_trans = db.query(models.Transaccion).filter(models.Transaccion.id == transaccion_id).first()
    
    if not db_trans:
        return None

    for key, value in transaccion.dict(exclude_unset=True).items():
        if value is not None and key != "fecha":
            setattr(db_trans, key, value)

    transaccion_dict = transaccion.dict(exclude_unset=True)
    if "fecha" in transaccion_dict and transaccion_dict["fecha"] is not None:
        if isinstance(transaccion_dict["fecha"], str):
            try:
                fecha_obj = datetime.datetime.fromisoformat(transaccion_dict["fecha"])
                db_trans.fecha = fecha_obj
            except ValueError:
                db_trans.fecha = transaccion_dict["fecha"]
        else:
            db_trans.fecha = transaccion_dict["fecha"]

    db.commit()
    db.refresh(db_trans)
    return db_trans

def eliminar_transaccion(db: Session, transaccion_id: int):
    db_trans = db.query(models.Transaccion).filter(models.Transaccion.id == transaccion_id).first()
    if not db_trans:
        return None
    db.delete(db_trans)
    db.commit()
    return db_trans

# CRUD para Sueldos
def crear_o_actualizar_sueldo(db: Session, sueldo: schemas.SueldoCreate, user_id: int):
    # Verificar si ya existe un sueldo para este mes/año/usuario
    db_sueldo = db.query(models.Sueldo).filter(
        models.Sueldo.mes == sueldo.mes,
        models.Sueldo.anio == sueldo.anio,
        models.Sueldo.user_id == user_id  # ← NUEVO: filtrar por usuario
    ).first()
    
    if db_sueldo:
        # Actualizar el existente
        db_sueldo.cantidad = sueldo.cantidad
        db.commit()
        db.refresh(db_sueldo)
        return db_sueldo
    else:
        # Crear nuevo
        sueldo_dict = sueldo.dict()
        sueldo_dict['user_id'] = user_id  # ← NUEVO: asociar al usuario
        db_sueldo = models.Sueldo(**sueldo_dict)
        db.add(db_sueldo)
        db.commit()
        db.refresh(db_sueldo)
        return db_sueldo

def obtener_sueldo_mes(db: Session, mes: int, anio: int, user_id: int):
    return db.query(models.Sueldo).filter(
        models.Sueldo.mes == mes,
        models.Sueldo.anio == anio,
        models.Sueldo.user_id == user_id  # ← NUEVO: filtrar por usuario
    ).first()

def obtener_sueldos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Sueldo).filter(models.Sueldo.user_id == user_id).order_by(models.Sueldo.anio.desc(), models.Sueldo.mes.desc()).offset(skip).limit(limit).all()

# CRUD para Usuarios
def crear_usuario(db: Session, user: schemas.UserCreate):
    """Crear un nuevo usuario con contraseña hasheada"""
    from .auth import get_password_hash
    
    # Hashear la contraseña antes de guardarla
    hashed_password = get_password_hash(user.password)
    
    db_user = models.Usuario(
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def obtener_usuario_por_email(db: Session, email: str):
    """Buscar un usuario por su email"""
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def obtener_usuario_por_id(db: Session, user_id: int):
    """Buscar un usuario por su ID"""
    return db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
