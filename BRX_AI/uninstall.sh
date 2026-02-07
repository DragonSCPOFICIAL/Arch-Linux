#!/bin/bash

# BRX_AI_App - Desinstalador para Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="brx_ai_app"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"

echo "--- Iniciando Desinstalação do BRX_AI_App ---"

# 1. Remover atalho do menu
sudo rm -f "$DESKTOP_DIR/$APP_NAME.desktop"

# 2. Remover link simbólico
sudo rm -f "$BIN_DIR/$APP_NAME"

# 3. Remover diretório de instalação
sudo rm -rf "$INSTALL_DIR"

echo "--- Desinstalação Concluída! ---"
