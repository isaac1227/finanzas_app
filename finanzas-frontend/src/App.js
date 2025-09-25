import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Inicio from "./components/Inicio";
import Navbar from "./components/Navbar";
import Transacciones from "./components/Transacciones";
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';

function App() {
  const fechaActual = new Date();
  const mesActual = fechaActual.getMonth() + 1;
  const añoActual = fechaActual.getFullYear();
  const [mesGlobal, setMesGlobal] = useState(mesActual);
  const [añoGlobal, setAñoGlobal] = useState(añoActual);

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={
          <Inicio 
            mesGlobal={mesGlobal} 
            setMesGlobal={setMesGlobal} 
            añoGlobal={añoGlobal} 
          />
        } />
        <Route path="/transacciones" element={
          <Transacciones 
            mesGlobal={mesGlobal} 
            setMesGlobal={setMesGlobal} 
            añoGlobal={añoGlobal} 
          />
        } />
        {/* Eliminar la ruta de gráficos */}
        <Route path="*" element={<h2>Página no encontrada</h2>} />
      </Routes>
    </Router>
  );
}

export default App;