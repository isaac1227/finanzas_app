"""
Caso de uso: Actualizar transacción
"""

from app.infrastructure.database.models import TransaccionORM
from app.infrastructure.config.database import SessionLocal

class ActualizarTransaccionUseCase:
	def __init__(self, db_session=None):
		self.db = db_session or SessionLocal()

	def execute(self, user_id: int, transaccion_id: int, tipo: str | None = None, cantidad: float | None = None, descripcion: str | None = None):
		transaccion = self.db.query(TransaccionORM).filter(TransaccionORM.id == transaccion_id, TransaccionORM.user_id == user_id).first()
		if not transaccion:
			raise ValueError("Transacción no encontrada")
		# Solo actualizar campos provistos (evitar escribir None en NOT NULL)
		if tipo is not None:
			transaccion.tipo = tipo
		if cantidad is not None:
			transaccion.cantidad = cantidad
		# descripcion puede ser nullable; si viene explícitamente, la aplicamos
		if descripcion is not None:
			transaccion.descripcion = descripcion
		self.db.commit()
		self.db.refresh(transaccion)
		return transaccion
