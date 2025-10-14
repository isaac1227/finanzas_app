import React, { createContext, useContext, useState, useEffect } from 'react';

// Crear contexto del tema
const ThemeContext = createContext();

// Provider del tema
export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  // Cargar tema guardado del localStorage al iniciar
  useEffect(() => {
    const savedTheme = localStorage.getItem('finanzas-theme');
    if (savedTheme) {
      setTheme(savedTheme);
    } else {
      // Detectar preferencia del sistema
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setTheme(prefersDark ? 'dark' : 'light');
    }
  }, []);

  // Aplicar tema al documento cuando cambie
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('finanzas-theme', theme);
  }, [theme]);

  // Función para alternar tema
  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  const value = {
    theme,
    toggleTheme,
    isDark: theme === 'dark'
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

// Hook personalizado para usar el tema
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme debe ser usado dentro de un ThemeProvider');
  }
  return context;
};