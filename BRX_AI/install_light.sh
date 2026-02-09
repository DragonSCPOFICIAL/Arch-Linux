#!/bin/bash

# --- Configurações --- 
AGENT_DIR="$(dirname "$(readlink -f "$0")")"
VENV_DIR="$AGENT_DIR/.venv"
AGENT_MAIN_SCRIPT="$AGENT_DIR/main.py"
AGENT_CONFIG_DIR="$AGENT_DIR/brain_core/params"
AGENT_CONFIG_FILE="$AGENT_CONFIG_DIR/agent_config.json"
BRX_AI_COMMAND="/usr/local/bin/brx-ai"

# --- Funções Auxiliares ---
log_info() { echo -e "\e[1;34m[INFO]\e[0m $1"; }
log_success() { echo -e "\e[1;32m[SUCESSO]\e[0m $1"; }
log_error() { echo -e "\e[1;31m[ERRO]\e[0m $1"; exit 1; }

# --- Início da Instalação ---
log_info "Iniciando instalação ULTRA-LEVE do BRX AI..."

# 1. Limpar ambiente antigo se existir
if [ -d "$VENV_DIR" ]; then
    log_info "Removendo ambiente virtual antigo para liberar espaço..."
    rm -rf "$VENV_DIR"
fi

# 2. Criar ambiente virtual Python
log_info "Criando ambiente virtual Python..."
python3 -m venv "$VENV_DIR" || log_error "Falha ao criar ambiente virtual."
source "$VENV_DIR/bin/activate" || log_error "Falha ao ativar ambiente virtual."

# 3. Instalar apenas dependências leves
log_info "Instalando dependências leves (requests)..."
pip install requests || log_error "Falha ao instalar dependências."
log_success "Dependências instaladas."

# 4. Configurar arquivos de dados
mkdir -p "$AGENT_CONFIG_DIR"
if [ ! -f "$AGENT_CONFIG_FILE" ]; then
    echo '{"agent_identity": {"version": "1.0.0-LIGHT", "specialization": ["Base System"]}, "technical_parameters": []}' > "$AGENT_CONFIG_FILE"
fi

# 5. Criar link simbólico
chmod +x "$AGENT_MAIN_SCRIPT"
if [ -L "$BRX_AI_COMMAND" ]; then sudo rm "$BRX_AI_COMMAND"; fi
sudo ln -s "$AGENT_MAIN_SCRIPT" "$BRX_AI_COMMAND"

log_success "Instalação concluída! Versão Ultra-Leve pronta."
log_info "Para iniciar, digite: brx-ai"
