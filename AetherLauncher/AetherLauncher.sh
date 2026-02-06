#!/bin/bash

# Aether Launcher - Script Principal
# Gerencia a interface e a execução do Minecraft

LOG_FILE="$HOME/.aether_launcher.log"
echo "--- Aether Launcher Iniciado em $(date) ---" > "$LOG_FILE"
exec 2>>"$LOG_FILE"

BASE_DIR="/opt/aetherlauncher"
[ ! -d "$BASE_DIR" ] && BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$BASE_DIR" || exit 1

# Verificar se a interface existe
if [ ! -f "$BASE_DIR/src/main.py" ]; then
    echo "ERRO: src/main.py não encontrado!" | tee -a "$LOG_FILE"
    exit 1
fi

# Iniciar a Interface
python3 "$BASE_DIR/src/main.py"
