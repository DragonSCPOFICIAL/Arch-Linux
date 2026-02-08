#!/bin/bash

# BRX_AI_App - Script Principal
# Gerencia a execução da inteligência artificial BRX

LOG_FILE="$HOME/.brx_ai_app.log"
echo "--- BRX_AI_App Iniciado em $(date) ---" > "$LOG_FILE"
exec 2>>"$LOG_FILE"

BASE_DIR="/opt/brx_ai_app"
[ ! -d "$BASE_DIR" ] && BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$BASE_DIR" || exit 1

# Verificar se a interface existe
if [ ! -f "$BASE_DIR/src/main.py" ]; then
    echo "ERRO: src/main.py não encontrado!" | tee -a "$LOG_FILE"
    exit 1
fi

# Iniciar a Inteligência Artificial
python3 "$BASE_DIR/src/main.py"
