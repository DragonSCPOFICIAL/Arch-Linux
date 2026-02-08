#!/bin/bash

# Aether Launcher - Desinstalador Robusto para Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"
CONFIG_DIR="$HOME/.config/aetherlauncher"
BASE_DATA_DIR="$HOME/.aetherlauncher"
LOG_FILE="$HOME/.aether_launcher.log"
AUTO_CONFIRM=false

# Verificar flag --auto
if [[ "$1" == "--auto" ]]; then
    AUTO_CONFIRM=true
fi

echo "----------------------------------------"
echo "Desinstalando Aether Launcher"
echo "----------------------------------------"

# 0. Encerrar processos
echo "Encerrando processos ativos..."
pkill -f "aetherlauncher" || true
pkill -f "AetherLauncher/src/main.py" || true

# 1. Remover link simbólico
echo "Removendo links simbólicos..."
sudo rm -f "$BIN_DIR/$APP_NAME" || true
sudo rm -f "/usr/local/bin/$APP_NAME" || true

# 2. Remover atalho do menu
echo "Removendo atalho do menu..."
sudo rm -f "$DESKTOP_DIR/$APP_NAME.desktop" || true
rm -f "$HOME/.local/share/applications/$APP_NAME.desktop" || true

# 3. Remover diretório de instalação
echo "Removendo arquivos da aplicação em $INSTALL_DIR..."
sudo rm -rf "$INSTALL_DIR" || true

# 4. Remover dados do usuário
if [ "$AUTO_CONFIRM" = true ]; then
    echo "Removendo configurações e dados do jogo..."
    rm -rf "$CONFIG_DIR" || true
    rm -rf "$BASE_DATA_DIR" || true
    rm -f "$LOG_FILE" || true
else
    echo -e "\nAVISO: Os dados do Minecraft e configurações estão em $BASE_DATA_DIR"
    read -p "Deseja remover também as configurações, perfis e dados do Minecraft? (s/n): " choice
    if [[ "$choice" == "s" || "$choice" == "S" ]]; then
        echo "Removendo dados do usuário..."
        rm -rf "$CONFIG_DIR" || true
        rm -rf "$BASE_DATA_DIR" || true
        rm -f "$LOG_FILE" || true
        echo "Dados do usuário removidos com sucesso."
    else
        echo "Dados do usuário mantidos."
    fi
fi

# 5. Limpeza final
echo "Limpando caches..."
sudo rm -f /var/crash/aetherlauncher* 2>/dev/null || true

echo "----------------------------------------"
echo "Desinstalação Concluída!"
echo "----------------------------------------"
