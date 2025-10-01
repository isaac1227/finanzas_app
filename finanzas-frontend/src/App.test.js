import { render, screen } from '@testing-library/react';
import App from './App';

test('renderiza correctamente la aplicación', () => {
  render(<App />);
  // Verificar que la aplicación se renderiza con el navbar y contenido inicial
  expect(screen.getByRole('heading', { name: 'Inicio' })).toBeInTheDocument();
  expect(screen.getByText('Transacciones')).toBeInTheDocument();
  expect(screen.getByText('Cargando...')).toBeInTheDocument();
});
