# 💰 Finanzas App - Gestión Personal de Finanzas

Un proyecto personal desarrollado para **practicar y demostrar competencias** en desarrollo full-stack moderno con **FastAPI**, **React** y **PostgreSQL**.

## 🎯 Objetivo del Proyecto

Este proyecto fue creado como **ejercicio de aprendizaje** para practicar:
- Desarrollo de APIs REST con FastAPI
- Frontend moderno con React y Bootstrap
- Gestión de bases de datos con PostgreSQL y SQLAlchemy
- Arquitectura full-stack completa
- Documentación profesional de proyectos

## 🛠️ Stack Tecnológico

### **Backend**
- **FastAPI** - Framework web moderno y rápido para Python
- **SQLAlchemy** - ORM para manejo de base de datos
- **Pydantic** - Validación de datos y serialización
- **PostgreSQL** - Base de datos relacional
- **Python 3.11+** - Lenguaje de programación

### **Frontend**
- **React 18** - Biblioteca para interfaces de usuario
- **Bootstrap 5** - Framework CSS para diseño responsivo
- **JavaScript ES6+** - Lenguaje de programación frontend

### **Desarrollo**
- **Git** - Control de versiones
- **uvicorn** - Servidor ASGI para desarrollo
- **npm** - Gestión de dependencias frontend

## ✨ Funcionalidades

### **🏠 Análisis Financiero (Inicio)**
- Visualización del saldo mensual (no acumulativo)
- Desglose por: Saldo Total, Sueldos, Transacciones
- Selector de mes maestro que sincroniza toda la aplicación
- Gestión de sueldos (un sueldo por mes)
- **Gráficos integrados** con Chart.js mostrando análisis visual

### **📊 Análisis Visual con Gráficos**
- **Gráfico de barras profesional** (Gastos vs Ingresos)
- **Panel de métricas** con 4 indicadores clave:
  - 💸 Total de Gastos del mes
  - 💰 Total de Ingresos del mes  
  - 📈 Balance mensual (positivo/negativo)
  - 📊 Tasa de Ahorro porcentual
- **Animaciones suaves** y tooltips informativos
- **Estados responsivos** (carga, vacío, error)

### **💸 Gestión de Transacciones**
- Crear, editar y eliminar transacciones (ingresos/gastos)
- Filtrado por mes y año
- Interfaz moderna con cards (no tablas tradicionales)
- Confirmación antes de eliminar
- Resumen automático del mes (ingresos vs gastos)

### **💰 Gestión de Sueldos**
- Un sueldo por mes (restricción de negocio)
- Crear o actualizar sueldo mensual
- Visualización histórica por meses

## 🏗️ Arquitectura del Proyecto

```
finanzas-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Endpoints de la API
│   │   ├── models.py        # Modelos de SQLAlchemy
│   │   ├── schemas.py       # Esquemas de Pydantic
│   │   ├── crud.py          # Operaciones de base de datos
│   │   └── database.py      # Configuración de BD
│   └── requirements.txt
├── finanzas-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Inicio.js         # Análisis Financiero principal con gráficos
│   │   │   ├── Transacciones.js  # Gestión de transacciones
│   │   │   ├── Graficos.js       # Componente de visualización
│   │   │   └── Navbar.js         # Navegación
│   │   ├── App.js           # Estado compartido y rutas
│   │   └── index.js
│   └── package.json
├── README.md
├── SETUP.md
└── PORTFOLIO.md
```

## 🚀 Instalación y Configuración

### **🐳 Opción 1: Con Docker (RECOMENDADO)**

#### **Prerrequisitos**
```bash
# Solo necesitas Docker y Docker Compose
docker --version     # >= 20.0
docker-compose --version  # >= 2.0
```

#### **Instalación rápida con Docker**
```bash
# 1. Clonar repositorio
git clone https://github.com/isaac1227/finanzas_app.git
cd finanzas_app

# 2. Ejecutar toda la aplicación
docker-compose up -d

# 3. ¡Listo! Acceder a:
# - Frontend: http://localhost:3001
# - Backend API: http://localhost:8001  
# - Docs API: http://localhost:8001/docs
# - Adminer DB: http://localhost:8080 (dev)
```

#### **Comandos Docker útiles**
```bash
# Ver logs en tiempo real
docker-compose logs -f

# Solo backend + database
docker-compose up -d postgres backend

# Incluir Adminer (desarrollo)
docker-compose --profile dev up -d

# Reconstruir después de cambios
docker-compose up -d --build

# Parar todo
docker-compose down

# Limpiar volúmenes (¡CUIDADO! - borra datos)
docker-compose down -v
```

---

### **💻 Opción 2: Instalación Manual (Desarrollo)**

