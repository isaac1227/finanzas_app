import React, { useState, useEffect } from "react";
import { authService } from "../services/authService";
import toast from 'react-hot-toast';

const Transacciones = ({ mesGlobal, añoGlobal, setMesGlobal }) => {
  const [transacciones, setTransacciones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  // Obtener transacciones filtradas por mes
  useEffect(() => {
    const fetchTransacciones = async () => {
      try {
        setLoading(true);
        const res = await authService.apiCall(`/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
        if (!res.ok) throw new Error("Error al obtener transacciones");
        const data = await res.json();
        setTransacciones(data);
      } catch (err) {
        setError(err.message);
        toast.error("Error al cargar las transacciones");
      } finally {
        setLoading(false);
      }
    };
    fetchTransacciones();
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

      const res = await authService.apiCall(`/transacciones`, {
        method: "POST",
        body: JSON.stringify(transaccionData),
      });
      if (!res.ok) throw new Error("Error al guardar transacción");
      
      // Recargar transacciones del mes seleccionado
      const resTransacciones = await authService.apiCall(`/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
      const data = await resTransacciones.json();
      setTransacciones(data);
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
      const data = await res.json();
      setTransacciones(data);
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
      fecha: new Date(transaccion.fecha).toISOString().slice(0, 10) // ← Formato YYYY-MM-DD para input date
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
      const data = await resTransacciones.json();
      setTransacciones(data);
  toast.success('Transacción actualizada correctamente');
  setEditando(null);
  setNuevaTransaccion({ tipo: "gasto", cantidad: 0, descripcion: "", fecha: "" });
    } catch (err) {
      toast.error("Error al actualizar la transacción");
    }
  };

  if (loading) return <p>Cargando transacciones...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="container mt-4">
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
          <h5 className="mb-0">Lista de Transacciones ({transacciones.length})</h5>
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
          {transacciones.length === 0 && !mostrarFormulario ? ( // ← Añadido !mostrarFormulario
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
              {transacciones.map((t) => (
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
                          <strong>{t.descripcion || 'Sin descripción'}</strong>
                          <div className="text-muted small">
                            {new Date(t.fecha).toLocaleDateString('es-ES', {
                              day: 'numeric',
                              month: 'short',
                              hour: '2-digit',
                              minute: '2-digit'
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
                            className="btn btn-outline-primary btn-sm"
                            onClick={() => editarTransaccion(t)}
                            disabled={mostrarFormulario} // ← Evitar conflictos
                          >
                            ✏️ Editar
                          </button>
                          <button 
                            className="btn btn-outline-danger btn-sm"
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
        </div>
      </div>
    </div>
  );
};

export default Transacciones;
