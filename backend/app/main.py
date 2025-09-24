from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from fastapi import HTTPException

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Finanzas App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Bienvenido a tu app de finanzas"}

@app.post("/transacciones", response_model=schemas.Transaccion)
def crear_transaccion(transaccion: schemas.TransaccionCreate, db: Session = Depends(database.get_db)):
    return crud.crear_transaccion(db, transaccion)

@app.get("/transacciones", response_model=list[schemas.Transaccion])
def leer_transacciones(mes: int = None, anio: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.obtener_transacciones(db, mes=mes, anio=anio, skip=skip, limit=limit)

@app.put("/transacciones/{transaccion_id}", response_model=schemas.Transaccion)
def actualizar_transaccion(transaccion_id: int, transaccion: schemas.TransaccionUpdate, db: Session = Depends(database.get_db)):
    db_trans = crud.actualizar_transaccion(db, transaccion_id, transaccion)
    if not db_trans:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_trans

@app.delete("/transacciones/{transaccion_id}", response_model=schemas.Transaccion)
def eliminar_transaccion(transaccion_id: int, db: Session = Depends(database.get_db)):
    db_trans = crud.eliminar_transaccion(db, transaccion_id)
    if db_trans is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return db_trans

# Endpoints para Sueldos
@app.post("/sueldos", response_model=schemas.Sueldo)
def crear_o_actualizar_sueldo(sueldo: schemas.SueldoCreate, db: Session = Depends(database.get_db)):
    return crud.crear_o_actualizar_sueldo(db, sueldo)

@app.get("/sueldos/{anio}/{mes}", response_model=schemas.Sueldo | None)
def obtener_sueldo_mes(anio: int, mes: int, db: Session = Depends(database.get_db)):
    return crud.obtener_sueldo_mes(db, mes, anio)

@app.get("/sueldos", response_model=list[schemas.Sueldo])
def obtener_sueldos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.obtener_sueldos(db, skip=skip, limit=limit)

@app.get("/saldo-total")
def obtener_saldo_total(mes: int = None, anio: int = None, db: Session = Depends(database.get_db)):
    # Si no se especifica mes/año, usar el mes actual
    if not mes or not anio:
        from datetime import datetime
        fecha_actual = datetime.now()
        mes = fecha_actual.month
        anio = fecha_actual.year
    
    # Obtener transacciones del mes específico
    transacciones = crud.obtener_transacciones(db, mes=mes, anio=anio, skip=0, limit=10000)
    
    # Calcular saldo de transacciones del mes
    saldo_transacciones = 0
    for t in transacciones:
        if t.tipo == "ingreso":
            saldo_transacciones += t.cantidad
        elif t.tipo == "gasto":
            saldo_transacciones -= t.cantidad
    
    # Obtener sueldo del mes específico
    sueldo_mes = crud.obtener_sueldo_mes(db, mes, anio)
    saldo_sueldo = sueldo_mes.cantidad if sueldo_mes else 0
    
    saldo_total = saldo_transacciones + saldo_sueldo
    
    return {
        "saldo_total": saldo_total,
        "saldo_transacciones": saldo_transacciones,
        "saldo_sueldo": saldo_sueldo,
        "mes": mes,
        "anio": anio
    }
