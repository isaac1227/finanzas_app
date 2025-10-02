-- 🗄️ Script de inicialización para PostgreSQL en Docker
-- Este script se ejecuta automáticamente cuando se crea el contenedor

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Verificar que las tablas se crean correctamente
-- (Las tablas se crean automáticamente por SQLAlchemy/Alembic)

-- Crear tabla sueldos
CREATE TABLE IF NOT EXISTS sueldos (
    id SERIAL PRIMARY KEY,
    cantidad NUMERIC NOT NULL,
    mes INT NOT NULL,
    anio INT NOT NULL,
    fecha TIMESTAMP DEFAULT NOW() NOT NULL,
    CONSTRAINT uq_mes_anio UNIQUE (mes, anio)
);

-- Crear tabla transacciones
CREATE TABLE IF NOT EXISTS transacciones (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    cantidad NUMERIC NOT NULL,
    descripcion TEXT,
    fecha TIMESTAMP NOT NULL
);

-- Insertar datos iniciales
/*INSERT INTO sueldos (cantidad, mes, anio) VALUES 
(2500.00, 10, 2025),
(2500.00, 9, 2025),
(2400.00, 8, 2025);

INSERT INTO transacciones (tipo, cantidad, descripcion, fecha) VALUES 
('ingreso', 100.00, 'Freelance proyecto web', '2025-10-01 10:00:00'),
('gasto', 45.50, 'Supermercado semanal', '2025-10-01 18:30:00'),
('gasto', 12.75, 'Café y merienda', '2025-10-02 15:45:00'),
('ingreso', 50.00, 'Venta producto usado', '2025-10-03 12:00:00');*/

-- Crear índices para optimización
CREATE INDEX IF NOT EXISTS idx_transacciones_fecha ON transacciones(fecha);
CREATE INDEX IF NOT EXISTS idx_transacciones_tipo ON transacciones(tipo);
CREATE INDEX IF NOT EXISTS idx_sueldos_mes_anio ON sueldos(mes, anio);