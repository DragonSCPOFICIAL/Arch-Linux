#!/bin/bash

# BRX AI App - Script de Inicialização
# Gerencia a execução da inteligência artificial BRX

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
APP_NAME="brx_ai_app"
LOG_FILE="$HOME/.brx_ai_app.log"
BASE_DIR="/opt/brx_ai_app"

# Verificar se está rodando do diretório de desenvolvimento
if [ ! -d "$BASE_DIR" ]; then
    BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
fi

# ============================================================================
# LOGGING
# ============================================================================
{
    echo "--- BRX AI App Iniciado em $(date) ---"
    echo "Base Directory: $BASE_DIR"
} >> "$LOG_FILE" 2>&1

# ============================================================================
# VERIFICAÇÕES
# ============================================================================
if [ ! -f "$BASE_DIR/src/main.py" ]; then
    echo "ERRO: src/main.py não encontrado em $BASE_DIR" | tee -a "$LOG_FILE"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não está instalado" | tee -a "$LOG_FILE"
    exit 1
fi

# ============================================================================
# INICIAR APLICAÇÃO
# ============================================================================
cd "$BASE_DIR" || exit 1

# Redirecionar output para log
exec 2>>"$LOG_FILE"

# Executar a aplicação
python3 "$BASE_DIR/src/main.py"

# Capturar código de saída
EXIT_CODE=$?

# Registrar saída
echo "--- BRX AI App Finalizado com código: $EXIT_CODE em $(date) ---" >> "$LOG_FILE"

exit $EXIT_CODE
