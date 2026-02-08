#!/bin/bash

# Aether Launcher - Desinstalador Total e Definitivo
# Mantenedor: DragonSCPOFICIAL

APP_NAME="aetherlauncher"
INSTALL_DIR="/opt/$APP_NAME"
BIN_DIRS=("/usr/bin" "/usr/local/bin")
DESKTOP_DIRS=("/usr/share/applications" "$HOME/.local/share/applications")
CONFIG_DIR="$HOME/.config/aetherlauncher"
BASE_DATA_DIR="$HOME/.aetherlauncher"
LOG_FILE="$HOME/.aether_launcher.log"

echo "----------------------------------------"
echo "DESINSTALAÇÃO TOTAL: Aether Launcher"
echo "----------------------------------------"

# 0. Forçar encerramento de qualquer processo relacionado
echo "Encerrando processos..."
sudo pkill -9 -f "aetherlauncher" 2>/dev/null || true
sudo pkill -9 -f "AetherLauncher" 2>/dev/null || true

# 1. Remover Binários e Links Simbólicos
echo "Removendo executáveis..."
for dir in "${BIN_DIRS[@]}"; do
    sudo rm -f "$dir/$APP_NAME" 2>/dev/null || true
done

# 2. Remover Atalhos de Desktop
echo "Removendo atalhos..."
for dir in "${DESKTOP_DIRS[@]}"; do
    sudo rm -f "$dir/$APP_NAME.desktop" 2>/dev/null || true
done

# 3. Remover Diretório de Instalação (Sistema)
if [ -d "$INSTALL_DIR" ]; then
    echo "Removendo arquivos do sistema ($INSTALL_DIR)..."
    sudo rm -rf "$INSTALL_DIR" 2>/dev/null || true
fi

# 4. Remover TODOS os dados do usuário (Configurações, Logs e Minecraft)
echo "Removendo dados do usuário e do jogo..."
rm -rf "$CONFIG_DIR" 2>/dev/null || true
rm -rf "$BASE_DATA_DIR" 2>/dev/null || true
rm -f "$LOG_FILE" 2>/dev/null || true

# 5. Limpeza de Caches e Resíduos
echo "Limpando resíduos..."
sudo rm -f /var/crash/aetherlauncher* 2>/dev/null || true

echo "----------------------------------------"
echo "DESINSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "----------------------------------------"
echo "O sistema está limpo de qualquer rastro do Aether Launcher."
