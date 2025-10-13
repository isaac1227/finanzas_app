# Caso de uso básico para eliminar transacción
from app.infrastructure.database.models import TransaccionORM
from app.infrastructure.config.database import SessionLocal

class EliminarTransaccionUseCase:
	def __init__(self, db_session=None):
		self.db = db_session or SessionLocal()

	def execute(self, user_id: int, transaccion_id: int):
		transaccion = self.db.query(TransaccionORM).filter(TransaccionORM.id == transaccion_id, TransaccionORM.user_id == user_id).first()
		if not transaccion:
			raise ValueError("Transacción no encontrada")
		self.db.delete(transaccion)
		self.db.commit()
		return transaccion
