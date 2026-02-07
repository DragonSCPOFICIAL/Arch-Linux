#!/bin/bash

# Aether Launcher - Instalador para Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Iniciando Instalação do Aether Launcher"

# 1. Criar diretórios
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/src"

# 2. Copiar arquivos
sudo cp -r ./* "$INSTALL_DIR/"

# 3. Instalar dependências do sistema e Python
echo "Verificando dependências..."
if command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -S --noconfirm python-pillow python-requests python-pip tk
elif command -v apt &> /dev/null; then
    # Debian/Ubuntu
    sudo apt update && sudo apt install -y python3-pil python3-requests python3-pip python3-tk
else
    echo "Gerenciador de pacotes não suportado. Instale as dependências manualmente."
fi

sudo pip3 install minecraft-launcher-lib --break-system-packages

# 4. Criar link simbólico
sudo ln -sf "$INSTALL_DIR/AetherLauncher.sh" "$BIN_DIR/$APP_NAME"
sudo chmod +x "$INSTALL_DIR/AetherLauncher.sh"
sudo chmod +x "$INSTALL_DIR/updater.py"
sudo chmod +x "$INSTALL_DIR/uninstall.sh"

# 5. Criar atalho no menu
cat <<EOF | sudo tee "$DESKTOP_DIR/$APP_NAME.desktop" > /dev/null
[Desktop Entry]
Name=Aether Launcher
Comment=Minecraft Launcher Elite para Linux
Exec=$APP_NAME
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Game;
EOF

echo "Instalação Concluída!"
echo "Você pode abrir o launcher digitando '$APP_NAME' no terminal ou pelo menu de aplicativos."
