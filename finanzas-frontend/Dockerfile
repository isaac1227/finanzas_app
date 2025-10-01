# ⚛️ Frontend Dockerfile - React + Node.js
FROM node:18-alpine

# 📂 Crear directorio de trabajo
WORKDIR /app

# 📥 Copiar package files primero
COPY package*.json ./

# 🔧 Instalar dependencias
RUN npm install && npm cache clean --force

# 📁 Copiar el resto del código fuente
COPY . .

# 🌐 Configurar el puerto para el servidor de desarrollo
ENV PORT=3001

# 🌐 Exponer el puerto configurado
EXPOSE 3001

# 🚀 Comando por defecto para desarrollo
CMD ["npm", "start"]