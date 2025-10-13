import { render, screen } from '@testing-library/react';
import App from './App';

test('renderiza correctamente la aplicación', () => {
  render(<App />);
  // Verificar que la aplicación se renderiza con el login de usuario
  // Usamos una expresión regular para permitir variaciones como emojis (p. ej., "🔑 Iniciar sesión")
  expect(screen.getByRole('heading', { name: /iniciar sesión/i })).toBeInTheDocument();
});
