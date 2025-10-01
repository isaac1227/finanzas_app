import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Graficos from '../Graficos';

// 🎭 MOCK de fetch
global.fetch = jest.fn();

// 🎯 MOCK de Chart.js - los componentes de gráficos son complejos de testear
jest.mock('react-chartjs-2', () => ({
  Bar: function MockBar({ data, options }) {
    return (
      <div data-testid="chart-component">
        <div data-testid="chart-data">{JSON.stringify(data)}</div>
        <div data-testid="chart-options">{JSON.stringify(options)}</div>
      </div>
    );
  }
}));

// Mock Chart.js registration
jest.mock('chart.js', () => ({
  Chart: {
    register: jest.fn()
  },
  CategoryScale: jest.fn(),
  LinearScale: jest.fn(),
  BarElement: jest.fn(),
  Title: jest.fn(),
  Tooltip: jest.fn(),
  Legend: jest.fn()
}));

// 🔧 Helper: Envolver con Router
const GraficosWithRouter = ({ 
  mesGlobal = 10, 
  setMesGlobal = jest.fn(), 
  añoGlobal = 2025, 
  hideSelector = false 
}) => (
  <BrowserRouter>
    <Graficos 
      mesGlobal={mesGlobal} 
      setMesGlobal={setMesGlobal} 
      añoGlobal={añoGlobal}
      hideSelector={hideSelector}
    />
  </BrowserRouter>
);

