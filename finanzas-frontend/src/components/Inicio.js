import React, { useState, useEffect } from "react";
import Graficos from "./Graficos";

const Inicio = ({ mesGlobal, setMesGlobal, añoGlobal }) => {
  const [sueldoActual, setSueldoActual] = useState(null);
  const [nuevoSueldo, setNuevoSueldo] = useState("");
  const [editando, setEditando] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saldoTotal, setSaldoTotal] = useState(null);

  const nombresMeses = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
  ];

  // Cargar saldo total del mes seleccionado
  useEffect(() => {
    const cargarSaldoTotal = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/saldo-total?mes=${mesGlobal}&anio=${añoGlobal}`);
        if (response.ok) {
          const data = await response.json();
          setSaldoTotal(data);
        } else {
          setSaldoTotal({ saldo_total: 0, saldo_transacciones: 0, saldo_sueldo: 0 });
        }
      } catch (error) {
        console.error("Error al cargar saldo total:", error);
        setSaldoTotal({ saldo_total: 0, saldo_transacciones: 0, saldo_sueldo: 0 });
      }
    };

    cargarSaldoTotal();
  }, [mesGlobal, añoGlobal]);

  // Cargar sueldo del mes seleccionado
  useEffect(() => {
    const cargarSueldoActual = async () => {
      setLoading(true);
      try {
        const response = await fetch(`http://127.0.0.1:8000/sueldos/${añoGlobal}/${mesGlobal}`);
        if (response.ok) {
          const sueldo = await response.json();
          setSueldoActual(sueldo);
          setNuevoSueldo(sueldo?.cantidad.toString() || "");
        } else {
          setSueldoActual(null);
          setNuevoSueldo("");
        }
      } catch (error) {
        console.error("Error al cargar sueldo:", error);
        setSueldoActual(null);
        setNuevoSueldo("");
      } finally {
        setLoading(false);
      }
    };

    cargarSueldoActual();
  }, [mesGlobal, añoGlobal]);

  // Guardar o actualizar sueldo
  const guardarSueldo = async () => {
    if (!nuevoSueldo || parseFloat(nuevoSueldo) <= 0) {
      alert("Por favor ingresa una cantidad válida");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/sueldos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cantidad: parseFloat(nuevoSueldo),
          mes: mesGlobal,
          anio: añoGlobal
        }),
      });

      if (response.ok) {
        const sueldo = await response.json();
        setSueldoActual(sueldo);
        setEditando(false);
        
        // Recargar saldo total
        const resSaldo = await fetch(`http://127.0.0.1:8000/saldo-total?mes=${mesGlobal}&anio=${añoGlobal}`);
        if (resSaldo.ok) {
          const dataSaldo = await resSaldo.json();
          setSaldoTotal(dataSaldo);
        }
      } else {
        alert("Error al guardar el sueldo");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Error al guardar el sueldo");
    }
  };

  const iniciarEdicion = () => {
    setEditando(true);
    setNuevoSueldo(sueldoActual?.cantidad.toString() || "");
  };

  const cancelarEdicion = () => {
    setEditando(false);
    setNuevoSueldo(sueldoActual?.cantidad.toString() || "");
  };

  if (loading) {
    return (
      <div className="container">
        <h1>Inicio</h1>
        <p>Cargando...</p>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h1>Dashboard</h1>
      
      {/* Saldo total - YA TIENES ESTO */}
      <div className="row mb-4">
        <div className="col-md-12">
          <div className="card">
            <div className="card-header bg-primary text-white d-flex justify-content-between align-items-center">
              <h4>Saldo de {nombresMeses[mesGlobal - 1]} {añoGlobal}</h4>
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
                  <h6 className="text-muted">Saldo Total</h6>
                  <h3 className={saldoTotal?.saldo_total >= 0 ? 'text-success' : 'text-danger'}>
                    {saldoTotal?.saldo_total || 0} €
                  </h3>
                </div>
                <div className="col-md-4">
                  <h6 className="text-muted">Sueldo</h6>
                  <h5 className="text-primary">{saldoTotal?.saldo_sueldo || 0} €</h5>
                </div>
                <div className="col-md-4">
                  <h6 className="text-muted">Transacciones</h6>
                  <h5 className={saldoTotal?.saldo_transacciones >= 0 ? 'text-success' : 'text-danger'}>
                    {saldoTotal?.saldo_transacciones >= 0 ? '+' : ''}{saldoTotal?.saldo_transacciones || 0} €
                  </h5>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Gestión de sueldo - YA TIENES ESTO */}
      <div className="row mb-4">
        <div className="col-md-8">
          <div className="card">
            <div className="card-header">
              <h5>Gestión de Sueldos - {nombresMeses[mesGlobal - 1]} {añoGlobal}</h5>
            </div>
            <div className="card-body">
              {!editando ? (
                <div>
                  {sueldoActual ? (
                    <div className="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 className="text-muted">Sueldo de {nombresMeses[mesGlobal - 1]}</h6>
                        <h4 className="text-success">{sueldoActual.cantidad} €</h4>
                        <small className="text-muted">
                          Registrado el {new Date(sueldoActual.fecha).toLocaleDateString()}
                        </small>
                      </div>
                      <button 
                        className="btn btn-outline-primary"
                        onClick={iniciarEdicion}
                      >
                        ✏️ Editar
                      </button>
                    </div>
                  ) : (
                    <div className="text-center">
                      <h6 className="text-muted">Sueldo de {nombresMeses[mesGlobal - 1]}</h6>
                      <p className="text-muted">No hay sueldo registrado para este mes</p>
                      <button 
                        className="btn btn-primary"
                        onClick={() => setEditando(true)}
                      >
                        ➕ Añadir Sueldo
                      </button>
                    </div>
                  )}
                </div>
              ) : (
                <div>
                  <div className="mb-3">
                    <label htmlFor="sueldo" className="form-label">
                      Cantidad del sueldo - {nombresMeses[mesGlobal - 1]} {añoGlobal}
                    </label>
                    <div className="input-group">
                      <input
                        id="sueldo"
                        type="number"
                        className="form-control"
                        value={nuevoSueldo}
                        onChange={(e) => setNuevoSueldo(e.target.value)}
                        placeholder="Ingresa tu sueldo"
                        step="0.01"
                        min="0"
                      />
                      <span className="input-group-text">€</span>
                    </div>
                  </div>
                  <div className="d-flex gap-2">
                    <button 
                      className="btn btn-success"
                      onClick={guardarSueldo}
                    >
                      💾 Guardar
                    </button>
                    <button 
                      className="btn btn-secondary"
                      onClick={cancelarEdicion}
                    >
                      ❌ Cancelar
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* NUEVA SECCIÓN: Gráficos integrados */}
      <div className="row mb-4">
        <div className="col-12">
          <Graficos 
            mesGlobal={mesGlobal}
            setMesGlobal={setMesGlobal}
            añoGlobal={añoGlobal}
            hideSelector={true} // ← Nueva prop para ocultar el selector
          />
        </div>
      </div>
    </div>
  );
};

export default Inicio;
