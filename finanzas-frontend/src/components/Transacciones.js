import React, { useState, useEffect } from "react";
import { authService } from "../services/authService";
import toast from 'react-hot-toast';

const Transacciones = ({ mesGlobal, añoGlobal, setMesGlobal }) => {
  const [transacciones, setTransacciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Estados para paginación
  const [paginaActual, setPaginaActual] = useState(1);
  const [transaccionesPorPagina] = useState(15);
  const [totalTransacciones, setTotalTransacciones] = useState(0);

  // Estados para añadir y editar
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [nuevaTransaccion, setNuevaTransaccion] = useState({
    tipo: "gasto",
    cantidad: 0,
    descripcion: "",
    fecha: `${añoGlobal}-${String(mesGlobal).padStart(2, '0')}-01` // Fecha inicial basada en el mes y año seleccionados
  });
  const [editando, setEditando] = useState(null);

  const nombresMeses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];

  // Obtener transacciones filtradas por mes con paginación
  useEffect(() => {
    const fetchTransacciones = async () => {
      try {
        setLoading(true);
        // Obtener transacciones del mes seleccionado
        const resAll = await authService.apiCall(`/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
        if (!resAll.ok) throw new Error("Error al obtener transacciones");
        const allData = await resAll.json();
        
  const ordenadas = [...allData].sort((a,b) => new Date(b.fecha) - new Date(a.fecha) || b.id - a.id);
  setTotalTransacciones(ordenadas.length);
  setTransacciones(ordenadas);
      } catch (err) {
        setError(err.message);
        toast.error("Error al cargar las transacciones");
      } finally {
        setLoading(false);
      }
    };
    fetchTransacciones();
  }, [mesGlobal, añoGlobal]); // Recargar cuando cambien mes/año

  // Resetear página al cambiar mes
  useEffect(() => {
    setPaginaActual(1);
  }, [mesGlobal, añoGlobal]);

  // Actualizar el estado de nuevaTransaccion al cambiar el mes o año global
  useEffect(() => {
    setNuevaTransaccion((prev) => ({
      ...prev,
      fecha: `${añoGlobal}-${String(mesGlobal).padStart(2, '0')}-01`
    }));
  }, [mesGlobal, añoGlobal]);

  // Crear nueva transacción
  const guardarTransaccion = async () => {
    if (!nuevaTransaccion.cantidad || Number(nuevaTransaccion.cantidad) <= 0) {
      toast.error('Introduce una cantidad válida para la transacción');
      return;
    }
    if (!nuevaTransaccion.descripcion || nuevaTransaccion.descripcion.trim().length === 0) {
      toast.error('Introduce una descripción para la transacción');
      return;
    }
    try {
      const transaccionData = {
        tipo: nuevaTransaccion.tipo,
        cantidad: nuevaTransaccion.cantidad,
        descripcion: nuevaTransaccion.descripcion,
      };

      // Solo añadir fecha si se especificó
      if (nuevaTransaccion.fecha) {
        transaccionData.fecha = nuevaTransaccion.fecha;  // Enviar fecha en formato YYYY-MM-DD
      }

      const res = await authService.apiCall(`/transacciones`, {
        method: "POST",
        body: JSON.stringify(transaccionData),
      });
      if (!res.ok) throw new Error("Error al guardar transacción");
      
      // Determinar mes/año de la nueva fecha si se cambió
      if (transaccionData.fecha) {
        const [newYear, newMonth] = transaccionData.fecha.split('-').map(Number);
        // Si la fecha nueva es de otro mes, cambiamos el mesGlobal para que el usuario vea la transacción movida
        if (newYear === añoGlobal && newMonth !== mesGlobal) {
          setMesGlobal(newMonth);
        }
      }
      // Recargar transacciones del mes (puede que hayamos cambiado mesGlobal arriba)
      const resTransacciones = await authService.apiCall(`/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
      let data = await resTransacciones.json();
      // Ordenar descendente por fecha luego id
      data = [...data].sort((a,b) => new Date(b.fecha) - new Date(a.fecha) || b.id - a.id);
      setTransacciones(data);
      setTotalTransacciones(data.length);
      // Colocar en primera página tras crear
      setPaginaActual(1);
      
      // Si la nueva transacción hace que sea necesario ir a la última página
      const totalPaginas = Math.ceil(data.length / transaccionesPorPagina);
      if (paginaActual > totalPaginas && totalPaginas > 0) {
        setPaginaActual(totalPaginas);
      }
      
      toast.success("Transacción guardada correctamente");
      setMostrarFormulario(false);
      setNuevaTransaccion({ tipo: "gasto", cantidad: 0, descripcion: "", fecha: "" });
    } catch (err) {
      toast.error("Error al guardar la transacción");
    }
  };

  // Eliminar transacción
  const eliminarTransaccion = async (id) => {
    try {
      await authService.apiCall(`/transacciones/${id}`, {
        method: "DELETE",
      });
        // Recargar transacciones del mes seleccionado
        const res = await authService.apiCall(`/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
  let data = await res.json();
  data = [...data].sort((a,b) => new Date(b.fecha) - new Date(a.fecha) || b.id - a.id);
  setTransacciones(data);
  setTotalTransacciones(data.length);
      
      // Si después de eliminar nos quedamos sin transacciones en la página actual, volver a la anterior
      const totalPaginas = Math.ceil(data.length / transaccionesPorPagina);
      if (paginaActual > totalPaginas && totalPaginas > 0) {
        setPaginaActual(totalPaginas);
      }
      
      toast.success("Transacción eliminada correctamente");
    } catch (err) {
      toast.error("Error al eliminar la transacción");
    }
  };

  // Preparar edición
  const editarTransaccion = (transaccion) => {
    setEditando(transaccion.id);
    setNuevaTransaccion({
      tipo: transaccion.tipo,
      cantidad: transaccion.cantidad,
      descripcion: transaccion.descripcion || "",
      // Evitar usar toISOString (convierte a UTC y puede retroceder un día cambiando el mes)
      // Si backend ya envía 'YYYY-MM-DD' o 'YYYY-MM-DDTHH:MM:SS', extraemos la parte de fecha.
      fecha: (typeof transaccion.fecha === 'string'
        ? transaccion.fecha.split('T')[0]
        : new Date(transaccion.fecha).toLocaleDateString('en-CA')) // en-CA => YYYY-MM-DD
    });
  };

  // Actualizar transacción
  const actualizarTransaccion = async () => {
    // Validación cliente: cantidad requerida y mayor que 0
    if (!nuevaTransaccion.cantidad || Number(nuevaTransaccion.cantidad) <= 0) {
      toast.error('Introduce una cantidad válida para la transacción');
      return;
    }
    // Validación cliente: descripción requerida
    if (!nuevaTransaccion.descripcion || nuevaTransaccion.descripcion.trim().length === 0) {
      toast.error('Introduce una descripción para la transacción');
      return;
    }
    try {
      const transaccionData = {
        tipo: nuevaTransaccion.tipo,
        cantidad: nuevaTransaccion.cantidad,
        descripcion: nuevaTransaccion.descripcion,
      };

      // Solo añadir fecha si se especificó
      if (nuevaTransaccion.fecha) {
        transaccionData.fecha = nuevaTransaccion.fecha;  // Enviar fecha en formato YYYY-MM-DD
      }

      const res = await authService.apiCall(
        `/transacciones/${editando}`,
        {
          method: "PUT",
          body: JSON.stringify(transaccionData), // ← Usando transaccionData con fecha procesada
        }
      );
      if (!res.ok) throw new Error("Error al actualizar transacción");
      
    // Recargar transacciones del mes seleccionado
    const resTransacciones = await authService.apiCall(`/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
  let data = await resTransacciones.json();
  data = [...data].sort((a,b) => new Date(b.fecha) - new Date(a.fecha) || b.id - a.id);
  setTransacciones(data);
  setTotalTransacciones(data.length);
      
      toast.success('Transacción actualizada correctamente');
      setEditando(null);
      setNuevaTransaccion({ tipo: "gasto", cantidad: 0, descripcion: "", fecha: "" });
    } catch (err) {
      toast.error("Error al actualizar la transacción");
    }
  };

  // Funciones de paginación
  const indiceUltimaTransaccion = paginaActual * transaccionesPorPagina;
  const indicePrimeraTransaccion = indiceUltimaTransaccion - transaccionesPorPagina;
  const transaccionesActuales = transacciones.slice(indicePrimeraTransaccion, indiceUltimaTransaccion);
  const totalPaginas = Math.ceil(totalTransacciones / transaccionesPorPagina);

  const cambiarPagina = (numeroPagina) => {
    setPaginaActual(numeroPagina);
  };

  const paginaAnterior = () => {
    if (paginaActual > 1) {
      setPaginaActual(paginaActual - 1);
    }
  };

  const paginaSiguiente = () => {
    if (paginaActual < totalPaginas) {
      setPaginaActual(paginaActual + 1);
    }
  };

  // Generar números de página para mostrar
  const generarNumerosPagina = () => {
    const numeros = [];
    const rango = 2; // Mostrar 2 páginas a cada lado de la actual
    
    let inicio = Math.max(1, paginaActual - rango);
    let fin = Math.min(totalPaginas, paginaActual + rango);
    
    // Ajustar si estamos cerca del inicio o fin
    if (paginaActual <= rango) {
      fin = Math.min(totalPaginas, 2 * rango + 1);
    }
    if (paginaActual >= totalPaginas - rango) {
      inicio = Math.max(1, totalPaginas - 2 * rango);
    }
    
    for (let i = inicio; i <= fin; i++) {
      numeros.push(i);
    }
    return numeros;
  };

  if (loading) return <p>Cargando transacciones...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="container mt-4 mb-5">
      <div className="card mb-4">
        <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
          <h3 className="mb-0">💰 Transacciones de {nombresMeses[mesGlobal - 1]} {añoGlobal}</h3>
          <select 
            className="form-select w-auto text-dark"
            value={mesGlobal}
            onChange={(e) => setMesGlobal(parseInt(e.target.value))}
          >
            {nombresMeses.map((nombre, index) => (
              <option key={index + 1} value={index + 1}>
                {nombre}
              </option>
            ))}
          </select>
        </div>
        <div className="card-body">
          <div className="row text-center">
            <div className="col-md-4">
              <div className="p-3 bg-success-subtle rounded">
                <h6 className="text-muted mb-1">Ingresos</h6>
                <h4 className="text-success mb-0">
                  {transacciones.filter(t => t.tipo === 'ingreso').reduce((sum, t) => sum + t.cantidad, 0)} €
                </h4>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 bg-danger-subtle rounded">
                <h6 className="text-muted mb-1">Gastos</h6>
                <h4 className="text-danger mb-0">
                  {transacciones.filter(t => t.tipo === 'gasto').reduce((sum, t) => sum + t.cantidad, 0)} €
                </h4>
              </div>
            </div>
            <div className="col-md-4">
              <div className="p-3 bg-primary-subtle rounded">
                <h6 className="text-muted mb-1">Balance</h6>
                <h4 className={
                  (transacciones.filter(t => t.tipo === 'ingreso').reduce((sum, t) => sum + t.cantidad, 0) - 
                   transacciones.filter(t => t.tipo === 'gasto').reduce((sum, t) => sum + t.cantidad, 0)) >= 0 
                   ? 'text-success' : 'text-danger'
                }>
                  {transacciones.filter(t => t.tipo === 'ingreso').reduce((sum, t) => sum + t.cantidad, 0) - 
                   transacciones.filter(t => t.tipo === 'gasto').reduce((sum, t) => sum + t.cantidad, 0)} €
                </h4>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Lista de transacciones */}
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <h5 className="mb-0">
            Lista de Transacciones ({totalTransacciones > 0 ? `${(paginaActual - 1) * transaccionesPorPagina + 1}-${Math.min(paginaActual * transaccionesPorPagina, totalTransacciones)} de ${totalTransacciones}` : '0'})
          </h5>
          {!mostrarFormulario && !editando && ( // ← Añadido !editando para evitar conflictos
            <button 
              className="btn btn-success"
              onClick={() => setMostrarFormulario(true)}
            >
              ➕ Nueva Transacción
            </button>
          )}
        </div>
        <div className="card-body p-0">
          {totalTransacciones === 0 && !mostrarFormulario ? ( // ← Cambiado a totalTransacciones
            <div className="text-center p-5">
              <div className="mb-3">
                <i className="fas fa-receipt fa-3x text-muted"></i>
              </div>
                <h5 className="text-muted">No hay transacciones este mes</h5>
              <p className="text-muted">¡Añade tu primera transacción para empezar!</p>
              <button 
                className="btn btn-primary"
                onClick={() => setMostrarFormulario(true)}
              >
                ➕ Añadir Primera Transacción
              </button>
            </div>
          ) : (
            <div className="list-group list-group-flush">
              {/* Formulario inline para nueva transacción */}
              {mostrarFormulario && (
                <div className="list-group-item bg-light">
                  <div className="row align-items-center">
                    <div className="col-sm-2">
                      <select
                        className="form-select"
                        value={nuevaTransaccion.tipo}
                        onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, tipo: e.target.value})}
                      >
                        <option value="gasto">🔴 Gasto</option>
                        <option value="ingreso">🟢 Ingreso</option>
                      </select>
                    </div>
                    <div className="col-md-3">
                      <input
                        type="text"
                        className="form-control"
                        placeholder="Descripción..."
                        value={nuevaTransaccion.descripcion}
                        onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, descripcion: e.target.value})}
                      />
                    </div>
                    <div className="col-md-2">
                      <input
                        type="date"
                        className="form-control"
                        value={nuevaTransaccion.fecha}
                        onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, fecha: e.target.value})}
                        placeholder="Fecha opcional"
                      />
                    </div>
                    <div className="col-md-2">
                      <div className="input-group">
                        <input
                          type="number"
                          className="form-control"
                          placeholder="0.00"
                          step="0.01"
                          min="0"
                          value={nuevaTransaccion.cantidad}
                          onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, cantidad: parseFloat(e.target.value) || 0})}
                        />
                        <span className="input-group-text">€</span>
                      </div>
                    </div>
                    <div className="col-md-3">
                      <div className="d-flex gap-2">
                        <button className="btn btn-success btn-sm" onClick={guardarTransaccion}>
                          💾 Guardar
                        </button>
                        <button 
                          className="btn btn-secondary btn-sm" 
                          onClick={() => {
                            setMostrarFormulario(false);
                            setNuevaTransaccion({ tipo: "gasto", cantidad: 0, descripcion: "", fecha: "" });
                          }}
                        >
                          ❌ Cancelar
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Editar transacciones existentes */}
              {transaccionesActuales.map((t) => (
                <div key={t.id} className="list-group-item">
                  {editando === t.id ? (
                    // Modo edición
                    <div className="row align-items-center">
                      <div className="col-md-2">
                        <select
                          className="form-select"
                          value={nuevaTransaccion.tipo}
                          onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, tipo: e.target.value})}
                        >
                          <option value="gasto">🔴 Gasto</option>
                          <option value="ingreso">🟢 Ingreso</option>
                        </select>
                      </div>
                      <div className="col-md-3">
                        <input
                          type="text"
                          className="form-control"
                          value={nuevaTransaccion.descripcion}
                          onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, descripcion: e.target.value})}
                        />
                      </div>
                      <div className="col-md-2">
                        <input
                          type="date"
                          className="form-control"
                          value={nuevaTransaccion.fecha}
                          onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, fecha: e.target.value})}
                        />
                      </div>
                      <div className="col-md-2">
                        <div className="input-group">
                          <input
                            type="number"
                            className="form-control"
                            step="0.01"
                            min="0"
                            value={nuevaTransaccion.cantidad}
                            onChange={(e) => setNuevaTransaccion({...nuevaTransaccion, cantidad: parseFloat(e.target.value) || 0})}
                          />
                          <span className="input-group-text">€</span>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <div className="d-flex gap-2">
                          <button className="btn btn-success btn-sm" onClick={actualizarTransaccion}>
                            💾 Guardar
                          </button>
                          <button 
                            className="btn btn-secondary btn-sm" 
                            onClick={() => {
                              setEditando(null);
                              setNuevaTransaccion({ tipo: "gasto", cantidad: 0, descripcion: "", fecha: "" });
                            }}
                          >
                            ❌ Cancelar
                          </button>
                        </div>
                      </div>
                    </div>
                  ) : (
                    // Modo visualización
                    <div className="row align-items-center">
                      <div className="col-md-2">
                        <span className={`badge ${t.tipo === 'ingreso' ? 'bg-success' : 'bg-danger'} fs-6`}>
                          {t.tipo === 'ingreso' ? '🟢 Ingreso' : '🔴 Gasto'}
                        </span>
                      </div>
                      <div className="col-md-4">
                        <div>
                          <strong className="transaction-description">{t.descripcion || 'Sin descripción'}</strong>
                          <div className="transaction-date text-muted small">
                            {new Date(t.fecha).toLocaleDateString('es-ES', {
                              day: 'numeric',
                              month: 'short',
                              year: 'numeric'
                            })}
                          </div>
                        </div>
                      </div>
                      <div className="col-md-3">
                        <h5 className={`mb-0 ${t.tipo === 'ingreso' ? 'text-success' : 'text-danger'}`}>
                          {t.tipo === 'ingreso' ? '+' : '-'}{t.cantidad} €
                        </h5>
                      </div>
                      <div className="col-md-3">
                        <div className="d-flex gap-2">
                          <button 
                            className="btn btn-outline-primary btn-sm transaction-btn"
                            onClick={() => editarTransaccion(t)}
                            disabled={mostrarFormulario} // ← Evitar conflictos
                          >
                            ✏️ Editar
                          </button>
                          <button 
                            className="btn btn-outline-danger btn-sm transaction-btn"
                            onClick={() => {
                              if (window.confirm('¿Seguro que deseas eliminar esta transacción?')) {
                                eliminarTransaccion(t.id);
                              }
                            }}
                            disabled={mostrarFormulario} // ← Evitar conflictos
                          >
                            🗑️ Eliminar
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
          
          {/* Controles de paginación */}
          {totalTransacciones > transaccionesPorPagina && (
            <div className="p-3 border-top">
              <nav aria-label="Paginación de transacciones">
                <ul className="pagination justify-content-center mb-0">
                  {/* Botón anterior */}
                  <li className={`page-item ${paginaActual === 1 ? 'disabled' : ''}`}>
                    <button 
                      className="page-link" 
                      onClick={paginaAnterior}
                      disabled={paginaActual === 1}
                    >
                      Anterior
                    </button>
                  </li>
                  
                  {/* Números de página */}
                  {generarNumerosPagina().map(numero => (
                    <li key={numero} className={`page-item ${paginaActual === numero ? 'active' : ''}`}>
                      <button 
                        className="page-link" 
                        onClick={() => cambiarPagina(numero)}
                      >
                        {numero}
                      </button>
                    </li>
                  ))}
                  
                  {/* Botón siguiente */}
                  <li className={`page-item ${paginaActual === Math.ceil(totalTransacciones / transaccionesPorPagina) ? 'disabled' : ''}`}>
                    <button 
                      className="page-link" 
                      onClick={paginaSiguiente}
                      disabled={paginaActual === Math.ceil(totalTransacciones / transaccionesPorPagina)}
                    >
                      Siguiente
                    </button>
                  </li>
                </ul>
              </nav>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Transacciones;