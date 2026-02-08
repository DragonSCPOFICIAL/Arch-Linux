#!/bin/bash

# BRX AI App - Desinstalador Robusto para Linux
# Remove o agente autônomo de IA do sistema completamente
# Mantenedor: DragonSCPOFICIAL

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
APP_NAME="brx_ai_app"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
AUTO_CONFIRM=false

# Verificar flag --auto
if [[ "$1" == "--auto" ]]; then
    AUTO_CONFIRM=true
fi

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# ============================================================================
# CONFIRMAÇÃO
# ============================================================================
if [ "$AUTO_CONFIRM" = false ]; then
    print_header "Desinstalação do BRX AI"
    echo ""
    print_warning "Você está prestes a desinstalar o BRX AI"
    echo "Isso removerá:"
    echo "  • Arquivos de aplicação em $INSTALL_DIR"
    echo "  • Link simbólico em $BIN_DIR/$APP_NAME"
    echo "  • Atalho do menu em $DESKTOP_DIR"
    echo ""
    read -p "Deseja continuar? (s/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_info "Desinstalação cancelada"
        exit 0
    fi
fi

# ============================================================================
# REMOVER PROCESSOS ATIVOS
# ============================================================================
print_header "Encerrando Processos"
pkill -f "brx_ai_app" || true
pkill -f "BRX_AI/src/main.py" || true
print_success "Processos encerrados"

# ============================================================================
# REMOVER ATALHO DO MENU
# ============================================================================
print_header "Removendo Atalho do Menu"
if [ -f "$DESKTOP_DIR/$APP_NAME.desktop" ]; then
    rm -f "$DESKTOP_DIR/$APP_NAME.desktop"
    print_success "Atalho removido de $DESKTOP_DIR"
fi
# Verificar também em diretórios globais
sudo rm -f "/usr/share/applications/$APP_NAME.desktop" || true

# ============================================================================
# REMOVER LINK SIMBÓLICO
# ============================================================================
print_header "Removendo Link Simbólico"
sudo rm -f "$BIN_DIR/$APP_NAME" || true
sudo rm -f "/usr/bin/$APP_NAME" || true
print_success "Links simbólicos removidos"

# ============================================================================
# REMOVER DIRETÓRIO DE INSTALAÇÃO
# ============================================================================
print_header "Removendo Diretório de Instalação"
if [ -d "$INSTALL_DIR" ]; then
    sudo rm -rf "$INSTALL_DIR"
    print_success "Diretório $INSTALL_DIR removido"
else
    print_info "Diretório de instalação não encontrado"
fi

# ============================================================================
# REMOVER DADOS DO USUÁRIO
# ============================================================================
print_header "Limpando Dados de Usuário"
if [ "$AUTO_CONFIRM" = true ]; then
    rm -rf "$HOME/.brx_ai"
    rm -f "$HOME/.brx_ai_app.log"
    print_success "Dados de usuário e logs removidos"
else
    if [ -d "$HOME/.brx_ai" ] || [ -f "$HOME/.brx_ai_app.log" ]; then
        echo ""
        read -p "Deseja remover dados do usuário e logs (~/.brx_ai)? (s/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            rm -rf "$HOME/.brx_ai"
            rm -f "$HOME/.brx_ai_app.log"
            print_success "Dados limpos"
        else
            print_info "Dados mantidos"
        fi
    fi
fi

# ============================================================================
# FINALIZAÇÃO
# ============================================================================
print_header "Desinstalação Concluída!"
echo ""
print_success "BRX AI foi removido completamente do sistema."
echo ""
