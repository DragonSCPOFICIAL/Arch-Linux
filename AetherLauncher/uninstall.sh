#!/bin/bash

# Aether Launcher - Desinstalador para Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"
CONFIG_DIR="$HOME/.config/aetherlauncher"
LOG_FILE="$HOME/.aether_launcher.log"

echo "Desinstalando Aether Launcher"

# 1. Remover link simbólico
sudo rm -f "$BIN_DIR/$APP_NAME"

# 2. Remover atalho do menu
sudo rm -f "$DESKTOP_DIR/$APP_NAME.desktop"

# 3. Remover diretório de instalação
sudo rm -rf "$INSTALL_DIR"

# 4. Perguntar sobre dados do usuário
read -p "Deseja remover também as configurações e perfis? (s/n): " choice
if [[ "$choice" == "s" || "$choice" == "S" ]]; then
    rm -rf "$CONFIG_DIR"
    rm -f "$LOG_FILE"
    echo "Configurações removidas."
fi

echo "Desinstalação Concluída!"
