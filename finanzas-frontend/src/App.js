import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Inicio from "./components/Inicio";
import Navbar from "./components/Navbar";
import Transacciones from "./components/Transacciones";
import Login from "./components/Login";
import { authService } from "./services/authService";
import { ThemeProvider } from "./contexts/ThemeContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/theme.css';
import React, { useState, useEffect } from 'react';
import { Toaster } from 'react-hot-toast';

function App() {
  const fechaActual = new Date();
  const mesActual = fechaActual.getMonth() + 1;
  const añoActual = fechaActual.getFullYear();
  const [mesGlobal, setMesGlobal] = useState(mesActual);
  const [añoGlobal] = useState(añoActual);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(authService.isLoggedIn());
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    authService.logout();
    setIsLoggedIn(false);
  };

  if (!isLoggedIn) {
    return (
      <ThemeProvider>
        <Toaster position="top-right" />
        <Login onLoginSuccess={handleLoginSuccess} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider>
      <Router>
        <Navbar onLogout={handleLogout} />
        <Toaster position="top-right" />
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
    </ThemeProvider>
  );
}

export default App;