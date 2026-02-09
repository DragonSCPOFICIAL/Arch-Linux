#!/bin/bash

# Cores para o terminal
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}=== BRX AI: Configuração do Motor de Programação ===${NC}"

# 1. Verificar e Instalar Ollama (Gerenciador de modelos ultra-leve)
if ! command -v ollama &> /dev/null; then
    echo -e "${YELLOW}[!] Ollama não encontrado. Instalando via script oficial...${NC}"
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo -e "${GREEN}[✓] Ollama já está instalado.${NC}"
fi

# 2. Iniciar o serviço do Ollama em segundo plano se não estiver rodando
if ! pgrep -x "ollama" > /dev/null; then
    echo -e "${YELLOW}[!] Iniciando serviço Ollama...${NC}"
    ollama serve > /dev/null 2>&1 &
    sleep 5
fi

# 3. Baixar o modelo DeepSeek-Coder (Versão 1.3B - Focada em Código e Hardware)
# Esta versão tem apenas ~800MB, mas é treinada especificamente para programação.
echo -e "${BLUE}[i] Baixando modelo DeepSeek-Coder (Otimizado para Programação)...${NC}"
ollama pull deepseek-coder:1.3b

echo -e "${GREEN}[✓] Motor de IA configurado com sucesso!${NC}"
echo -e "${BLUE}O BRX AI agora tem acesso ao cérebro do DeepSeek para criar sua linguagem.${NC}"

# 4. Configurar safe.directory para o Git
echo -e "${BLUE}[i] Configurando safe.directory para o repositório Git...${NC}"
git config --global --add safe.directory /home/ubuntu/Arch-Linux-Repo
echo -e "${GREEN}[✓] safe.directory configurado.${NC}"
