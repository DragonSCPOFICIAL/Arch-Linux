#!/bin/bash

# Aether Launcher - Instalador Nativo para Linux
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIR="/usr/bin"
DESKTOP_DIR="/usr/share/applications"

echo "==============================================="
echo "   Iniciando Instalação do Aether Launcher"
echo "==============================================="

# 1. Criar diretórios
echo "[1/5] Criando diretórios do sistema..."
sudo mkdir -p "$INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR/src"

# 2. Copiar arquivos
echo "[2/5] Copiando arquivos do launcher..."
sudo cp -r ./* "$INSTALL_DIR/"

# 3. Instalar dependências
echo "[3/5] Verificando dependências do sistema e Python..."
if command -v pacman &> /dev/null; then
    # Arch Linux
    sudo pacman -S --noconfirm python-pillow python-requests python-pip python-tk jre17-openjdk
elif command -v apt &> /dev/null; then
    # Debian/Ubuntu
    sudo apt update && sudo apt install -y python3-pil python3-requests python3-pip python3-tk openjdk-17-jre
else
    echo "Aviso: Gerenciador de pacotes não reconhecido. Certifique-se de ter Python3, Tkinter e Java 17 instalados."
fi

# Instalar bibliotecas Python necessárias
sudo pip3 install minecraft-launcher-lib Pillow requests --break-system-packages --quiet
    # Garantir que minecraft-launcher-lib esteja acessível
    python3 -m pip install minecraft-launcher-lib --break-system-packages --quiet

# 4. Configurar Executável
echo "[4/5] Configurando permissões e links..."
sudo chmod +x "$INSTALL_DIR/AetherLauncher.sh"
sudo ln -sf "$INSTALL_DIR/AetherLauncher.sh" "$BIN_DIR/$APP_NAME"

# 5. Criar atalho no menu
echo "[5/5] Criando atalho no menu de aplicativos..."
cat <<EOF | sudo tee "$DESKTOP_DIR/$APP_NAME.desktop" > /dev/null
[Desktop Entry]
Name=Aether Launcher
Comment=Minecraft Launcher Nativo Elite para Linux
Exec=$APP_NAME
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Game;
EOF

echo "==============================================="
echo "        Instalação Concluída com Sucesso!"
echo "==============================================="
echo "Você pode abrir o launcher digitando '$APP_NAME' ou pelo menu."
