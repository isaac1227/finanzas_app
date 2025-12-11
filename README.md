# 💰 Finanzas App - Gestión Personal de Finanzas con Autenticación JWT

[![CI/CD Pipeline](https://github.com/isaac1227/finanzas_app/actions/workflows/ci.yml/badge.svg)](https://github.com/isaac1227/finanzas_app/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-passing-green.svg)](https://github.com/isaac1227/finanzas_app/actions)
[![Clean Architecture](https://img.shields.io/badge/architecture-clean-blue.svg)](#-arquitectura-del-proyecto-clean-architecture)

Un proyecto personal **full-stack** desarrollado para **practicar y demostrar competencias** en desarrollo web moderno con **autenticación JWT**, **FastAPI**, **React** y **PostgreSQL**.

## 🎯 Objetivo del Proyecto

Este proyecto fue creado como **ejercicio de aprendizaje avanzado** para practicar:
- 🔐 **Autenticación JWT completa** (registro, login, protección de rutas)
- 🚀 Desarrollo de APIs REST seguras con FastAPI
- ⚛️ Frontend moderno con React y gestión de estado
- 🗄️ Gestión de bases de datos con PostgreSQL y SQLAlchemy
- 🏗️ Arquitectura full-stack con separación de usuarios
- 📚 Documentación profesional de proyectos

## 🛠️ Stack Tecnológico

### **Backend**
- **FastAPI** - Framework web moderno y rápido para Python
- **SQLAlchemy** - ORM para manejo de base de datos
- **JWT (JSON Web Tokens)** - Autenticación stateless y segura
- **Passlib** - Hasheo seguro de contraseñas (pbkdf2_sha256)
- **Python-Jose** - Manejo de tokens JWT
- **Pydantic** - Validación de datos y serialización
- **PostgreSQL** - Base de datos relacional
- **Python 3.11+** - Lenguaje de programación

### **Frontend**
- **React 18** - Biblioteca para interfaces de usuario
- **JWT Authentication** - Sistema completo de autenticación
- **LocalStorage** - Persistencia segura de tokens
- **Bootstrap 5** - Framework CSS para diseño responsivo
- **React Hot Toast** - Notificaciones UX
- **Chart.js** - Visualización de datos
- **JavaScript ES6+** - Lenguaje de programación frontend

### **Desarrollo & Deploy**
- **Docker & Docker Compose** - Containerización completa
- **Git** - Control de versiones
- **uvicorn** - Servidor ASGI para desarrollo
- **npm** - Gestión de dependencias frontend

## ✨ Funcionalidades

### **🔐 Sistema de Autenticación JWT**
- **Registro de usuarios** con validación de email y contraseña
- **Login seguro** con JWT tokens (30 min de expiración)
- **Protección de rutas** automática en frontend y backend
- **Separación completa de usuarios** - cada uno ve solo sus datos
- **Logout automático** cuando el token expira
- **Interfaz moderna** con diseño UX/UI profesional
- **Hasheo seguro** de contraseñas con pbkdf2_sha256

### **🏠 Dashboard Personalizado (Inicio)**
- **Datos únicos por usuario** - completa privacidad
- Visualización del saldo mensual (no acumulativo)
- Desglose por: Saldo Total, Sueldos, Transacciones
- Selector de mes maestro que sincroniza toda la aplicación
- Gestión de sueldos (un sueldo por mes)
- **Gráficos integrados** con Chart.js mostrando análisis visual

### **📊 Análisis Visual con Gráficos**
- **Gráfico de barras profesional** (Gastos vs Ingresos por usuario)
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

## 🔐 **Sistema JWT Implementado**

### **Flujo de Autenticación Completo**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │    │    Backend      │    │   Base Datos    │
│   (React)       │    │   (FastAPI)     │    │  (PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │ 1. POST /register     │                       │
         ├──────────────────────►│ 2. Hash password      │
         │                       ├──────────────────────►│ 3. Save user
         │ 4. 201 Created        │◄──────────────────────┤
         │◄──────────────────────┤                       │
         │                       │                       │
         │ 5. POST /login        │                       │
         ├──────────────────────►│ 6. Verify password    │
         │                       ├──────────────────────►│ 7. Get user
         │ 8. JWT Token          │◄──────────────────────┤
         │◄──────────────────────┤                       │
         │                       │                       │
         │ 9. API + JWT Header   │                       │
         ├──────────────────────►│ 10. Verify JWT        │
         │                       ├──────────────────────►│ 11. User data
         │ 12. Protected data    │◄──────────────────────┤
         │◄──────────────────────┤                       │
```

### **Características de Seguridad**

- 🔒 **Contraseñas hasheadas** con `pbkdf2_sha256` (compatible Docker)
- 🎫 **JWT Tokens** con expiración de 30 minutos
- 🛡️ **Middleware de autenticación** en todos los endpoints protegidos
- 👤 **Separación completa de usuarios** - aislamiento total de datos
- 🚪 **Logout automático** cuando el token expira o es inválido
- 📱 **Stateless** - escalable y compatible con múltiples dispositivos

## 🏗️ Arquitectura del Proyecto (Clean Architecture)

```
finanzas-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/       # Controladores (Auth, Transacciones, Sueldos)
│   │   │   └── dependencies/    # Inyección de dependencias (Use Cases, Repos)
│   │   ├── application/
│   │   │   ├── dtos/            # DTOs de entrada/salida
│   │   │   └── use_cases/       # Casos de uso por agregado
│   │   ├── domain/
│   │   │   ├── entities/        # Entidades de dominio
│   │   │   └── repositories/    # Interfaces de repositorios
│   │   ├── infrastructure/
│   │   │   ├── database/        # Repositorios SQLAlchemy, modelos ORM
│   │   │   └── config/          # Sesiones de DB, settings
│   │   ├── auth.py              # Servicios de autenticación (hash/JWT)
│   │   └── main.py              # FastAPI app, middlewares y routers
│   ├── requirements.txt
│   └── tests/                   # Tests unitarios e integración (pytest)
├── finanzas-frontend/
│   └── src/                     # React app (authService, componentes, etc.)
├── docker-compose.yml
├── README.md
└── SETUP.md
```

Ventajas:
- Separación clara de responsabilidades (API ↔ Use Cases ↔ Dominio ↔ Infraestructura)
- Testeabilidad mejorada (mocks/stubs a nivel de repositorios)
- Sostenibilidad para crecimiento (nuevos casos de uso/endpoints sin acoplar capas)

## 🚀 Instalación y Configuración

### **� Primer Uso - Sistema de Autenticación**

1. **Accede a la aplicación**: http://localhost:3001
2. **Crea tu primera cuenta** con el formulario de registro
3. **Automáticamente serás logueado** y tendrás acceso completo
4. **Tus datos son privados** - solo tú puedes ver tus finanzas
5. **El token expira en 30 minutos** - se renovará automáticamente

### **�🐳 Opción 1: Con Docker (RECOMENDADO)**

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

O bien, usando Docker (recomendado):

```bash
docker compose exec backend pytest -q
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

### **🔐 Autenticación (Públicos)**
- `POST /auth/register` - Registro de nuevos usuarios
- `POST /auth/login` - Login con email/contraseña → retorna JWT (JSON)
- `POST /auth/token` - Login estilo OAuth2PasswordRequestForm (docs)
- `GET /auth/me` - Información del usuario actual (requiere JWT)

### **📊 Transacciones (Protegidos con JWT)**
- `GET /transacciones` - Listar transacciones del usuario actual
- `GET /transacciones?mes=9&anio=2025` - Filtrar por mes (usuario actual)
- `POST /transacciones` - Crear nueva transacción (usuario actual)
- `PUT /transacciones/{id}` - Actualizar transacción (solo si es tuya)
- `DELETE /transacciones/{id}` - Eliminar transacción (solo si es tuya)

### **💰 Sueldos (Protegidos con JWT)**
- `GET /sueldos` - Listar sueldos del usuario actual
- `GET /sueldos/{anio}/{mes}` - Obtener sueldo específico (usuario actual)
- `POST /sueldos` - Crear o actualizar sueldo (usuario actual)

### **📈 Dashboard (Protegido con JWT)**
- `GET /saldo-total?mes=9&anio=2025` - Saldo completo del mes (usuario actual)

> 🔒 **Todos los endpoints protegidos requieren header**: `Authorization: Bearer <jwt_token>`

## 🎓 Conocimientos Aplicados

### **🔐 Autenticación & Seguridad**
- ✅ **JWT (JSON Web Tokens)** - Implementación completa stateless
- ✅ **Password Hashing** - pbkdf2_sha256 con salt automático  
- ✅ **Bearer Authentication** - Headers HTTP automáticos
- ✅ **Route Protection** - Middleware de autenticación
- ✅ **User Separation** - Aislamiento completo de datos por usuario
- ✅ **Token Management** - Expiración, renovación automática
- ✅ **Security Headers** - CORS, Content-Type, Authorization

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

- **📁 Archivos de código**: ~20 archivos principales (+33% con JWT)
- **📝 Líneas de código**: ~2,000 líneas (Python + JavaScript) (+33% con auth)
- **🔌 Endpoints API**: 11 endpoints (8 protegidos + 3 auth)
- **🎨 Componentes React**: 4 componentes principales (+Login, AuthService)
- **🗄️ Tablas de BD**: 3 tablas con relaciones (Usuarios + Transacciones + Sueldos)
- **⚡ Funcionalidades**: 8 funcionalidades (+Registro, Login, JWT)
- **🔐 Seguridad**: Autenticación completa, separación de usuarios
- **🐳 Docker**: Aplicación completamente containerizada

## 🌐 Acceso

### **URLs de la Aplicación (Docker)**
- **🔐 Frontend con Login**: http://localhost:3001
- **📚 API Backend**: http://localhost:8001
- **📖 Documentación API**: http://localhost:8001/docs (Swagger UI con auth)
- **🗄️ Base de datos**: localhost:5433/finanzas_db
- **🔧 Adminer DB**: http://localhost:8080 (usuario: finanzas, pass: finanzas)

### **URLs de Desarrollo (Local)**
- **Frontend**: http://localhost:3000 (si usas `npm start`)
- **Backend**: http://localhost:8000 (si usas `uvicorn`)

> 💡 **Recomendación**: Usa Docker para tener el entorno exacto con autenticación JWT

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

## 📚 Roadmap de Aprendizaje - Progreso Actual

### **✅ Completadas**
- [x] **🔐 Autenticación JWT completa**: Registro, login, tokens, separación usuarios ✅  
- [x] **📊 Gráficos interactivos**: Chart.js con métricas financieras ✅
- [x] **🧪 Testing**: Tests unitarios con pytest y React Testing Library ✅  
- [x] **🐳 Docker**: Containerización completa del stack ✅
- [x] **⚙️ CI/CD**: GitHub Actions con tests automáticos ✅
- [x] **🎨 UX/UI moderna**: Bootstrap, toasts, diseño responsivo ✅
- [x] **📚 Documentación**: README completo con diagramas y guías ✅

### **🚧 En Progreso / Próximas**
- [ ] **📱 Mobile**: Progressive Web App (PWA) 
- [ ] **🔄 Real-time**: WebSockets para actualizaciones en vivo
- [ ] **📈 Analytics**: Dashboard con métricas avanzadas
- [ ] **🌐 Multi-idioma**: Internacionalización (i18n)
- [ ] **☁️ Cloud Deploy**: Despliegue en AWS/Vercel/Railway

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

### **Beneficios de la Dockerización**
- **Portabilidad**: El proyecto puede ejecutarse en cualquier máquina con Docker instalado.
- **Aislamiento**: Cada servicio se ejecuta en su propio contenedor, evitando conflictos.
- **Facilidad de Uso**: Comandos simples para iniciar, detener y reconstruir servicios.
- **Optimización para Desarrollo**: Auto-reload habilitado para backend y frontend.

## ⚙️ CI/CD - Integración Continua

El proyecto cuenta con **GitHub Actions** que se ejecuta automáticamente en cada `push` o `pull request`:

### **¿Qué hace el CI/CD?**
1. **Tests Backend** - Ejecuta pytest sobre FastAPI (36 tests)
2. **Tests Frontend** - Ejecuta npm test sobre React (32 tests)
3. **Tests de Integración** - Levanta Docker Compose completo y verifica endpoints
4. **Validación** - Si algo falla ❌ rechaza el merge; si todo pasa ✅ permite mergear

### **Ver estado CI/CD**
```bash
# Ir a GitHub → Actions para ver el historial de ejecuciones
https://github.com/isaac1227/finanzas_app/actions/workflows/ci.yml
```