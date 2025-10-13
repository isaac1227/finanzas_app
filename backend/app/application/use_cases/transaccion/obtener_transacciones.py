# Caso de uso básico para obtener transacciones

from app.infrastructure.database.models import TransaccionORM
from app.infrastructure.config.database import SessionLocal
from sqlalchemy import extract

class ObtenerTransaccionesUseCase:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def execute(self, user_id: int, mes: int = None, anio: int = None, skip: int = 0, limit: int = 100):
        query = self.db.query(TransaccionORM).filter(TransaccionORM.user_id == user_id)
        if mes:
            query = query.filter(extract('month', TransaccionORM.fecha) == mes)
        if anio:
            query = query.filter(extract('year', TransaccionORM.fecha) == anio)
        return query.offset(skip).limit(limit).all()