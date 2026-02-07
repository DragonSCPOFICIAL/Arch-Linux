#!/bin/bash

# Aether Launcher - Instalador para Arch Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Iniciando Instalação do Aether Launcher para Arch Linux"

# 1. Verificar dependências do sistema
echo "Verificando dependências do sistema..."
sudo pacman -S --noconfirm python-pillow python-requests python-pip tk

# 2. Criar diretórios
echo "Criando diretórios de instalação..."
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/src"

# 3. Copiar arquivos
echo "Copiando arquivos..."
sudo cp -r ./* "$INSTALL_DIR/"

# 4. Instalar dependências Python via pip (se necessário)
echo "Instalando dependências Python..."
sudo pip3 install minecraft-launcher-lib --break-system-packages

# 5. Criar link simbólico
echo "Criando link simbólico..."
sudo ln -sf "$INSTALL_DIR/AetherLauncher.sh" "$BIN_DIR/$APP_NAME"
sudo chmod +x "$INSTALL_DIR/AetherLauncher.sh"
sudo chmod +x "$INSTALL_DIR/updater.py"
sudo chmod +x "$INSTALL_DIR/uninstall.sh"

# 6. Criar atalho no menu
echo "Criando atalho no menu..."
mkdir -p "$DESKTOP_DIR"
cat <<EOF > "$DESKTOP_DIR/$APP_NAME.desktop"
[Desktop Entry]
Name=Aether Launcher
Comment=Minecraft Launcher Elite para Arch Linux
Exec=$APP_NAME
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Game;
EOF

chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"

echo "Instalação Concluída!"
echo "Você pode abrir o launcher digitando '$APP_NAME' no terminal ou pelo menu de aplicativos."
