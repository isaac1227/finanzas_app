import { Link } from "react-router-dom";

const Navbar = () => (
  <nav className="navbar navbar-expand-lg navbar-light bg-light p-3 mb-4">
    <Link className="navbar-brand" to="/">Inicio</Link>
    <Link className="nav-link" to="/transacciones">Transacciones</Link>
  </nav>
);

export default Navbar;
