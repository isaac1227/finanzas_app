# Caso de uso básico para calcular balance

from app.infrastructure.database.models import TransaccionORM, SueldoORM
from app.infrastructure.config.database import SessionLocal
from sqlalchemy import extract

class CalcularBalanceUseCase:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def execute(self, user_id: int, mes: int = None, anio: int = None):
        query = self.db.query(TransaccionORM).filter(TransaccionORM.user_id == user_id)
        if mes:
            query = query.filter(extract('month', TransaccionORM.fecha) == mes)
        if anio:
            query = query.filter(extract('year', TransaccionORM.fecha) == anio)
        transacciones = query.all()
        ingresos = sum(t.cantidad for t in transacciones if t.tipo == 'ingreso')
        gastos = sum(t.cantidad for t in transacciones if t.tipo == 'gasto')
        saldo_transacciones = ingresos - gastos
        sueldo = self.db.query(SueldoORM).filter(SueldoORM.user_id == user_id)
        if mes:
            sueldo = sueldo.filter(SueldoORM.mes == mes)
        if anio:
            sueldo = sueldo.filter(SueldoORM.anio == anio)
        sueldo_mes = sueldo.first()
        saldo_sueldo = sueldo_mes.cantidad if sueldo_mes else 0
        saldo_total = saldo_transacciones + saldo_sueldo
        return {
            "saldo_total": saldo_total,
            "saldo_transacciones": saldo_transacciones,
            "saldo_sueldo": saldo_sueldo,
            "mes": mes,
            "anio": anio
        }
