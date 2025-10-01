import { React, useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const Graficos = ({ mesGlobal, añoGlobal, setMesGlobal, hideSelector = false }) => {
    const [totalGastos, setTotalGastos] = useState(0);
    const [totalIngresos, setTotalIngresos] = useState(0);
    const [loading, setLoading] = useState(true);

    const nombresMeses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ];

    useEffect(() => {
        const cargarDatos = async () => {
            setLoading(true);
            try {
                const response = await fetch(`http://127.0.0.1:8001/transacciones?mes=${mesGlobal}&anio=${añoGlobal}`);
                if (response.ok) {
                    const data = await response.json();

                    let gastos = 0;
                    let ingresos = 0;

                    for (const d of data) {
                        if (d.tipo === 'gasto') {
                            gastos += d.cantidad;
                        } else if (d.tipo === 'ingreso') {
                            ingresos += d.cantidad;
                        }
                    }

                    setTotalGastos(gastos);
                    setTotalIngresos(ingresos);
                } else {
                    setTotalGastos(0);
                    setTotalIngresos(0);
                }
            } catch (error) {
                console.error("Error al cargar datos:", error);
                setTotalGastos(0);
                setTotalIngresos(0);
            } finally {
                setLoading(false);
            }
        };

        cargarDatos();
    }, [mesGlobal, añoGlobal]);

    const dataGrafico = {
        labels: ['💸 Gastos', '💰 Ingresos'],
        datasets: [
            {
                label: 'Cantidad (€)',
                data: [totalGastos, totalIngresos],
                backgroundColor: [
                    'rgba(220, 53, 69, 0.8)',   // Rojo moderno para gastos
                    'rgba(25, 135, 84, 0.8)'    // Verde moderno para ingresos
                ],
                borderColor: [
                    'rgba(220, 53, 69, 1)',
                    'rgba(25, 135, 84, 1)'
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false,
            },
        ],
    };

    const opcionesGrafico = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    padding: 20,
                    usePointStyle: true,
                    pointStyle: 'circle'
                }
            },
            title: {
                display: true,
                text: `📊 Balance Financiero - ${nombresMeses[mesGlobal - 1]} ${añoGlobal}`,
                font: {
                    size: 18,
                    weight: 'bold'
                },
                padding: {
                    top: 10,
                    bottom: 30
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: 'white',
                bodyColor: 'white',
                borderColor: 'rgba(255, 255, 255, 0.1)',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        return `${context.parsed.y.toFixed(2)} €`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)',
                    lineWidth: 1
                },
                ticks: {
                    font: {
                        size: 12
                    },
                    callback: function(value) {
                        return value.toFixed(0) + '€';
                    }
                },
                title: {
                    display: true,
                    text: 'Cantidad (€)',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        },
        animation: {
            duration: 1000,
            easing: 'easeInOutQuart'
        }
    };

    const balance = totalIngresos - totalGastos;

    if (loading) {
        return (
            <div className="container mt-4">
                <div className="text-center">
                    <div className="spinner-border text-primary" role="status" style={{width: '3rem', height: '3rem'}}>
                        <span className="visually-hidden">Cargando...</span>
                    </div>
                    <p className="mt-3 h5">Cargando gráfico...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="container-fluid mt-4">
            <div className="row">
                <div className="col-12">
                    <div className="card shadow-lg border-0">
                        <div className="card-header bg-gradient bg-primary text-white d-flex justify-content-between align-items-center py-3">
                            <h3 className="mb-0">📊 Análisis Financiero</h3>
                            {/* Mostrar selector solo si hideSelector es false */}
                            {!hideSelector && (
                                <select 
                                    className="form-select w-auto text-dark fw-bold"
                                    value={mesGlobal}
                                    onChange={(e) => setMesGlobal(parseInt(e.target.value))}
                                    style={{minWidth: '120px'}}
                                >
                                    {nombresMeses.map((nombre, index) => (
                                        <option key={index + 1} value={index + 1}>
                                            {nombre}
                                        </option>
                                    ))}
                                </select>
                            )}
                        </div>
                        
                        <div className="card-body p-4">
                            {/* Dashboard de resumen */}
                            <div className="row mb-4">
                                <div className="col-lg-3 col-md-6 mb-3">
                                    <div className="card bg-danger-subtle border-danger border-start border-4 h-100">
                                        <div className="card-body text-center">
                                            <div className="text-danger mb-2">
                                                <i className="fas fa-arrow-down fa-2x"></i>
                                            </div>
                                            <h6 className="text-muted text-uppercase mb-1">Gastos Totales</h6>
                                            <h3 className="text-danger fw-bold mb-0">{totalGastos.toFixed(2)} €</h3>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="col-lg-3 col-md-6 mb-3">
                                    <div className="card bg-success-subtle border-success border-start border-4 h-100">
                                        <div className="card-body text-center">
                                            <div className="text-success mb-2">
                                                <i className="fas fa-arrow-up fa-2x"></i>
                                            </div>
                                            <h6 className="text-muted text-uppercase mb-1">Ingresos Totales</h6>
                                            <h3 className="text-success fw-bold mb-0">{totalIngresos.toFixed(2)} €</h3>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="col-lg-3 col-md-6 mb-3">
                                    <div className={`card ${balance >= 0 ? 'bg-success-subtle border-success' : 'bg-danger-subtle border-danger'} border-start border-4 h-100`}>
                                        <div className="card-body text-center">
                                            <div className={balance >= 0 ? 'text-success' : 'text-danger'}>
                                                <i className={`fas ${balance >= 0 ? 'fa-trending-up' : 'fa-trending-down'} fa-2x mb-2`}></i>
                                            </div>
                                            <h6 className="text-muted text-uppercase mb-1">Balance</h6>
                                            <h3 className={`fw-bold mb-0 ${balance >= 0 ? 'text-success' : 'text-danger'}`}>
                                                {balance >= 0 ? '+' : ''}{balance.toFixed(2)} €
                                            </h3>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="col-lg-3 col-md-6 mb-3">
                                    <div className="card bg-info-subtle border-info border-start border-4 h-100">
                                        <div className="card-body text-center">
                                            <div className="text-info mb-2">
                                                <i className="fas fa-percentage fa-2x"></i>
                                            </div>
                                            <h6 className="text-muted text-uppercase mb-1">Tasa Ahorro</h6>
                                            <h3 className="text-info fw-bold mb-0">
                                                {totalIngresos > 0 ? ((balance / totalIngresos) * 100).toFixed(1) : 0}%
                                            </h3>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* Gráfico principal */}
                            <div className="row">
                                <div className="col-12">
                                    <div className="card border-0 bg-light">
                                        <div className="card-body p-3">
                                            {totalGastos === 0 && totalIngresos === 0 ? (
                                                <div className="text-center py-5">
                                                    <div className="mb-4">
                                                        <i className="fas fa-chart-bar fa-4x text-muted"></i>
                                                    </div>
                                                    <h4 className="text-muted">No hay datos para mostrar</h4>
                                                    <p className="text-muted lead">
                                                        No hay transacciones registradas en {nombresMeses[mesGlobal - 1]} {añoGlobal}
                                                    </p>
                                                    <div className="mt-4">
                                                        <span className="badge bg-primary fs-6 px-3 py-2">
                                                            ¡Añade tu primera transacción para ver el análisis!
                                                        </span>
                                                    </div>
                                                </div>
                                            ) : (
                                                <div style={{ height: '400px', position: 'relative' }}>
                                                    <Bar data={dataGrafico} options={opcionesGrafico} />
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Graficos;