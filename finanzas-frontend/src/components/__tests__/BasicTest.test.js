import { render, screen } from '@testing-library/react';

// Test súper simple sin dependencias externas
describe('Testing Environment', () => {
  test('Jest y React Testing Library funcionan', () => {
    // Renderizar un elemento simple
    render(<div data-testid="test">Hello World</div>);
    
    // Verificar que se renderiza
    expect(screen.getByTestId('test')).toBeInTheDocument();
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });
});