#### **Prerrequisitos**
```bash
# Verificar versiones
python3 --version  # >= 3.11
node --version     # >= 16
npm --version      # >= 8
psql --version     # PostgreSQL 12+
```

#### **1. Clonar el repositorio**
```bash
git clone https://github.com/isaac1227/finanzas_app.git
cd finanzas_app
```

#### **2. Configurar PostgreSQL**
```bash
# Acceder a PostgreSQL
sudo -u postgres psql

# Crear base de datos y usuario
CREATE DATABASE finanzas_db;
CREATE USER finanzas_user WITH PASSWORD 'tu_password_seguro';
GRANT ALL PRIVILEGES ON DATABASE finanzas_db TO finanzas_user;
\q
```

#### **3. Configurar Backend**
```bash
cd backend

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
echo 'DATABASE_URL="postgresql://finanzas_user:tu_password_seguro@localhost/finanzas_db"' > .env

# Iniciar servidor
uvicorn app.main:app --reload --port 8000
```

#### **4. Configurar Frontend**
```bash
cd ../finanzas-frontend

# Instalar dependencias
npm install

# Iniciar aplicación
npm start
```

## 🐘 Comandos PostgreSQL Útiles

### **Acceso a la Base de Datos**
```bash
# Conectar a PostgreSQL como usuario finanzas_user
psql -h localhost -U finanzas_user -d finanzas_db

# Conectar como superusuario postgres
sudo -u postgres psql finanzas_db
```

### **Comandos de Consulta y Visualización**
```sql
-- Ver todas las tablas
\dt

-- Describir estructura de tabla
\d transacciones
\d sueldos

-- Ver todas las transacciones
SELECT * FROM transacciones ORDER BY fecha DESC;

-- Ver transacciones de un mes específico
SELECT * FROM transacciones 
WHERE EXTRACT(month FROM fecha) = 9 
AND EXTRACT(year FROM fecha) = 2025;

-- Ver todos los sueldos
SELECT * FROM sueldos ORDER BY anio DESC, mes DESC;

-- Resumen de transacciones por tipo
SELECT 
    tipo,
    COUNT(*) as cantidad,
    SUM(cantidad) as total,
    AVG(cantidad) as promedio
FROM transacciones 
GROUP BY tipo;

-- Saldo mensual completo (como lo hace la API)
SELECT 
    s.cantidad as sueldo,
    COALESCE(SUM(CASE WHEN t.tipo = 'ingreso' THEN t.cantidad ELSE 0 END), 0) as ingresos,
    COALESCE(SUM(CASE WHEN t.tipo = 'gasto' THEN t.cantidad ELSE 0 END), 0) as gastos,
    s.cantidad + 
    COALESCE(SUM(CASE WHEN t.tipo = 'ingreso' THEN t.cantidad ELSE 0 END), 0) - 
    COALESCE(SUM(CASE WHEN t.tipo = 'gasto' THEN t.cantidad ELSE 0 END), 0) as saldo_total
FROM sueldos s
LEFT JOIN transacciones t ON EXTRACT(month FROM t.fecha) = s.mes 
                          AND EXTRACT(year FROM t.fecha) = s.anio
WHERE s.mes = 9 AND s.anio = 2025
GROUP BY s.mes, s.anio, s.cantidad;

-- Ver últimas 10 transacciones with formato legible
SELECT 
    id,
    tipo,
    cantidad,
    TO_CHAR(fecha, 'DD/MM/YYYY HH24:MI') as fecha_formato,
    COALESCE(descripcion, 'Sin descripción') as descripcion
FROM transacciones 
ORDER BY fecha DESC 
LIMIT 10;

-- Salir de PostgreSQL
\q
```

### **Comandos de Mantenimiento**
```sql
-- Limpiar todas las transacciones (¡CUIDADO!)
DELETE FROM transacciones;

-- Limpiar todos los sueldos (¡CUIDADO!)
DELETE FROM sueldos;

-- Insertar datos de prueba
INSERT INTO transacciones (tipo, cantidad, descripcion, fecha) VALUES 
('ingreso', 100.50, 'Freelance proyecto', '2025-09-15 10:30:00'),
('gasto', 25.75, 'Café y comida', '2025-09-15 14:15:00'),
('gasto', 150.00, 'Supermercado', '2025-09-16 18:00:00');

INSERT INTO sueldos (cantidad, mes, anio) VALUES 
(2500.00, 9, 2025);

-- Ver información del sistema
SELECT version();
SELECT current_database();
SELECT current_user;
```

## 🔌 API Endpoints

### **Transacciones**
- `GET /transacciones` - Listar todas las transacciones  
- `GET /transacciones?mes=9&anio=2025` - Filtrar por mes
- `POST /transacciones` - Crear nueva transacción
- `PUT /transacciones/{id}` - Actualizar transacción
- `DELETE /transacciones/{id}` - Eliminar transacción

