# Caso de uso básico para crear transacción
from app.infrastructure.database.models import TransaccionORM
from app.infrastructure.config.database import SessionLocal
from fastapi import HTTPException, status
from datetime import datetime

class CrearTransaccionUseCase:
    def __init__(self, db_session=None):
        self.db = db_session or SessionLocal()

    def execute(self, user_id: int, tipo: str, cantidad: float, descripcion: str = None, fecha: str = None) -> TransaccionORM:
        """
        Ejecuta el caso de uso para crear una nueva transacción
        
        Args:
            user_id: ID del usuario que crea la transacción
            tipo: Tipo de transacción ('ingreso' o 'gasto')
            cantidad: Cantidad de la transacción
            descripcion: Descripción opcional de la transacción
            fecha: Fecha de la transacción en formato YYYY-MM-DD
        
        Returns:
            TransaccionORM: La transacción creada
        """
        try:
            # Crear la transacción con la fecha proporcionada
            nueva_transaccion = TransaccionORM(
                user_id=user_id,
                tipo=tipo,
                cantidad=cantidad,
                descripcion=descripcion
            )
            
            # Si se proporciona una fecha, la asignamos (convertir string a datetime)
            if fecha:
                try:
                    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                    nueva_transaccion.fecha = fecha_obj
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Formato de fecha inválido. Use YYYY-MM-DD"
                    )
            
            self.db.add(nueva_transaccion)
            self.db.commit()
            self.db.refresh(nueva_transaccion)
            return nueva_transaccion
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear la transacción: {str(e)}"
            )