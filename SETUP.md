# 🚀 Setup Rápido - Finanzas App

## ⚡ Inicio Rápido (5 minutos)

### 1️⃣ Clonar el proyecto
```bash
git clone https://github.com/isaac-marroqui/finanzas-app.git
cd finanzas-app
```

### 2️⃣ Backend Setup
```bash
cd backend/
pip install fastapi sqlalchemy pydantic uvicorn python-dotenv
uvicorn app.main:app --reload --port 8000
```
✅ Backend corriendo en: http://localhost:8000

### 3️⃣ Frontend Setup
```bash
cd ../finanzas-frontend/
npm install
npm start
```
✅ Frontend corriendo en: http://localhost:3000

## 🔧 Variables de Entorno (Opcional)

Crear `.env` en `/backend/`:
```env
DATABASE_URL=sqlite:///./finanzas.db
# O para PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/finanzas
```

## 📱 Uso Básico

1. **Dashboard** - Ver saldo mensual y gestionar sueldos
2. **Transacciones** - Añadir ingresos y gastos por mes
3. **Filtros** - Cambiar entre meses con el selector

## 🛠️ Dependencias Principales

### Backend
```txt
fastapi>=0.104.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
uvicorn[standard]>=0.24.0
python-dotenv>=1.0.0
```

### Frontend
```json
{
  "react": "^18.2.0",
  "bootstrap": "^5.3.0"
}
```

## 📊 API Endpoints

- `GET /` - Info de la API
- `GET /transacciones?mes=9&anio=2025` - Transacciones filtradas
- `POST /transacciones` - Crear transacción
- `PUT /transacciones/{id}` - Actualizar transacción
- `DELETE /transacciones/{id}` - Eliminar transacción
- `GET /sueldos/{anio}/{mes}` - Sueldo específico
- `POST /sueldos` - Crear/actualizar sueldo
- `GET /saldo-total?mes=9&anio=2025` - Saldo calculado

## 🔍 Documentación API

Una vez iniciado el backend: http://localhost:8000/docs

---
**¿Problemas?** Revisa que tengas Python 3.12+ y Node.js 18+