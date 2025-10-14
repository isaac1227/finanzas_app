import { Link } from "react-router-dom";
import { useTheme } from "../contexts/ThemeContext";
import { useState } from "react";

const Navbar = ({ onLogout }) => {
  const { theme, toggleTheme, isDark } = useTheme();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="navbar navbar-expand-lg p-3 mb-4">
      <div className="container-fluid">
        {/* Brand */}
        <Link className="navbar-brand fw-bold" to="/" onClick={closeMenu}>
          💰 Finanzas App
        </Link>
        
        {/* Hamburger Button (solo visible en móvil) */}
        <button 
          className="navbar-toggler"
          type="button"
          onClick={toggleMenu}
          aria-controls="navbarNav"
          aria-expanded={isMenuOpen}
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        {/* Contenido colapsable */}
        <div className={`collapse navbar-collapse ${isMenuOpen ? 'show' : ''}`} id="navbarNav">
          {/* Links de navegación */}
          <div className="navbar-nav me-auto">
            <Link 
              className="nav-link" 
              to="/"
              onClick={closeMenu}
            >
              🏠 Inicio
            </Link>
            <Link 
              className="nav-link" 
              to="/transacciones"
              onClick={closeMenu}
            >
              💳 Transacciones
            </Link>
          </div>

          {/* Controles del lado derecho */}
          <div className="d-flex align-items-center gap-2 flex-wrap">
            {/* Botón de cambio de tema */}
            <button 
              className="theme-toggle btn btn-outline-secondary btn-sm"
              onClick={toggleTheme}
              title={`Cambiar a tema ${isDark ? 'claro' : 'oscuro'}`}
            >
              {isDark ? '☀️' : '🌙'} 
              <span className="d-none d-md-inline ms-1">
                {isDark ? 'Claro' : 'Oscuro'}
              </span>
            </button>
            
            {/* Botón de cerrar sesión */}
            <button 
              className="btn btn-outline-danger btn-sm" 
              onClick={() => {
                onLogout();
                closeMenu();
              }}
            >
              🚪 
              <span className="d-none d-md-inline ms-1">
                Cerrar Sesión
              </span>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