### **Sueldos**
- `GET /sueldos` - Listar todos los sueldos
- `GET /sueldos/{anio}/{mes}` - Obtener sueldo específico
- `POST /sueldos` - Crear o actualizar sueldo

### **Inicio**
- `GET /saldo-total?mes=9&anio=2025` - Saldo completo del mes

## 🎓 Conocimientos Aplicados

### **Backend Development**
- ✅ **REST API Design** - Endpoints RESTful con FastAPI
- ✅ **Database Design** - Esquema relacional con restricciones
- ✅ **ORM Usage** - SQLAlchemy con modelos y relaciones
- ✅ **Data Validation** - Pydantic schemas con validaciones
- ✅ **CRUD Operations** - Separación de lógica de negocio
- ✅ **Query Optimization** - Filtros eficientes con SQLAlchemy

### **Frontend Development**
- ✅ **React Hooks** - useState, useEffect para estado
- ✅ **API Integration** - Fetch con manejo de errores
- ✅ **Responsive Design** - Bootstrap 5 con grid system
- ✅ **Component Architecture** - Componentes reutilizables
- ✅ **State Management** - Estado local con React hooks
- ✅ **User Experience** - Confirmaciones, loading states

### **Database Management**
- ✅ **PostgreSQL** - Base de datos relacional avanzada
- ✅ **Schema Design** - Tablas con restricciones de integridad
- ✅ **Data Modeling** - Relaciones y constraints únicos
- ✅ **Query Writing** - SQL para reportes y agregaciones

## 📈 Métricas del Proyecto

- **📁 Archivos de código**: ~15 archivos principales
- **📝 Líneas de código**: ~1,500 líneas (Python + JavaScript)
- **🔌 Endpoints API**: 8 endpoints RESTful
- **🎨 Componentes React**: 2 componentes principales
- **🗄️ Tablas de BD**: 2 tablas con relaciones
- **⚡ Funcionalidades**: 6 funcionalidades principales

## 🌐 Acceso

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs (Swagger UI automático)
- **Base de datos**: localhost:5432/finanzas_db

## 🧪 Testing y Calidad de Código

### **Suite de Tests Completa Implementada**

El proyecto cuenta con **68 tests automatizados** que cubren tanto backend como frontend:

#### **🔧 Backend Testing (36 tests)**
```bash
cd backend
python3 -m pytest -v
```

**Cobertura Backend:**
- ✅ **16 tests CRUD**: Operaciones de base de datos con SQLAlchemy
- ✅ **20 tests API**: Endpoints FastAPI con TestClient
- ✅ **Fixtures compartidas**: Base de datos SQLite temporal para tests
- ✅ **Dependency injection**: Override de dependencias para testing
- ✅ **Validaciones**: Tests de errores y edge cases

#### **⚛️ Frontend Testing (32 tests)**
```bash
cd finanzas-frontend
npm test                    # Todos los tests
npm test -- --watchAll=false  # Sin modo watch
```

**Cobertura Frontend:**
- ✅ **Navbar (2 tests)**: Navegación y routing básico
- ✅ **Inicio (6 tests)**: Componente complejo con API calls, loading states
- ✅ **Transacciones (10 tests)**: CRUD completo, formularios, validaciones
- ✅ **Gráficos (12 tests)**: Chart.js mock, visualización de datos
- ✅ **App (1 test)**: Integración y renderizado general
- ✅ **BasicTest (1 test)**: Verificación de setup

#### **🛠️ Tecnologías de Testing Utilizadas**

**Backend:**
- **pytest**: Framework principal de testing
- **FastAPI TestClient**: Cliente HTTP para testing de APIs  
- **SQLAlchemy**: Base de datos temporal para tests aislados
- **Fixtures**: Configuración reutilizable de tests

**Frontend:**
- **React Testing Library**: Testing centrado en el usuario
- **Jest**: Framework de testing y mocking
- **@testing-library/jest-dom**: Matchers adicionales para DOM
- **React Router Testing**: Testing de navegación

#### **🎯 Características Avanzadas de Testing**

- **🎭 Mocking avanzado**: fetch API, Chart.js, React Router
- **⏳ Testing asíncrono**: waitFor, estados de loading  
- **🔄 Testing de estados**: loading, error, éxito, vacío
- **📝 Testing de formularios**: input, submit, validaciones
- **🖱️ Testing de interacciones**: click, change, confirmaciones
- **📊 Testing de visualizaciones**: Chart.js components mock
- **🛣️ Testing de navegación**: BrowserRouter, MemoryRouter

