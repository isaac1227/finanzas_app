import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Navbar from '../Navbar';

// Helper: Envolver componente con Router (necesario para Link)
const NavbarWithRouter = () => (
  <BrowserRouter>
    <Navbar />
  </BrowserRouter>
);

describe('Navbar Component', () => {
  test('renderiza los enlaces principales', () => {
    // 1. RENDERIZAR componente
    render(<NavbarWithRouter />);
    
    // 2. BUSCAR elementos que el usuario ve
    expect(screen.getByText('Inicio')).toBeInTheDocument();
    expect(screen.getByText('Transacciones')).toBeInTheDocument();
  });
  
  test('los enlaces tienen las rutas correctas', () => {
    render(<NavbarWithRouter />);
    
    // Buscar por rol de enlace y verificar href
    const inicioLink = screen.getByRole('link', { name: 'Inicio' });
    const transaccionesLink = screen.getByRole('link', { name: 'Transacciones' });
    
    expect(inicioLink).toHaveAttribute('href', '/');
    expect(transaccionesLink).toHaveAttribute('href', '/transacciones');
  });
});