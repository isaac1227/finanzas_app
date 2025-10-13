import React, { useState } from 'react';
import { authService } from '../services/authService';
import toast from 'react-hot-toast';

const Login = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('usuario@ejemplo.com');
  const [password, setPassword] = useState('mipassword123');
  const [isRegister, setIsRegister] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      if (isRegister) {
        await authService.register(email, password);
        toast.success('✅ Usuario creado correctamente');
        setIsRegister(false);
      } else {
        await authService.login(email, password);
        toast.success('🎉 Bienvenido de vuelta!');
        onLoginSuccess();
      }
    } catch (error) {
      toast.error(isRegister ? '❌ Error al crear usuario' : '🚫 Credenciales incorrectas');
    }
    setLoading(false);
  };

  return (
    <div className="min-vh-100 d-flex align-items-center bg-light">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-5 col-lg-4">
            
            {/* Header con logo */}
            <div className="text-center mb-4">
              <div className="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" 
                   style={{ width: '80px', height: '80px', fontSize: '2rem' }}>
                💰
              </div>
              <h1 className="h3 text-dark mb-1">Finanzas App</h1>
              <p className="text-muted">Gestiona tus finanzas de forma segura</p>
            </div>

            {/* Card principal */}
            <div className="card border-0 shadow-lg">
              <div className="card-body p-4">
                
                {/* Título del formulario */}
                <div className="text-center mb-4">
                  <h2 className="h4 text-dark mb-2">
                    {isRegister ? '📝 Crear cuenta nueva' : '🔑 Iniciar sesión'}
                  </h2>
                  <p className="text-muted small">
                    {isRegister 
                      ? 'Únete y comienza a gestionar tus finanzas' 
                      : 'Accede a tu panel de finanzas personal'
                    }
                  </p>
                </div>
                
                {/* Formulario */}
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label className="form-label text-dark fw-semibold">
                      📧 Correo electrónico
                    </label>
                    <input
                      type="email"
                      className="form-control form-control-lg border-2"
                      placeholder="tu@email.com"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      style={{ borderRadius: '12px' }}
                    />
                  </div>
                  
                  <div className="mb-4">
                    <label className="form-label text-dark fw-semibold">
                      🔒 Contraseña
                    </label>
                    <input
                      type="password"
                      className="form-control form-control-lg border-2"
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      minLength="6"
                      style={{ borderRadius: '12px' }}
                    />
                    {isRegister && (
                      <div className="form-text text-muted">
                        Mínimo 6 caracteres para mayor seguridad
                      </div>
                    )}
                  </div>
                  
                  {/* Botón principal */}
                  <button 
                    type="submit" 
                    className={`btn btn-lg w-100 fw-semibold ${isRegister ? 'btn-success' : 'btn-primary'}`}
                    disabled={loading}
                    style={{ borderRadius: '12px', padding: '12px' }}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" />
                        Procesando...
                      </>
                    ) : (
                      isRegister ? '🚀 Crear mi cuenta' : '✨ Entrar'
                    )}
                  </button>
                </form>
                
                {/* Divisor */}
                <hr className="my-4" />
                
                {/* Cambiar modo */}
                <div className="text-center">
                  <p className="text-muted mb-2">
                    {isRegister ? '¿Ya tienes una cuenta?' : '¿Nuevo por aquí?'}
                  </p>
                  <button 
                    type="button"
                    className={`btn ${isRegister ? 'btn-outline-primary' : 'btn-outline-success'} fw-semibold`}
                    onClick={() => setIsRegister(!isRegister)}
                    style={{ borderRadius: '12px' }}
                  >
                    {isRegister ? '👋 Iniciar sesión' : '📝 Crear cuenta'}
                  </button>
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="text-center mt-4">
              <p className="text-muted small">
                🔐 Tus datos están protegidos con JWT tokens
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;