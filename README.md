# 💰 Finanzas App - Gestor Personal de Finanzas

**Proyecto personal de práctica** para el aprendizaje y dominio de tecnologías modernas de desarrollo web full-stack.

## 📖 Descripción del Proyecto

**Finanzas App** es una aplicación web completa para la gestión personal de finanzas que permite a los usuarios controlar sus ingresos, gastos y sueldos de manera organizada por meses. El proyecto fue desarrollado como una práctica integral de tecnologías modernas de desarrollo web, implementando un stack completo con frontend en React y backend en FastAPI.

### 🎯 Propósito

Este proyecto sirve como:
- **Práctica de desarrollo full-stack** con tecnologías modernas
- **Aprendizaje de arquitectura API REST** con FastAPI
- **Experiencia con React** y gestión de estado
- **Implementación de base de datos** con SQLAlchemy
- **Diseño de interfaces** con Bootstrap
- **Gestión de proyectos** con Git

## ✨ Funcionalidades Principales

### 💵 Gestión de Sueldos
- ✅ **Un sueldo por mes** - Registro único mensual con validación de BD
- ✅ **Crear/Actualizar** - Sistema inteligente que crea o actualiza automáticamente
- ✅ **Selector de mes** - Gestión de sueldos para cualquier mes del año
- ✅ **Validaciones** - Control de datos con Pydantic schemas

### 📊 Gestión de Transacciones
- ✅ **Ingresos y gastos** - Clasificación automática con colores
- ✅ **Filtrado por mes** - Vista organizada por periodos mensuales
- ✅ **CRUD completo** - Crear, leer, actualizar y eliminar transacciones
- ✅ **Confirmaciones** - Seguridad ante eliminaciones accidentales

### 📈 Dashboard Inteligente
- ✅ **Saldo mensual** - Cálculo automático por mes (no acumulativo)
- ✅ **Desglose detallado** - Sueldos + Balance de transacciones
- ✅ **Indicadores visuales** - Colores intuitivos (verde/rojo)
- ✅ **Resúmenes automáticos** - Totales de ingresos, gastos y balance

### 🎨 Interfaz Moderna
- ✅ **Diseño responsive** - Bootstrap 5 con sistema de grid
- ✅ **Componentes modernos** - Cards, badges, y estados visuales
- ✅ **Experiencia intuitiva** - Emojis, colores y confirmaciones
- ✅ **Estados de carga** - Feedback visual para el usuario

## 🛠️ Stack Tecnológico

### Backend (API REST)
- **🐍 Python 3.12** - Lenguaje principal
- **⚡ FastAPI** - Framework web moderno y rápido
- **🗄️ SQLAlchemy** - ORM para gestión de base de datos
- **✅ Pydantic** - Validación y serialización de datos
- **🐘 PostgreSQL** - Base de datos relacional (configurable)
- **🔄 Uvicorn** - Servidor ASGI de alto rendimiento

### Frontend (SPA)
- **⚛️ React 18** - Biblioteca de interfaces de usuario
- **🎨 Bootstrap 5** - Framework CSS para diseño responsive
- **📡 Fetch API** - Comunicación con el backend
- **🪝 React Hooks** - useState, useEffect para gestión de estado
- **📱 Responsive Design** - Adaptable a móviles y desktop

### Base de Datos
- **📊 Modelo relacional** con constraints y validaciones
- **🔗 Relaciones** optimizadas con índices
- **🛡️ Constraints únicos** para reglas de negocio
- **📅 Campos de auditoría** con timestamps automáticos

## 🏗️ Arquitectura del Proyecto

```
finanzas-app/
├── backend/                 # API REST en FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # Endpoints y aplicación principal
│   │   ├── models.py       # Modelos SQLAlchemy
│   │   ├── schemas.py      # Schemas Pydantic
│   │   ├── crud.py         # Operaciones de base de datos
│   │   └── database.py     # Configuración de BD
│   └── requirements.txt    # Dependencias Python
├── finanzas-frontend/      # Aplicación React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   │   ├── Dashboard.js
│   │   │   └── Transacciones.js
│   │   └── App.js         # Aplicación principal
│   └── package.json       # Dependencias Node.js
└── README.md              # Documentación del proyecto
```

## 🚀 Configuración y Ejecución

### Prerrequisitos
- Python 3.12+
- Node.js 18+
- PostgreSQL (opcional, SQLite por defecto)

### 🔧 Backend Setup
```bash
cd backend/
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### ⚛️ Frontend Setup
```bash
cd finanzas-frontend/
npm install
npm start
```

### 🌐 Acceso
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## 📊 Modelo de Datos

### Tabla `transacciones`
- `id` - Identificador único
- `tipo` - "ingreso" | "gasto"
- `cantidad` - Monto de la transacción
- `descripcion` - Descripción opcional
- `fecha` - Timestamp automático

### Tabla `sueldos`
- `id` - Identificador único
- `cantidad` - Monto del sueldo
- `mes` - Mes (1-12)
- `anio` - Año
- `fecha` - Timestamp automático
- **Constraint único**: (mes, anio)

## 🎓 Aprendizajes Técnicos

### Backend Development
- ✅ **API REST** - Diseño y implementación de endpoints RESTful
- ✅ **Validación de datos** - Schemas con Pydantic para seguridad
- ✅ **ORM avanzado** - Consultas complejas con SQLAlchemy
- ✅ **Arquitectura en capas** - Separación Models/Schemas/CRUD/Endpoints
- ✅ **Manejo de errores** - HTTPExceptions y validaciones

### Frontend Development
- ✅ **React Hooks** - useState, useEffect para gestión de estado
- ✅ **Comunicación API** - Fetch con async/await
- ✅ **Componentización** - Componentes reutilizables y props
- ✅ **Manejo de formularios** - Estados controlados y validaciones
- ✅ **UX/UI Design** - Bootstrap, estados de carga, confirmaciones

### DevOps y Herramientas
- ✅ **Control de versiones** - Git para gestión del código
- ✅ **Gestión de dependencias** - pip y npm
- ✅ **Documentación** - README completo y comentarios en código
- ✅ **Debugging** - Herramientas de desarrollo y logs

## 🔮 Características Destacadas

### 🧠 Lógica de Negocio Inteligente
- **Sueldo único por mes** - Previene duplicados con constraints de BD
- **Cálculo mensual** - Saldos no acumulativos, por periodo específico
- **Filtrado dinámico** - Backend optimizado con parámetros de consulta

### 🎨 Experiencia de Usuario
- **Interfaz moderna** - Cards en lugar de tablas tradicionales
- **Feedback visual** - Estados de carga, confirmaciones, colores intuitivos
- **Responsive design** - Funciona perfectamente en móvil y desktop

### 🏗️ Arquitectura Escalable
- **Separación de responsabilidades** - Frontend/Backend independientes
- **API documentada** - Swagger automático con FastAPI
- **Código mantenible** - Estructura clara y comentarios explicativos

## 👨‍💻 Autor

**Isaac Marroquí** - Desarrollador en formación

Este proyecto representa mi práctica y aprendizaje en desarrollo full-stack, implementando buenas prácticas y tecnologías modernas para crear una aplicación funcional y bien estructurada.

---
### 📝 Notas del Desarrollo

- **Duración estimada**: 2-3 semanas de desarrollo activo
- **Propósito**: Proyecto personal de práctica y aprendizaje
- **Estado**: ✅ Funcional - En mejora continua
- **Licencia**: Uso personal y educativo

*Desarrollado con ❤️ para aprender y crecer como desarrollador full-stack*