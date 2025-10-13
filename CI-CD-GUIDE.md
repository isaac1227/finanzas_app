# 🚀 CI/CD en Finanzas App

## ¿Qué es CI/CD?

**CI = Continuous Integration (Integración Continua)**
- Cada vez que haces `git push`, automáticamente se ejecutan los tests
- Si algo falla, te avisa inmediatamente

**CD = Continuous Deployment (Deploy Continuo)**  
- Si todos los tests pasan, automáticamente publica tu app
- No tienes que hacer deploy manual

## 🏗️ ¿Qué hace nuestro CI/CD?

### 1. **Backend Tests** 🐍
```bash
# Lo que hace automáticamente:
cd backend
pip install -r requirements.txt
pytest -v  # Ejecuta todos los tests
```

### 2. **Frontend Tests** ⚛️
```bash
# Lo que hace automáticamente:
cd finanzas-frontend  
npm ci
npm run test:ci  # Tests de React
npm run build    # Verifica que compile
```

### 3. **Integration Tests** 🐳
```bash
# Lo que hace automáticamente:
docker compose up -d --build  # Levanta todo
curl http://localhost:8000/docs  # Verifica que funcione
docker compose down  # Limpia
```

## 📁 Archivos que necesitas entender

### `.github/workflows/ci.yml` (EL ÚNICO IMPORTANTE)
```yaml
# Se ejecuta cuando haces git push
on:
  push:
    branches: [ main ]

jobs:
  backend-tests:    # Ejecuta tests del backend
  frontend-tests:   # Ejecuta tests del frontend  
  integration-tests: # Prueba todo junto con Docker
  deploy:           # Deploy (si está en main)
```

### Los archivos que YA TIENES y usa el CI/CD:
- `docker-compose.yml` ✅ (ya lo tienes)
- `backend/Dockerfile` ✅ (ya lo tienes)
- `finanzas-frontend/Dockerfile` ✅ (ya lo tienes)
- `backend/requirements.txt` ✅ (ya lo tienes)
- `finanzas-frontend/package.json` ✅ (ya lo tienes)

## 🔄 Flujo completo

```
1. Haces cambios en tu código
2. git add . && git commit -m "mi cambio"
3. git push origin main
4. 🤖 GitHub ejecuta automáticamente:
   ├── Tests del backend
   ├── Tests del frontend  
   ├── Tests de integración
   └── Deploy (si todo sale bien)
5. ✅ Te llega notificación: "Todo OK" o ❌ "Algo falló"
```

## 🎯 Componentes clave

**Elementos principales:**
1. **Un archivo**: `.github/workflows/ci.yml`
2. **Una acción**: Hacer `git push`  
3. **Un resultado**: Tests automáticos + deploy

**Los detalles técnicos se ejecutan automáticamente en segundo plano.**

## 🛠️ Para probarlo

1. Haz cualquier cambio pequeño
2. `git add . && git commit -m "test CI/CD"`
3. `git push origin main`
4. Ve a GitHub → tu repositorio → pestaña "Actions"
5. Verás tu pipeline ejecutándose en tiempo real

## ❓ ¿Por qué es útil?

- **Sin CI/CD**: Cada vez que cambias algo, necesitas probar todo manualmente
- **Con CI/CD**: Cambias algo → automáticamente se prueba todo → deploy automático

Automatiza el proceso de testing y deployment.

## 🚨 ¿Qué hacer si hay errores?

### 1. **Ver el error en GitHub**
1. Ve a tu repositorio en GitHub
2. Pestaña "Actions" 
3. Haz clic en el commit que falló (aparece con ❌)
4. Haz clic en el job que falló (Backend Tests, Frontend Tests, etc.)
5. Expande la sección que tiene el error

### 2. **Tipos de errores comunes**

#### **🐍 Backend Tests fallan**
```bash
# Error típico: test falló
FAILED tests/test_algo.py::test_function - AssertionError

# Qué hacer:
cd backend
pytest tests/test_algo.py::test_function -v  # Ejecuta solo ese test
# Arregla el código o actualiza el test
```

#### **⚛️ Frontend Tests fallan**
```bash
# Error típico: test de React falló
FAIL src/components/__tests__/Algo.test.js

# Qué hacer:
cd finanzas-frontend
npm test -- --testNamePattern="nombre del test"  # Ejecuta solo ese test
# Arregla el componente o actualiza el test
```

#### **🐳 Integration Tests fallan**
```bash
# Error típico: no se puede conectar a la API
curl: (7) Failed to connect to localhost:8000

# Qué hacer:
docker compose up -d  # Levanta los servicios localmente
docker compose logs backend  # Ve los logs del backend
docker compose logs postgres  # Ve los logs de la base de datos
```

#### **📦 Dependency errors**
```bash
# Error típico: paquete no encontrado
ModuleNotFoundError: No module named 'algo'
# o
Cannot resolve dependency 'algo'

# Qué hacer:
# Backend: actualiza requirements.txt
# Frontend: ejecuta npm install y actualiza package.json
```

### 3. **Flujo de resolución**

```bash
# 1. Reproduce el error localmente
git pull origin main  # Asegúrate de tener la última versión

# 2. Backend
cd backend
python -m pytest -v  # Ejecuta tests localmente

# 3. Frontend  
cd finanzas-frontend
npm test  # Ejecuta tests localmente

# 4. Integration
docker compose up -d  # Prueba todo junto
curl http://localhost:8000/docs  # Verifica que funcione

# 5. Si todo funciona local, pero falla en CI:
# Revisa las diferencias de entorno (versiones, variables, etc.)
```

### 4. **Comandos de emergencia**

```bash
# Ver logs detallados
docker compose logs -f backend
docker compose logs -f postgres

# Reiniciar todo
docker compose down -v  # Borra volúmenes también
docker compose up -d --build  # Reconstruye todo

# Tests específicos
pytest tests/test_archivo.py::test_funcion -v -s  # Backend
npm test -- --testNamePattern="test name"  # Frontend
```

### 5. **Cuándo ignorar temporalmente**

Si necesitas hacer un push urgente y hay un test roto que no afecta la funcionalidad:

```bash
# Opción 1: Skip el test temporalmente
@pytest.mark.skip(reason="Fix pendiente")
def test_algo():
    pass

# Opción 2: Commit con [skip ci] (úsalo con cuidado)
git commit -m "fix urgente [skip ci]"
```

**⚠️ Recuerda arreglar los tests después, no los dejes rotos permanentemente.**