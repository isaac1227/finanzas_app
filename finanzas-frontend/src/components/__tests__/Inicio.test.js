import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Inicio from '../Inicio';

// 🎭 MOCK de fetch para simular API
global.fetch = jest.fn();

// 🎯 MOCK del componente Graficos (complejo de testear)
jest.mock('../Graficos', () => {
  return function MockGraficos() {
    return <div data-testid="graficos-component">Gráficos Mock</div>;
  };
});

// 🔧 Helper: Envolver con Router
const InicioWithRouter = ({ mesGlobal = 10, setMesGlobal = jest.fn(), añoGlobal = 2025 }) => (
  <BrowserRouter>
    <Inicio 
      mesGlobal={mesGlobal} 
      setMesGlobal={setMesGlobal} 
      añoGlobal={añoGlobal} 
    />
  </BrowserRouter>
);

describe('Inicio Component - Tests Complejos', () => {
  beforeEach(() => {
    // 🧹 Limpiar mocks antes de cada test
    jest.clearAllMocks();
    fetch.mockClear();
  });

  // 🧪 TEST 1: Loading State
  test('muestra loading mientras carga datos', async () => {
    // Simular API lenta (nunca resuelve)
    fetch.mockImplementation(() => new Promise(() => {}));
    
    render(<InicioWithRouter />);
    
    // Verificar que se muestra loading
    expect(screen.getByText('Cargando...')).toBeInTheDocument();
    expect(screen.getByText('Inicio')).toBeInTheDocument();
  });

  // 🧪 TEST 2: Carga exitosa de datos
  test('carga y muestra saldo total correctamente', async () => {
    // 🎭 Simular respuestas de API exitosas
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          saldo_total: 1500.50,
          saldo_transacciones: -500.50,
          saldo_sueldo: 2000
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 1,
          cantidad: 2000,
          mes: 10,
          anio: 2025
        })
      });

    render(<InicioWithRouter mesGlobal={10} añoGlobal={2025} />);

    // ⏱️ Esperar que se carguen los datos
    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });

    // ✅ Verificar contenido renderizado
    expect(screen.getByText('Saldo de Octubre 2025')).toBeInTheDocument();
    expect(screen.getByText('1500.5 €')).toBeInTheDocument();
    
    // Buscar texto específico dentro del contexto de "Sueldo"
    expect(screen.getByText('Sueldo')).toBeInTheDocument();
    const sueldoElements = screen.getAllByText('2000 €');
    expect(sueldoElements.length).toBeGreaterThan(0);
    
    // Verificar que se hicieron las llamadas correctas
    expect(fetch).toHaveBeenCalledTimes(2);
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/saldo-total?mes=10&anio=2025');
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/sueldos/2025/10');
  });

  // 🧪 TEST 3: Manejo de errores de API
  test('maneja errores de API gracefully', async () => {
    // 💥 Simular error de red
    fetch.mockRejectedValue(new Error('Network error'));
    
    // 🚨 Espiar console.error para verificar que se logea
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    render(<InicioWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });

    // Verificar que maneja el error sin crashear
    expect(consoleSpy).toHaveBeenCalledWith('Error al cargar saldo total:', expect.any(Error));
    expect(consoleSpy).toHaveBeenCalledWith('Error al cargar sueldo:', expect.any(Error));
    
    consoleSpy.mockRestore();
  });

  // 🧪 TEST 4: Interacciones del usuario - Cambiar mes
  test('permite cambiar el mes via selector', async () => {
    const mockSetMesGlobal = jest.fn();
    
    // API exitosa
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ saldo_total: 0, saldo_transacciones: 0, saldo_sueldo: 0 })
    });

    render(<InicioWithRouter setMesGlobal={mockSetMesGlobal} />);

    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });

    // 🔽 Encontrar y cambiar el selector de mes
    const selectMes = screen.getByDisplayValue('Octubre');
    fireEvent.change(selectMes, { target: { value: '3' } });

    // ✅ Verificar que se llamó la función
    expect(mockSetMesGlobal).toHaveBeenCalledWith(3);
  });

  // 🧪 TEST 5: Edición de sueldo (Complejo)
  test('permite editar y guardar sueldo', async () => {
    // Configurar mocks para flujo completo
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ saldo_total: 1000, saldo_transacciones: 0, saldo_sueldo: 1000 })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, cantidad: 1000, mes: 10, anio: 2025 })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 1, cantidad: 2500, mes: 10, anio: 2025 })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ saldo_total: 2500, saldo_transacciones: 0, saldo_sueldo: 2500 })
      });

    render(<InicioWithRouter />);

    // Esperar carga inicial - buscar elemento específico
    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
      expect(screen.getAllByText('1000 €').length).toBeGreaterThan(0);
    });

    // 🖊️ Hacer clic en "Editar"
    const editarBtn = screen.getByText('✏️ Editar');
    fireEvent.click(editarBtn);

    // 📝 Cambiar el valor en el input
    const inputSueldo = screen.getByDisplayValue('1000');
    fireEvent.change(inputSueldo, { target: { value: '2500' } });

    // 💾 Guardar
    const guardarBtn = screen.getByText('💾 Guardar');
    fireEvent.click(guardarBtn);

    // ✅ Verificar que se actualizó (múltiples elementos con 2500 €)
    await waitFor(() => {
      const elementos2500 = screen.getAllByText('2500 €');
      expect(elementos2500.length).toBeGreaterThan(0);
    });

    // Verificar llamada a API de guardado
    expect(fetch).toHaveBeenCalledWith('http://127.0.0.1:8000/sueldos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        cantidad: 2500,
        mes: 10,
        anio: 2025
      })
    });
  });

  // 🧪 TEST 6: Validación de entrada inválida
  test('valida entrada de sueldo inválida', async () => {
    // Mock de window.alert
    window.alert = jest.fn();
    
    fetch.mockResolvedValue({
      ok: true,
      json: async () => ({ saldo_total: 0, saldo_transacciones: 0, saldo_sueldo: 0 })
    });

    render(<InicioWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('Dashboard')).toBeInTheDocument();
    });

    // Encontrar botón "Añadir Sueldo" (cuando no hay sueldo)
    const agregarBtn = screen.getByText('➕ Añadir Sueldo');
    fireEvent.click(agregarBtn);

    // Intentar guardar con input vacío
    const guardarBtn = screen.getByText('💾 Guardar');
    fireEvent.click(guardarBtn);

    // Verificar validación
    expect(window.alert).toHaveBeenCalledWith('Por favor ingresa una cantidad válida');
  });
});
