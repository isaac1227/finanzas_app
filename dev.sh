#!/bin/bash

# 🚀 Script de desarrollo rápido para Finanzas App
# Uso: ./dev.sh [start|stop|restart|logs|build|clean]

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}🚀 Finanzas App - Gestión de Desarrollo${NC}"
    echo ""
    echo "Comandos disponibles:"
    echo -e "  ${GREEN}start${NC}    - Iniciar toda la aplicación"
    echo -e "  ${GREEN}stop${NC}     - Parar toda la aplicación"
    echo -e "  ${GREEN}restart${NC}  - Reiniciar toda la aplicación"
    echo -e "  ${GREEN}logs${NC}     - Ver logs en tiempo real"
    echo -e "  ${GREEN}build${NC}    - Reconstruir imágenes"
    echo -e "  ${GREEN}clean${NC}    - Limpiar todo (¡CUIDADO! Borra datos)"
    echo -e "  ${GREEN}dev${NC}      - Modo desarrollo (incluye Adminer)"
    echo -e "  ${GREEN}test${NC}     - Ejecutar todos los tests"
    echo -e "  ${GREEN}status${NC}   - Ver estado de contenedores"
    echo ""
    echo "Ejemplos:"
    echo "  ./dev.sh start"
    echo "  ./dev.sh logs backend"
    echo "  ./dev.sh clean"
}

# Verificar que Docker está corriendo
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker no está corriendo. Por favor, inicia Docker primero.${NC}"
        exit 1
    fi
}

# Función principal
case "${1:-help}" in
    start)
        echo -e "${GREEN}🚀 Iniciando Finanzas App...${NC}"
        check_docker
        docker-compose up -d
        echo -e "${GREEN}✅ Aplicación iniciada!${NC}"
        echo -e "${BLUE}📱 Frontend: http://localhost:3001${NC}"
        echo -e "${BLUE}🔗 Backend: http://localhost:8001${NC}"
        echo -e "${BLUE}📚 API Docs: http://localhost:8001/docs${NC}"
        ;;
        
    stop)
        echo -e "${YELLOW}⏹️  Parando Finanzas App...${NC}"
        docker-compose down
        echo -e "${GREEN}✅ Aplicación parada${NC}"
        ;;
        
    restart)
        echo -e "${YELLOW}🔄 Reiniciando Finanzas App...${NC}"
        docker-compose down
        docker-compose up -d
        echo -e "${GREEN}✅ Aplicación reiniciada${NC}"
        ;;
        
    logs)
        echo -e "${BLUE}📋 Mostrando logs...${NC}"
        if [ -n "$2" ]; then
            docker-compose logs -f "$2"
        else
            docker-compose logs -f
        fi
        ;;
        
    build)
        echo -e "${YELLOW}🔨 Reconstruyendo imágenes...${NC}"
        docker-compose build --no-cache
        docker-compose up -d
        echo -e "${GREEN}✅ Aplicación reconstruida${NC}"
        ;;
        
    clean)
        echo -e "${RED}🧹 ¡CUIDADO! Esto borrará todos los datos.${NC}"
        read -p "¿Estás seguro? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            docker system prune -f
            echo -e "${GREEN}✅ Limpieza completa realizada${NC}"
        else
            echo -e "${YELLOW}⏹️  Limpieza cancelada${NC}"
        fi
        ;;
        
    dev)
        echo -e "${GREEN}🛠️  Iniciando en modo desarrollo (con Adminer)...${NC}"
        check_docker
        docker-compose --profile dev up -d
        echo -e "${GREEN}✅ Modo desarrollo iniciado!${NC}"
        echo -e "${BLUE}📱 Frontend: http://localhost:3001${NC}"
        echo -e "${BLUE}🔗 Backend: http://localhost:8001${NC}"
        echo -e "${BLUE}📚 API Docs: http://localhost:8001/docs${NC}"
        echo -e "${BLUE}🗄️  Adminer: http://localhost:8080${NC}"
        ;;
        
    test)
        echo -e "${GREEN}🧪 Ejecutando tests...${NC}"
        echo -e "${YELLOW}Backend tests:${NC}"
        docker-compose exec backend python -m pytest -v || echo -e "${YELLOW}Backend no está corriendo${NC}"
        echo -e "${YELLOW}Frontend tests:${NC}"
        docker-compose exec frontend npm test -- --watchAll=false || echo -e "${YELLOW}Frontend no está corriendo${NC}"
        ;;
        
    status)
        echo -e "${BLUE}📊 Estado de contenedores:${NC}"
        docker-compose ps
        ;;
        
    help|*)
        show_help
        ;;
esac