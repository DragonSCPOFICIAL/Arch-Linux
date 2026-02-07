#!/bin/bash

# BRX_AI_App - Instalador de Agente Autônomo para Arch Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="brx_ai_app"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"

echo "--- Iniciando Instalação do Agente BRX AI (Arch Linux Edition) ---"

# 1. Verificar se é Arch Linux
if [ ! -f /etc/arch-release ]; then
    echo "AVISO: Este instalador foi otimizado para Arch Linux."
fi

# 2. Criar diretórios
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/src"

# 3. Copiar arquivos
sudo cp -r ./* "$INSTALL_DIR/"

# 4. Instalar dependências via pacman (Sistema e Bibliotecas de Automação)
echo "Instalando dependências do sistema e ferramentas de automação..."
sudo pacman -S --noconfirm python tk python-pillow python-requests python-pip xdotool scrot

# 5. Instalar dependências Python para Visão e Controle
echo "Configurando bibliotecas de visão e controle..."
sudo pip install pyautogui --break-system-packages

# 6. Criar link simbólico
sudo ln -sf "$INSTALL_DIR/BRX_AI_App.sh" "$BIN_DIR/$APP_NAME"
sudo chmod +x "$INSTALL_DIR/BRX_AI_App.sh"
sudo chmod +x "$INSTALL_DIR/uninstall.sh"

# 7. Criar atalho no menu
cat <<EOF | sudo tee "$DESKTOP_DIR/$APP_NAME.desktop"
[Desktop Entry]
Name=BRX AI Agent
Comment=Agente de IA Autônomo com Visão e Controle para Arch Linux
Exec=$APP_NAME
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Utility;AI;Development;Automation;
Keywords=AI;BRX;Arch;Automation;Vision;
EOF

echo "--- Instalação Concluída! ---"
echo "O Agente BRX AI está pronto para interagir com seu ambiente."
echo "Execute '$APP_NAME' para iniciar o comando em tempo real."