describe('Graficos Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    fetch.mockClear();
  });

  // 🧪 TEST 1: Loading State
  test('muestra spinner de carga', async () => {
    fetch.mockImplementation(() => new Promise(() => {}));
    
    render(<GraficosWithRouter />);
    
    expect(screen.getByText('Cargando gráfico...')).toBeInTheDocument();
    expect(screen.getByText('Cargando...')).toBeInTheDocument();
    
    // Verificar spinner
    const spinner = document.querySelector('.spinner-border');
    expect(spinner).toBeInTheDocument();
  });

  // 🧪 TEST 2: Datos vacíos - Sin transacciones
  test('muestra mensaje cuando no hay datos', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    render(<GraficosWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('📊 Análisis Financiero')).toBeInTheDocument();
      expect(screen.getByText('No hay datos para mostrar')).toBeInTheDocument();
      expect(screen.getByText('No hay transacciones registradas en Octubre 2025')).toBeInTheDocument();
      expect(screen.getByText('¡Añade tu primera transacción para ver el análisis!')).toBeInTheDocument();
    });

    // Verificar cards de resumen con valores 0
    expect(screen.getByText('Gastos Totales')).toBeInTheDocument();
    expect(screen.getByText('Ingresos Totales')).toBeInTheDocument();
    expect(screen.getByText('Balance')).toBeInTheDocument();
    expect(screen.getByText('Tasa Ahorro')).toBeInTheDocument();
    
    expect(screen.getAllByText('0.00 €')).toHaveLength(2); // Gastos, Ingresos
    expect(screen.getByText('+0.00 €')).toBeInTheDocument(); // Balance
    expect(screen.getByText('0%')).toBeInTheDocument(); // Tasa Ahorro
  });

  // 🧪 TEST 3: Con datos - Gráfico visible
  test('renderiza gráfico con datos correctamente', async () => {
    const mockTransacciones = [
      { id: 1, tipo: 'gasto', cantidad: 500.75, descripcion: 'Compras' },
      { id: 2, tipo: 'ingreso', cantidad: 2000, descripcion: 'Salario' },
      { id: 3, tipo: 'gasto', cantidad: 150.25, descripcion: 'Gasolina' },
      { id: 4, tipo: 'ingreso', cantidad: 300, descripcion: 'Freelance' }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    render(<GraficosWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('📊 Análisis Financiero')).toBeInTheDocument();
      
      // Verificar cards con cálculos correctos
      // Gastos: 500.75 + 150.25 = 651.00 €
      expect(screen.getByText('651.00 €')).toBeInTheDocument();
      
      // Ingresos: 2000 + 300 = 2300.00 €
      expect(screen.getByText('2300.00 €')).toBeInTheDocument();
      
      // Balance: 2300 - 651 = +1649.00 €
      expect(screen.getByText('+1649.00 €')).toBeInTheDocument();
      
      // Tasa Ahorro: (1649 / 2300) * 100 = 71.7%
      expect(screen.getByText('71.7%')).toBeInTheDocument();
      
      // Verificar que aparece el gráfico (no el mensaje de sin datos)
      expect(screen.getByTestId('chart-component')).toBeInTheDocument();
      expect(screen.queryByText('No hay datos para mostrar')).not.toBeInTheDocument();
    });
  });

  // 🧪 TEST 4: Balance negativo
  test('muestra balance negativo correctamente', async () => {
    const mockTransacciones = [
      { id: 1, tipo: 'gasto', cantidad: 1500, descripcion: 'Gastos altos' },
      { id: 2, tipo: 'ingreso', cantidad: 1000, descripcion: 'Ingreso bajo' }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    render(<GraficosWithRouter />);

    await waitFor(() => {
      // Gastos: 1500.00 €
      expect(screen.getByText('1500.00 €')).toBeInTheDocument();
      
      // Ingresos: 1000.00 €
      expect(screen.getByText('1000.00 €')).toBeInTheDocument();
      
      // Balance: -500.00 € (sin +)
      expect(screen.getByText('-500.00 €')).toBeInTheDocument();
      
      // Tasa Ahorro: -50.0%
      expect(screen.getByText('-50.0%')).toBeInTheDocument();
    });
  });

  // 🧪 TEST 5: Selector de mes (cuando no está oculto)
  test('permite cambiar mes cuando el selector no está oculto', async () => {
    const mockSetMesGlobal = jest.fn();

    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    render(<GraficosWithRouter setMesGlobal={mockSetMesGlobal} hideSelector={false} />);

    await waitFor(() => {
      expect(screen.getByDisplayValue('Octubre')).toBeInTheDocument();
    });

    // Cambiar mes
    const selectMes = screen.getByDisplayValue('Octubre');
    fireEvent.change(selectMes, { target: { value: '5' } });

    expect(mockSetMesGlobal).toHaveBeenCalledWith(5);
  });

  // 🧪 TEST 6: Selector oculto
  test('oculta selector cuando hideSelector es true', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    render(<GraficosWithRouter hideSelector={true} />);

    await waitFor(() => {
      expect(screen.getByText('📊 Análisis Financiero')).toBeInTheDocument();
      // No debe existir el selector
      expect(screen.queryByDisplayValue('Octubre')).not.toBeInTheDocument();
    });
  });

  // 🧪 TEST 7: Título dinámico del gráfico
  test('muestra título correcto según mes y año', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => [
        { id: 1, tipo: 'gasto', cantidad: 100, descripcion: 'Test' }
      ]
    });

    render(<GraficosWithRouter mesGlobal={3} añoGlobal={2024} />);

    await waitFor(() => {
      // Verificar que el gráfico tiene los datos del título correcto
      const chartComponent = screen.getByTestId('chart-component');
      expect(chartComponent).toBeInTheDocument();
      
      // El título debería incluir "Marzo 2024"
      const chartOptions = screen.getByTestId('chart-options');
      expect(chartOptions.textContent).toContain('Marzo 2024');
    });
  });

  // 🧪 TEST 8: Datos del gráfico
  test('configura datos del gráfico correctamente', async () => {
    const mockTransacciones = [
      { id: 1, tipo: 'gasto', cantidad: 250, descripcion: 'Compra' },
      { id: 2, tipo: 'ingreso', cantidad: 800, descripcion: 'Pago' }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    render(<GraficosWithRouter />);

    await waitFor(() => {
      const chartData = screen.getByTestId('chart-data');
      const dataObj = JSON.parse(chartData.textContent);
      
      // Verificar estructura de datos
      expect(dataObj.labels).toEqual(['💸 Gastos', '💰 Ingresos']);
      expect(dataObj.datasets[0].data).toEqual([250, 800]);
      expect(dataObj.datasets[0].label).toBe('Cantidad (€)');
    });
  });

  // 🧪 TEST 9: Manejo de errores de API
  test('maneja errores de red gracefully', async () => {
    fetch.mockRejectedValue(new Error('Network error'));
    
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    render(<GraficosWithRouter />);

    await waitFor(() => {
      // Debe mostrar datos vacíos cuando hay error
      expect(screen.getByText('No hay datos para mostrar')).toBeInTheDocument();
      // Solo gastos e ingresos muestran "0.00 €", el balance muestra "+0.00 €"
      expect(screen.getAllByText('0.00 €')).toHaveLength(2);
    });

    expect(consoleSpy).toHaveBeenCalledWith('Error al cargar datos:', expect.any(Error));
    consoleSpy.mockRestore();
  });

  // 🧪 TEST 10: Iconos y elementos visuales
  test('renderiza todos los iconos y elementos visuales', async () => {
    const mockTransacciones = [
      { id: 1, tipo: 'gasto', cantidad: 100, descripcion: 'Test' }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    render(<GraficosWithRouter />);

    await waitFor(() => {
      // Verificar iconos en los títulos de las cards
      expect(screen.getByText('Gastos Totales')).toBeInTheDocument();
      expect(screen.getByText('Ingresos Totales')).toBeInTheDocument();
      expect(screen.getByText('Balance')).toBeInTheDocument();
      expect(screen.getByText('Tasa Ahorro')).toBeInTheDocument();
      
      // Verificar que las clases CSS correctas están aplicadas
      const gastoCard = screen.getByText('Gastos Totales').closest('.card');
      expect(gastoCard).toHaveClass('bg-danger-subtle');
      
      const ingresoCard = screen.getByText('Ingresos Totales').closest('.card');
      expect(ingresoCard).toHaveClass('bg-success-subtle');
    });
  });

  // 🧪 TEST 11: Response no OK
  test('maneja respuesta no exitosa de la API', async () => {
    fetch.mockResolvedValue({
      ok: false,
      status: 500
    });

    render(<GraficosWithRouter />);

    await waitFor(() => {
      // Debe mostrar datos vacíos cuando la respuesta no es OK
      expect(screen.getByText('No hay datos para mostrar')).toBeInTheDocument();
      // Solo gastos e ingresos muestran "0.00 €", el balance muestra "+0.00 €"
      expect(screen.getAllByText('0.00 €')).toHaveLength(2);
    });
  });

  // 🧪 TEST 12: Diferentes meses
  test('actualiza contenido cuando cambian mes y año', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    const { rerender } = render(<GraficosWithRouter mesGlobal={1} añoGlobal={2024} />);

    await waitFor(() => {
      expect(screen.getByText('No hay transacciones registradas en Enero 2024')).toBeInTheDocument();
    });

    // Cambiar props
    rerender(<GraficosWithRouter mesGlobal={12} añoGlobal={2025} />);

    await waitFor(() => {
      expect(screen.getByText('No hay transacciones registradas en Diciembre 2025')).toBeInTheDocument();
    });
  });
});
