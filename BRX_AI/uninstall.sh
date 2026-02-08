#!/bin/bash

# BRX AI App - Desinstalador para Linux
# Remove o agente autônomo de IA do sistema
# Mantenedor: DragonSCPOFICIAL

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
APP_NAME="brx_ai_app"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

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

# ============================================================================
# REMOVER ATALHO DO MENU
# ============================================================================
print_header "Removendo Atalho do Menu"

if [ -f "$DESKTOP_DIR/$APP_NAME.desktop" ]; then
    rm -f "$DESKTOP_DIR/$APP_NAME.desktop"
    print_success "Atalho removido"
else
    print_info "Atalho não encontrado (já removido?)"
fi

# ============================================================================
# REMOVER LINK SIMBÓLICO
# ============================================================================
print_header "Removendo Link Simbólico"

if [ -L "$BIN_DIR/$APP_NAME" ]; then
    sudo rm -f "$BIN_DIR/$APP_NAME"
    print_success "Link simbólico removido"
else
    print_info "Link simbólico não encontrado (já removido?)"
fi

# ============================================================================
# REMOVER DIRETÓRIO DE INSTALAÇÃO
# ============================================================================
print_header "Removendo Diretório de Instalação"

if [ -d "$INSTALL_DIR" ]; then
    sudo rm -rf "$INSTALL_DIR"
    print_success "Diretório de instalação removido"
else
    print_info "Diretório de instalação não encontrado (já removido?)"
fi

# ============================================================================
# OPÇÃO DE REMOVER DADOS DO USUÁRIO
# ============================================================================
print_header "Dados do Usuário"

if [ -d "$HOME/.brx_ai" ]; then
    echo ""
    read -p "Deseja remover dados do usuário em $HOME/.brx_ai? (s/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf "$HOME/.brx_ai"
        print_success "Dados do usuário removidos"
    else
        print_info "Dados do usuário mantidos"
    fi
fi

# ============================================================================
# FINALIZAÇÃO
# ============================================================================
print_header "Desinstalação Concluída!"

echo ""
print_success "BRX AI foi desinstalado com sucesso!"
echo ""
print_info "Obrigado por usar o BRX AI!"
echo ""
