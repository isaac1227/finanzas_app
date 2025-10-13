# Caso de uso básico para login de usuario
# Adaptación Clean Architecture: usar repositorio

from app.auth import verify_password, create_access_token

class LoginUsuarioUseCase:
    def __init__(self, usuario_repository):
        self.usuario_repository = usuario_repository

    def execute(self, email: str, password: str):
        usuario = self.usuario_repository.find_by_email(email)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        # Verificar contraseña usando función segura
        if not verify_password(password, usuario.hashed_password):
            raise ValueError("Contraseña incorrecta")
        # Generar JWT usando la función global y el email
        access_token = create_access_token({"email": usuario.email})
        return {"access_token": access_token, "token_type": "bearer"}
