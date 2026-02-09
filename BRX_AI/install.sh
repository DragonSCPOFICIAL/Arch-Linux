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
log_info "Iniciando instalação do BRX AI..."

# 1. Criar e ativar ambiente virtual Python
log_info "Criando ambiente virtual Python em $VENV_DIR..."
python3 -m venv "$VENV_DIR" || log_error "Falha ao criar ambiente virtual."
source "$VENV_DIR/bin/activate" || log_error "Falha ao ativar ambiente virtual."
log_success "Ambiente virtual criado e ativado."

# 2. Instalar dependências Python
log_info "Instalando dependências Python (torch, transformers, requests)..."
pip install torch transformers requests || log_error "Falha ao instalar dependências Python."
log_success "Dependências Python instaladas."

# 3. Criar estrutura de diretórios para o agent_config.json se não existir
log_info "Verificando e criando estrutura de diretórios para o agent_config.json..."
mkdir -p "$AGENT_CONFIG_DIR" || log_error "Falha ao criar diretório para agent_config.json."

# 4. Criar agent_config.json se não existir
if [ ! -f "$AGENT_CONFIG_FILE" ]; then
    log_info "Criando agent_config.json inicial..."
    echo 
    "{
    "agent_identity": {
        "version": "1.0.0-CORE",
        "specialization": ["Base System Agent"]
    },
    "technical_parameters": [],
    "logging_and_telemetry": {
        "last_evolution": "",
        "evolution_status": "Initialized"
    }
}" > "$AGENT_CONFIG_FILE" || log_error "Falha ao criar agent_config.json."
    log_success "agent_config.json inicial criado."
else
    log_info "agent_config.json já existe. Pulando criação inicial."
fi

# 5. Tornar o main.py executável e criar link simbólico
log_info "Tornando main.py executável e criando link simbólico para '$BRX_AI_COMMAND'..."
chmod +x "$AGENT_MAIN_SCRIPT" || log_error "Falha ao tornar main.py executável."

# Remover link simbólico antigo se existir
if [ -L "$BRX_AI_COMMAND" ]; then
    sudo rm "$BRX_AI_COMMAND" || log_error "Falha ao remover link simbólico antigo."
fi

# Criar novo link simbólico
sudo ln -s "$AGENT_MAIN_SCRIPT" "$BRX_AI_COMMAND" || log_error "Falha ao criar link simbólico."
log_success "Comando 'brx-ai' configurado globalmente."

# 6. Desativar ambiente virtual
deactivate

log_success "Instalação do BRX AI concluída com sucesso!"
log_info "Para iniciar o agente, digite: brx-ai"
log_info "Para rodar o motor de evolução, navegue até a pasta do BRX_AI e execute o script brx_ai_mass_injector.py no seu Colab ou localmente."
