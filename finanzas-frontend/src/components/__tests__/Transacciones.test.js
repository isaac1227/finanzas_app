import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Transacciones from '../Transacciones';

// 🎭 MOCK de fetch
global.fetch = jest.fn();

// 🔧 Helper: Envolver con Router
const TransaccionesWithRouter = ({ mesGlobal = 10, setMesGlobal = jest.fn(), añoGlobal = 2025 }) => (
  <BrowserRouter>
    <Transacciones 
      mesGlobal={mesGlobal} 
      setMesGlobal={setMesGlobal} 
      añoGlobal={añoGlobal} 
    />
  </BrowserRouter>
);

describe('Transacciones Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    fetch.mockClear();
  });

  // 🧪 TEST 1: Loading State
  test('muestra loading mientras carga transacciones', async () => {
    fetch.mockImplementation(() => new Promise(() => {}));
    
    render(<TransaccionesWithRouter />);
    
    expect(screen.getByText('Cargando transacciones...')).toBeInTheDocument();
  });

  // 🧪 TEST 2: Estado vacío - Sin transacciones
  test('muestra mensaje cuando no hay transacciones', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('💰 Transacciones de Octubre 2025')).toBeInTheDocument();
      expect(screen.getByText('No hay transacciones este mes')).toBeInTheDocument();
      expect(screen.getByText('¡Añade tu primera transacción para empezar!')).toBeInTheDocument();
      expect(screen.getByText('➕ Añadir Primera Transacción')).toBeInTheDocument();
    });

    // Verificar los valores del resumen
    expect(screen.getByText('Ingresos')).toBeInTheDocument();
    expect(screen.getByText('Gastos')).toBeInTheDocument();
    expect(screen.getByText('Balance')).toBeInTheDocument();
    expect(screen.getAllByText('0 €')).toHaveLength(3); // Ingresos, Gastos, Balance
  });

  // 🧪 TEST 3: Lista con transacciones
  test('renderiza lista de transacciones correctamente', async () => {
    const mockTransacciones = [
      {
        id: 1,
        tipo: 'ingreso',
        cantidad: 1500,
        descripcion: 'Salario',
        fecha: '2025-10-15T10:00:00Z'
      },
      {
        id: 2,
        tipo: 'gasto',
        cantidad: 50.5,
        descripcion: 'Supermercado',
        fecha: '2025-10-14T15:30:00Z'
      }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    const { container } = render(<TransaccionesWithRouter />);

    await waitFor(() => {
      // Nuevo formato de encabezado con rango: (1-2 de 2)
      expect(screen.getByText(/Lista de Transacciones \(1-2 de 2\)/)).toBeInTheDocument();

      // Verificar transacciones
      expect(screen.getByText('🟢 Ingreso')).toBeInTheDocument();
      expect(screen.getByText('🔴 Gasto')).toBeInTheDocument();
      expect(screen.getByText('Salario')).toBeInTheDocument();
      expect(screen.getByText('Supermercado')).toBeInTheDocument();
      expect(screen.getByText('+1500 €')).toBeInTheDocument();
      expect(screen.getByText('-50.5 €')).toBeInTheDocument();

      // Verificar botón nueva transacción
      expect(screen.getByText('➕ Nueva Transacción')).toBeInTheDocument();
    });

    // Comprobar orden descendente por fecha (más reciente primero)
    const descripcionElems = container.querySelectorAll('strong.transaction-description');
    expect(descripcionElems[0].textContent).toBe('Salario'); // fecha 15 > 14
    expect(descripcionElems[1].textContent).toBe('Supermercado');
  });

  // 🧪 TEST 4: Cálculos del resumen
  test('calcula correctamente ingresos, gastos y balance', async () => {
    const mockTransacciones = [
      { id: 1, tipo: 'ingreso', cantidad: 2000, descripcion: 'Salario', fecha: '2025-10-01T10:00:00Z' },
      { id: 2, tipo: 'gasto', cantidad: 300, descripcion: 'Compras', fecha: '2025-10-02T15:30:00Z' },
      { id: 3, tipo: 'ingreso', cantidad: 500, descripcion: 'Freelance', fecha: '2025-10-03T12:00:00Z' },
      { id: 4, tipo: 'gasto', cantidad: 150.75, descripcion: 'Gasolina', fecha: '2025-10-04T18:00:00Z' }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      // Ingresos: 2000 + 500 = 2500 €
      expect(screen.getByText('2500 €')).toBeInTheDocument();
      // Gastos: 300 + 150.75 = 450.75 €
      expect(screen.getByText('450.75 €')).toBeInTheDocument();
      // Balance: 2500 - 450.75 = 2049.25 €
      expect(screen.getByText('2049.25 €')).toBeInTheDocument();
    });
  });

  // 🧪 TEST 5: Formulario nueva transacción
  test('permite crear nueva transacción', async () => {
    // Mock inicial - sin transacciones
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });

    // Mock POST exitoso
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, tipo: 'gasto', cantidad: 25, descripcion: 'Café' })
    });

    // Mock GET después del POST
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{ id: 1, tipo: 'gasto', cantidad: 25, descripcion: 'Café', fecha: '2025-10-15T10:00:00Z' }]
    });

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('➕ Añadir Primera Transacción')).toBeInTheDocument();
    });

    // Hacer clic en añadir transacción
    const btnAñadir = screen.getByText('➕ Añadir Primera Transacción');
    fireEvent.click(btnAñadir);

    // Verificar que aparece el formulario - buscar por texto del option
    expect(screen.getByText('🔴 Gasto')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Descripción...')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('0.00')).toBeInTheDocument();

    // Llenar formulario
    const inputDescripcion = screen.getByPlaceholderText('Descripción...');
    const inputCantidad = screen.getByPlaceholderText('0.00');
    
    fireEvent.change(inputDescripcion, { target: { value: 'Café' } });
    fireEvent.change(inputCantidad, { target: { value: '25' } });

    // Guardar
    const btnGuardar = screen.getByText('💾 Guardar');
    fireEvent.click(btnGuardar);

    // Verificar llamada a API (el componente puede incluir fecha)
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8001/transacciones', expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: expect.stringContaining('"tipo":"gasto"')
      }));
    });
  });

  // 🧪 TEST 6: Editar transacción
  test('permite editar transacción existente', async () => {
    const mockTransaccion = {
      id: 1,
      tipo: 'gasto',
      cantidad: 50,
      descripcion: 'Supermercado',
      fecha: '2025-10-15T10:00:00Z'
    };

    // Mock inicial con transacción
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [mockTransaccion]
    });

    // Mock PUT exitoso
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ ...mockTransaccion, cantidad: 75, descripcion: 'Supermercado', fecha: '2025-10-15T10:00:00Z' })
    });

    // Mock GET después del PUT
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{ ...mockTransaccion, cantidad: 75, descripcion: 'Supermercado', fecha: '2025-10-15T10:00:00Z' }]
    });

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('Supermercado')).toBeInTheDocument();
    });

    // Hacer clic en editar
    const btnEditar = screen.getByText('✏️ Editar');
    fireEvent.click(btnEditar);

    // Verificar que aparece el formulario de edición con valores pre-llenados
    expect(screen.getByDisplayValue('Supermercado')).toBeInTheDocument();
    expect(screen.getByDisplayValue('50')).toBeInTheDocument();

    // Cambiar valores
    const inputCantidad = screen.getByDisplayValue('50');
    fireEvent.change(inputCantidad, { target: { value: '75' } });

    // Guardar cambios
    const btnGuardar = screen.getByText('💾 Guardar');
    fireEvent.click(btnGuardar);

    // Verificar llamada PUT (el componente incluye fecha del formulario)
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8001/transacciones/1', expect.objectContaining({
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: expect.stringContaining('"cantidad":75')
      }));
    });
  });

  // 🧪 TEST 7: Eliminar transacción
  test('permite eliminar transacción con confirmación', async () => {
    const mockTransaccion = {
      id: 1,
      tipo: 'gasto',
      cantidad: 50,
      descripcion: 'Para eliminar',
      fecha: '2025-10-15T10:00:00Z'
    };

    // Mock inicial
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [mockTransaccion]
    });

    // Mock DELETE
    fetch.mockResolvedValueOnce({ ok: true });

    // Mock GET después del DELETE
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => []
    });

    // Mock window.confirm
    const mockConfirm = jest.spyOn(window, 'confirm').mockReturnValue(true);

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('Para eliminar')).toBeInTheDocument();
    });

    // Hacer clic en eliminar
    const btnEliminar = screen.getByText('🗑️ Eliminar');
    fireEvent.click(btnEliminar);

    // Verificar que se muestra confirmación
    expect(mockConfirm).toHaveBeenCalledWith('¿Seguro que deseas eliminar esta transacción?');

    // Verificar llamada DELETE
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('http://localhost:8001/transacciones/1', expect.objectContaining({
        method: 'DELETE',
        headers: expect.any(Object),
      }));
    });

    mockConfirm.mockRestore();
  });

  // 🧪 TEST 8: Cambio de mes
  test('permite cambiar el mes de visualización', async () => {
    const mockSetMesGlobal = jest.fn();

    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    render(<TransaccionesWithRouter setMesGlobal={mockSetMesGlobal} />);

    await waitFor(() => {
      expect(screen.getByDisplayValue('Octubre')).toBeInTheDocument();
    });

    // Cambiar mes
    const selectMes = screen.getByDisplayValue('Octubre');
    fireEvent.change(selectMes, { target: { value: '12' } });

    expect(mockSetMesGlobal).toHaveBeenCalledWith(12);
  });

  // 🧪 TEST 9: Cancelar formularios
  test('permite cancelar formulario de nueva transacción', async () => {
    fetch.mockResolvedValue({
      ok: true,
      json: async () => []
    });

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText('➕ Añadir Primera Transacción')).toBeInTheDocument();
    });

    // Abrir formulario
    const btnAñadir = screen.getByText('➕ Añadir Primera Transacción');
    fireEvent.click(btnAñadir);

    // Verificar que aparece formulario y botón cancelar
    expect(screen.getByText('❌ Cancelar')).toBeInTheDocument();

    // Cancelar
    const btnCancelar = screen.getByText('❌ Cancelar');
    fireEvent.click(btnCancelar);

    // Verificar que desaparece formulario
    expect(screen.queryByText('❌ Cancelar')).not.toBeInTheDocument();
    expect(screen.getByText('➕ Añadir Primera Transacción')).toBeInTheDocument();
  });

  // 🧪 TEST 10: Manejo de errores
  test('maneja errores de red correctamente', async () => {
    fetch.mockRejectedValue(new Error('Network error'));
    
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
    });

    consoleSpy.mockRestore();
  });

  // 🧪 TEST 11: Orden por fecha descendente y luego id
  test('ordena transacciones por fecha descendente y desempata por id', async () => {
    const mockTransacciones = [
      { id: 10, tipo: 'gasto', cantidad: 20, descripcion: 'Z Gasto', fecha: '2025-10-10T10:00:00Z' },
      { id: 11, tipo: 'ingreso', cantidad: 40, descripcion: 'A Ingreso', fecha: '2025-10-11T10:00:00Z' },
      { id: 12, tipo: 'gasto', cantidad: 15, descripcion: 'B Gasto', fecha: '2025-10-11T09:00:00Z' }, // misma fecha día que id 11 (hora distinta)
      { id: 13, tipo: 'ingreso', cantidad: 100, descripcion: 'C Ingreso', fecha: '2025-10-09T08:00:00Z' }
    ];

    fetch.mockResolvedValue({
      ok: true,
      json: async () => mockTransacciones
    });

    const { container } = render(<TransaccionesWithRouter />);

    await waitFor(() => {
      expect(screen.getByText(/Lista de Transacciones \(1-4 de 4\)/)).toBeInTheDocument();
    });

    const descripcionElems = container.querySelectorAll('strong.transaction-description');
    const texts = Array.from(descripcionElems).map(e => e.textContent);
    // Esperado: fechas 11 (id 11 y 12, pero hora: 11 10:00 > 11 09:00, luego id), luego 10, luego 9
    expect(texts[0]).toBe('A Ingreso');
    expect(texts[1]).toBe('B Gasto');
    expect(texts[2]).toBe('Z Gasto');
    expect(texts[3]).toBe('C Ingreso');
  });
});
