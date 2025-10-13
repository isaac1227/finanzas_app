# Caso de uso básico para obtener perfil de usuario
from app.infrastructure.database.models import UsuarioORM
from app.infrastructure.config.database import SessionLocal

class PerfilUsuarioUseCase:
	def __init__(self, db_session=None):
		self.db = db_session or SessionLocal()

	def execute(self, user_id: int):
		usuario = self.db.query(UsuarioORM).filter(UsuarioORM.id == user_id).first()
		if not usuario:
			raise ValueError("Usuario no encontrado")
		return usuario