#### **📊 Comandos de Testing Específicos**
```bash
# Frontend - Tests por componente
npm test -- --testPathPattern=Navbar.test.js
npm test -- --testPathPattern=Inicio.test.js
npm test -- --testPathPattern=Transacciones.test.js
npm test -- --testPathPattern=Graficos.test.js

# Frontend - Con verbose output
npm test -- --verbose --watchAll=false

# Backend - Tests por categoría
python3 -m pytest tests/test_crud.py -v      # Solo CRUD
python3 -m pytest tests/test_main.py -v      # Solo API
python3 -m pytest --tb=short                 # Output compacto
```

#### **✅ Beneficios Conseguidos**
- **Detección temprana de bugs** y regresiones
- **Refactoring seguro** con confianza en los cambios
- **Documentación viva** del comportamiento esperado  
- **CI/CD ready** para integración continua
- **Patrones reutilizables** para futuros componentes
- **Cobertura completa** de funcionalidades críticas

## 📚 Próximas Mejoras (Roadmap de Aprendizaje)

- [ ] **Autenticación**: JWT tokens con FastAPI Security
- [x] **Testing**: Tests unitarios con pytest y React Testing Library ✅  
- [x] **Docker**: Containerización completa del stack ✅
- [ ] **CI/CD**: GitHub Actions para deployment automático
- [ ] **Charts**: Gráficos con Chart.js o D3.js
- [ ] **Mobile**: Progressive Web App (PWA)

## 🤝 Propósito Educativo

Este proyecto demuestra competencias en:
- **Desarrollo Full-Stack** completo con análisis financiero y visualización
- **Arquitectura de software** bien estructurada con estado compartido
- **Integración de librerías** externas (Chart.js) en React
- **Mejores prácticas** de desarrollo web y UX/UI
- **Documentación profesional** de proyectos
- **Resolución de problemas** técnicos reales

---

**📧 Contacto**: [isaac1227@github.com](mailto:isaac1227@github.com)  
**🔗 Portfolio**: [Más proyectos en mi GitHub](https://github.com/isaac1227)

## � Notificaciones (Frontend)

Se ha añadido un sistema de notificaciones en el frontend usando la librería `react-hot-toast`.

- Ubicación: la integración global se realiza en `finanzas-frontend/src/App.js` con `<Toaster />`.
- Uso en componentes: los componentes (por ejemplo `Transacciones.js` e `Inicio.js`) llaman a `toast.success(...)` y `toast.error(...)` para mostrar mensajes de resultado o validación.
- Mensajes comunes:
    - "Introduce una cantidad válida para la transacción"
    - "Introduce una descripción para la transacción"
    - "Transacción guardada correctamente"
    - "Transacción actualizada correctamente"

Cómo probar:
1. Arranca la aplicación (docker-compose o `npm start` dentro de `finanzas-frontend`).
2. Ve a la sección "Transacciones" del frontend.
3. Intenta crear una transacción sin cantidad o sin descripción — aparecerá un toast de error.
4. Crea/edita correctamente una transacción — aparecerá un toast de éxito.

## �🐳 Dockerización Completa

El proyecto ha sido completamente dockerizado para facilitar su despliegue y desarrollo. A continuación, se describen los detalles de la configuración:

### **Servicios Configurados**
- **Backend**: Contenedor basado en FastAPI con auto-reload habilitado para desarrollo.
- **Frontend**: Contenedor basado en React con servidor de desarrollo.
- **Base de Datos**: PostgreSQL configurado con persistencia de datos.
- **Adminer**: Herramienta de administración de base de datos (solo en desarrollo).

### **Características Clave**
- **Archivos Docker**: Dockerfiles separados para backend y frontend.
- **Orquestación**: Uso de `docker-compose.yml` para gestionar todos los servicios.
- **Variables de Entorno**: Configuración centralizada mediante archivos `.env`.
- **Perfiles de Desarrollo**: Uso de perfiles en Docker Compose para incluir herramientas como Adminer.
- **Reconstrucción Simplificada**: Comandos para reconstruir imágenes tras cambios en el código.

### **Comandos Principales**
```bash
# Iniciar todos los servicios
docker-compose up -d

# Reconstruir imágenes después de cambios
docker-compose up -d --build

# Parar y limpiar todos los servicios
docker-compose down -v
```

### **Accesos**
- **Frontend**: [http://localhost:3001](http://localhost:3001)
- **Backend API**: [http://localhost:8001](http://localhost:8001)
- **Documentación API**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **Adminer**: [http://localhost:8080](http://localhost:8080) (solo en desarrollo)

### **Beneficios de la Dockerización**
- **Portabilidad**: El proyecto puede ejecutarse en cualquier máquina con Docker instalado.
- **Aislamiento**: Cada servicio se ejecuta en su propio contenedor, evitando conflictos.
- **Facilidad de Uso**: Comandos simples para iniciar, detener y reconstruir servicios.
- **Optimización para Desarrollo**: Auto-reload habilitado para backend y frontend.