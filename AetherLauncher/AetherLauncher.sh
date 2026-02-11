#!/bin/bash

# Aether Launcher - Script Principal
# Gerencia a interface e a execução do Minecraft

LOG_FILE="$HOME/.aether_launcher.log"
echo "Aether Launcher Iniciado em $(date)" > "$LOG_FILE"
exec 2>>"$LOG_FILE"

BASE_DIR="/opt/aetherlauncher"
[ ! -d "$BASE_DIR" ] && BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$BASE_DIR" || exit 1

# Verificar se a interface existe
if [ ! -f "$BASE_DIR/src/main.py" ]; then
    echo "ERRO: src/main.py não encontrado!" | tee -a "$LOG_FILE"
    exit 1
fi

# Otimizações de Performance para o Launcher
export MESA_GL_VERSION_OVERRIDE=4.6
export MESA_GLSL_VERSION_OVERRIDE=460
export vblank_mode=0

# Iniciar a Interface com prioridade normal (o Minecraft será iniciado com prioridade alta pelo Python)
echo "Lançando interface..." | tee -a "$LOG_FILE"
python3 "$BASE_DIR/AetherLauncher.py" "$@" 2>>"$LOG_FILE"

if [ $? -ne 0 ]; then
    echo "A interface fechou com erro. Verifique $LOG_FILE para detalhes."
    # Se falhar, tenta um modo de segurança sem aceleração para a UI
    if [[ "$*" != *"--safe-mode"* ]]; then
        echo "Tentando modo de segurança..."
        LIBGL_ALWAYS_SOFTWARE=1 python3 "$BASE_DIR/AetherLauncher.py" --safe-mode 2>>"$LOG_FILE"
