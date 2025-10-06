from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, crud, database, auth

# DESARROLLO: Borrar y recrear tablas para aplicar cambios de esquema
models.Base.metadata.drop_all(bind=database.engine)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Finanzas App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"], # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTPBearer - esto le dice a FastAPI que espere un token Bearer simple
security = HTTPBearer()

def get_current_user(credentials = Depends(security), db: Session = Depends(database.get_db)):
    """Función que extrae el usuario actual desde el JWT token"""
    # Extraer el token de las credenciales Bearer
    token = credentials.credentials
    # Verificar el token
    token_data = auth.verify_token(token)
    
    # Buscar el usuario en la BD
    user = crud.obtener_usuario_por_email(db, email=token_data["email"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

@app.get("/")
def root():
    return {"message": "Bienvenido a tu app de finanzas"}

# 🔐 ENDPOINTS DE AUTENTICACIÓN

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Registro de nuevo usuario"""
    
    # Verificar si el email ya existe
    db_user = crud.obtener_usuario_por_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )
    
    # Crear el usuario
    return crud.crear_usuario(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """Login del usuario - devuelve JWT token"""
    
    # Buscar usuario por email
    user = crud.obtener_usuario_por_email(db, email=form_data.username)
    
    # Verificar que existe y la contraseña es correcta
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear el token JWT
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    """Obtener información del usuario actual"""
    return current_user

# 💰 ENDPOINTS PROTEGIDOS - Solo para usuarios autenticados

@app.post("/transacciones", response_model=schemas.Transaccion)
def crear_transaccion(
    transaccion: schemas.TransaccionCreate, 
    current_user: models.Usuario = Depends(get_current_user),  # ← NUEVO: requiere autenticación
    db: Session = Depends(database.get_db)
):
    # Crear transacción asociada al usuario actual
    transaccion = crud.crear_transaccion(db, transaccion, user_id=current_user.id, fecha_custom=transaccion.fecha)
    if transaccion is None:
        raise HTTPException(
            status_code=400, 
            detail="Error al crear la transacción"
        )
    return transaccion

@app.get("/transacciones", response_model=list[schemas.Transaccion])
def leer_transacciones(
    mes: int = None, 
    anio: int = None, 
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.Usuario = Depends(get_current_user),  # ← NUEVO: requiere autenticación
    db: Session = Depends(database.get_db)
):
    # Solo devolver transacciones del usuario actual
    return crud.obtener_transacciones(db, user_id=current_user.id, mes=mes, anio=anio, skip=skip, limit=limit)

@app.put("/transacciones/{transaccion_id}", response_model=schemas.Transaccion)
def actualizar_transaccion(
    transaccion_id: int, 
    transaccion: schemas.TransaccionUpdate, 
    current_user: models.Usuario = Depends(get_current_user),  # ← NUEVO: requiere autenticación
    db: Session = Depends(database.get_db)
):
    db_trans = crud.actualizar_transaccion(db, transaccion_id, transaccion)
    if not db_trans:
        raise HTTPException(
            status_code=404, 
            detail="Transacción no encontrada"
        )
    return db_trans

@app.delete("/transacciones/{transaccion_id}", response_model=schemas.Transaccion)
def eliminar_transaccion(
    transaccion_id: int, 
    current_user: models.Usuario = Depends(get_current_user),  # ← NUEVO: requiere autenticación
    db: Session = Depends(database.get_db)
):
    db_trans = crud.eliminar_transaccion(db, transaccion_id)
    if db_trans is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_trans

# Endpoints para Sueldos
@app.post("/sueldos", response_model=schemas.Sueldo)
def crear_o_actualizar_sueldo(
    sueldo: schemas.SueldoCreate, 
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(database.get_db)):
    return crud.crear_o_actualizar_sueldo(db, sueldo, user_id=current_user.id)

@app.get("/sueldos/{anio}/{mes}", response_model=schemas.Sueldo | None)
def obtener_sueldo_mes(
    anio: int, 
    mes: int, 
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(database.get_db)):
    sueldo = crud.obtener_sueldo_mes(db, mes=mes, anio=anio, user_id=current_user.id)
    if sueldo is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Sueldo no encontrado para el mes {mes} de {anio}"
        )
    return sueldo

@app.get("/sueldos", response_model=list[schemas.Sueldo])
def obtener_sueldos(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(database.get_db)):
    return crud.obtener_sueldos(db, skip=skip, limit=limit, user_id=current_user.id)

@app.get("/saldo-total")
def obtener_saldo_total(
    mes: int = None, 
    anio: int = None, 
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(database.get_db)):
    # Si no se especifica mes/año, usar el mes actual
    if not mes or not anio:
        from datetime import datetime
        fecha_actual = datetime.now()
        mes = fecha_actual.month
        anio = fecha_actual.year
    
    # Obtener transacciones del mes específico del usuario actual
    transacciones = crud.obtener_transacciones(db, user_id=current_user.id, mes=mes, anio=anio, skip=0, limit=10000)
    
    # Calcular ingresos y gastos del usuario
    ingresos = sum(t.cantidad for t in transacciones if t.tipo == 'ingreso')
    gastos = sum(t.cantidad for t in transacciones if t.tipo == 'gasto')
    
    # Calcular saldo de transacciones del mes
    saldo_transacciones = ingresos - gastos

    # Obtener sueldo del mes específico del usuario actual
    sueldo_mes = crud.obtener_sueldo_mes(db, mes, anio, user_id=current_user.id)
    saldo_sueldo = sueldo_mes.cantidad if sueldo_mes else 0
    saldo_total = saldo_transacciones + saldo_sueldo
    
    return {
        "saldo_total": saldo_total,
        "saldo_transacciones": saldo_transacciones,
        "saldo_sueldo": saldo_sueldo,
        "mes": mes,
        "anio": anio
    }
    
