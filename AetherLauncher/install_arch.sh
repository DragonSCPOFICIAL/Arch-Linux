#!/bin/bash

# Aether Launcher - Instalador para Arch Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/local/bin"
DESKTOP_DIR="/usr/share/applications"

echo "----------------------------------------"
echo "Iniciando Instalação do Aether Launcher"
echo "----------------------------------------"

# 1. Verificar dependências do sistema
echo "Verificando dependências do sistema..."
sudo pacman -S --noconfirm python-pillow python-requests python-pip tk 2>/dev/null || echo "Aviso: Falha ao instalar dependências via pacman. Certifique-se de que estão instaladas."

# 2. Preparar diretórios (limpeza se já existir)
if [ -d "$INSTALL_DIR" ]; then
    echo "Limpando instalação anterior em $INSTALL_DIR..."
    sudo rm -rf "$INSTALL_DIR"
fi

echo "Criando diretórios de instalação..."
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/src"

# 3. Copiar arquivos
echo "Copiando arquivos..."
sudo cp -r ./* "$INSTALL_DIR/"

# 4. Instalar dependências Python via pip
echo "Instalando dependências Python..."
sudo pip3 install minecraft-launcher-lib --break-system-packages 2>/dev/null || echo "Aviso: Falha ao instalar via pip. Verifique sua conexão."

# 5. Configurar permissões e links
echo "Configurando executáveis..."
sudo chmod +x "$INSTALL_DIR/AetherLauncher.sh"
sudo chmod +x "$INSTALL_DIR/updater.py"
sudo chmod +x "$INSTALL_DIR/uninstall.sh"

echo "Criando link simbólico em $BIN_DIR/$APP_NAME..."
sudo ln -sf "$INSTALL_DIR/AetherLauncher.sh" "$BIN_DIR/$APP_NAME"

# 6. Criar atalho no menu
echo "Criando atalho no menu..."
sudo mkdir -p "$DESKTOP_DIR"
cat <<EOF | sudo tee "$DESKTOP_DIR/$APP_NAME.desktop" > /dev/null
[Desktop Entry]
Name=Aether Launcher
Comment=Minecraft Launcher Elite para Arch Linux
Exec=$APP_NAME
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Game;
EOF
sudo chmod +x "$DESKTOP_DIR/$APP_NAME.desktop"

echo "----------------------------------------"
echo "Instalação Concluída com Sucesso!"
echo "----------------------------------------"
echo "Você pode abrir o launcher digitando '$APP_NAME' no terminal"
echo "ou procurando por 'Aether Launcher' no seu menu de aplicativos."
