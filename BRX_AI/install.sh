#!/bin/bash

# BRX AI App - Instalador para Linux
# Instala o agente autônomo de IA como aplicativo nativo
# Mantenedor: DragonSCPOFICIAL

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
APP_NAME="brx_ai_app"
APP_DISPLAY_NAME="BRX AI Agent"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

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
    echo -e "${GREEN}SUCCESS: $1${NC}"
}

print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

print_info() {
    echo -e "${BLUE}INFO: $1${NC}"
}

# ============================================================================
# VERIFICAÇÕES PRÉ-INSTALAÇÃO
# ============================================================================
print_header "Verificações Pré-Instalação"

# Verificar se é Linux
if [[ ! "$OSTYPE" =~ ^linux ]]; then
    print_error "Este instalador requer Linux"
    exit 1
fi
print_success "Sistema operacional: Linux"

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 não está instalado"
    print_info "Instale com: sudo pacman -S python (Arch) ou apt install python3 (Debian/Ubuntu)"
    exit 1
fi
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
print_success "Python 3 encontrado: $PYTHON_VERSION"

# Verificar se tkinter está disponível
if ! python3 -c "import tkinter" 2>/dev/null; then
    print_error "tkinter não está instalado"
    print_info "Instale com: sudo pacman -S tk (Arch) ou apt install python3-tk (Debian/Ubuntu)"
    exit 1
fi
print_success "tkinter encontrado"

# Verificar se psutil está disponível
if ! python3 -c "import psutil" 2>/dev/null; then
    print_warning "psutil não está instalado. Será instalado automaticamente."
fi

# ============================================================================
# CRIAR DIRETÓRIOS
# ============================================================================
print_header "Criando Diretórios"

# Criar diretório de instalação
if [ -d "$INSTALL_DIR" ]; then
    print_warning "Diretório $INSTALL_DIR já existe. Será sobrescrito."
    sudo rm -rf "$INSTALL_DIR"
fi

sudo mkdir -p "$INSTALL_DIR"
print_success "Diretório de instalação criado: $INSTALL_DIR"

sudo mkdir -p "$INSTALL_DIR/src"
sudo mkdir -p "$INSTALL_DIR/config"
sudo mkdir -p "$INSTALL_DIR/assets"
print_success "Subdiretórios criados"

# ============================================================================
# COPIAR ARQUIVOS
# ============================================================================
print_header "Copiando Arquivos"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copiar arquivos Python
sudo cp "$SCRIPT_DIR/config.py" "$INSTALL_DIR/"
sudo cp "$SCRIPT_DIR/src/main.py" "$INSTALL_DIR/src/"
sudo cp "$SCRIPT_DIR/src/ui.py" "$INSTALL_DIR/src/"
sudo cp "$SCRIPT_DIR/src/utils.py" "$INSTALL_DIR/src/"
print_success "Arquivos Python copiados"

# Copiar scripts
sudo cp "$SCRIPT_DIR/brx_ai_app.sh" "$INSTALL_DIR/"
sudo chmod +x "$INSTALL_DIR/brx_ai_app.sh"
print_success "Script de inicialização copiado"

# Copiar ícone
if [ -f "$SCRIPT_DIR/icon.png" ]; then
    sudo cp "$SCRIPT_DIR/icon.png" "$INSTALL_DIR/assets/"
    print_success "Ícone copiado para assets"
fi

# Copiar README se existir
if [ -f "$SCRIPT_DIR/README.md" ]; then
    sudo cp "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"
    print_success "README copiado"
fi

# ============================================================================
# INSTALAR DEPENDÊNCIAS PYTHON
# ============================================================================
print_header "Instalando Dependências Python"

# Detectar gerenciador de pacotes
if command -v pacman &> /dev/null; then
    print_info "Detectado: Arch Linux (pacman)"
    sudo pacman -S --noconfirm python-pillow python-requests python-pip 2>/dev/null || true
    print_success "Dependências do sistema instaladas"
elif command -v apt &> /dev/null; then
    print_info "Detectado: Debian/Ubuntu (apt)"
    sudo apt update
    sudo apt install -y python3-tk python3-pil python3-requests 2>/dev/null || true
    print_success "Dependências do sistema instaladas"
else
    print_warning "Gerenciador de pacotes não detectado. Pulando instalação de dependências do sistema."
fi

# Instalar psutil via pip
print_info "Instalando psutil..."
pip3 install psutil --break-system-packages 2>/dev/null || pip3 install psutil || true
print_success "Dependências Python instaladas"

# ============================================================================
# CRIAR LINK SIMBÓLICO
# ============================================================================
print_header "Criando Link Simbólico"

# Criar diretório se não existir
mkdir -p "$BIN_DIR"

# Remover link antigo se existir
sudo rm -f "$BIN_DIR/$APP_NAME"

# Criar novo link
sudo ln -sf "$INSTALL_DIR/brx_ai_app.sh" "$BIN_DIR/$APP_NAME"
sudo chmod +x "$BIN_DIR/$APP_NAME"
print_success "Link simbólico criado: $BIN_DIR/$APP_NAME"

# ============================================================================
# CRIAR ATALHO NO MENU
# ============================================================================
print_header "Criando Atalho no Menu"

mkdir -p "$DESKTOP_DIR"

# Criar arquivo .desktop
sudo bash -c "cat > $DESKTOP_DIR/$APP_NAME.desktop <<EOF"
[Desktop Entry]
Version=1.0
Type=Application
Name=$APP_DISPLAY_NAME
Comment=Agente de IA Autônomo com Visão e Controle para Linux
Exec=$BIN_DIR/$APP_NAME
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Categories=Utility;Development;AI;Automation;
Keywords=AI;BRX;Automation;Vision;Agent;
StartupNotify=true
EOF
"
sudo chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"
print_success "Atalho criado: $DESKTOP_DIR/$APP_NAME.desktop"

# ============================================================================
# CRIAR DIRETÓRIOS DE CONFIGURAÇÃO
# ============================================================================
print_header "Configurando Diretórios do Usuário"

mkdir -p "$HOME/.brx_ai/logs"
mkdir -p "$HOME/.brx_ai/data"
mkdir -p "$HOME/.brx_ai/cache"
print_success "Diretórios de configuração criados em $HOME/.brx_ai"

# ============================================================================
# FINALIZAÇÃO
# ============================================================================
print_header "Instalação Concluída!"

echo ""
print_success "BRX AI foi instalado com sucesso!"
echo ""
print_info "Como usar:"
echo "  • Terminal: Digite '$APP_NAME' para iniciar"
echo "  • Menu: Procure por '$APP_DISPLAY_NAME' no menu de aplicativos"
echo "  • Atalho: Clique no atalho criado em $DESKTOP_DIR"
echo ""
print_info "Arquivos de log: $HOME/.brx_ai_app.log"
print_info "Configurações: $HOME/.brx_ai/"
echo ""
print_info "Para desinstalar, execute: sudo $INSTALL_DIR/uninstall.sh"
echo ""
