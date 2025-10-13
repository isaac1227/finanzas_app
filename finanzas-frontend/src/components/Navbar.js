import { Link } from "react-router-dom";

const Navbar = ({ onLogout }) => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light p-3 mb-4">
    <Link className="navbar-brand" to="/">Inicio</Link>
    <Link className="nav-link" to="/transacciones">Transacciones</Link>
    <button 
      className="btn btn-outline-danger ms-auto" 
      onClick={onLogout}
    >
      Cerrar Sesión
    </button>
  </nav>
);

export default Navbar;
