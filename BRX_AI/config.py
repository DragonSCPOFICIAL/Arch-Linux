"""
BRX AI - Configurações Globais
Paleta de cores, constantes e configurações do sistema
"""

# ============================================================================
# INFORMAÇÕES DO APLICATIVO
# ============================================================================
APP_NAME = "BRX AI"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Agente de IA Autônomo com Visão e Controle para Linux"
AUTHOR = "DragonSCPOFICIAL"

# ============================================================================
# PALETA DE CORES - "MODO PRIME" (Inspirada no Manus)
# ============================================================================
COLORS = {
    # Fundos
    "bg_primary": "#0B0E14",        # Fundo principal (Deep Space)
    "bg_secondary": "#10141B",      # Fundo secundário (Sidebar)
    "bg_tertiary": "#161B22",       # Fundo de cards
    
    # Acentos
    "accent_primary": "#1793D1",    # Azul Arch (Links e botões)
    "accent_secondary": "#00E5FF",  # Cyan Neon (Destaques)
    
    # Estados
    "success": "#00FF9C",           # Verde Neon (Sucesso)
    "warning": "#FFD700",           # Amarelo (Avisos)
    "error": "#FF6B6B",             # Vermelho (Erros)
    "info": "#1793D1",              # Azul (Informações)
    
    # Texto
    "text_primary": "#E6EDF3",      # Texto principal
    "text_secondary": "#7D8590",    # Texto secundário
    "text_tertiary": "#484F58",     # Texto terciário
    
    # Bordas e divisores
    "border": "#30363D",            # Bordas
    "divider": "#21262D",           # Divisores
}

# ============================================================================
# DIMENSÕES DA JANELA
# ============================================================================
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# ============================================================================
# DIMENSÕES DOS COMPONENTES
# ============================================================================
SIDEBAR_WIDTH = 280
HEADER_HEIGHT = 60
FOOTER_HEIGHT = 50
CHAT_PADDING = 20
BORDER_RADIUS = 8

# ============================================================================
# TIPOGRAFIA
# ============================================================================
FONTS = {
    "title_large": ("Segoe UI", 24, "bold"),
    "title_medium": ("Segoe UI", 18, "bold"),
    "title_small": ("Segoe UI", 14, "bold"),
    
    "body_large": ("Segoe UI", 12, "normal"),
    "body_medium": ("Segoe UI", 11, "normal"),
    "body_small": ("Segoe UI", 10, "normal"),
    
    "mono_large": ("Courier New", 11, "normal"),
    "mono_medium": ("Courier New", 10, "normal"),
    "mono_small": ("Courier New", 9, "normal"),
    
    "label": ("Segoe UI", 9, "bold"),
    "button": ("Segoe UI", 10, "bold"),
}

# ============================================================================
# CONFIGURAÇÕES DE CHAT
# ============================================================================
CHAT_CONFIG = {
    "max_history": 500,             # Máximo de mensagens no histórico
    "auto_scroll": True,            # Auto-scroll ao receber mensagens
    "show_timestamps": True,        # Mostrar timestamps
    "show_sender": True,            # Mostrar nome do remetente
}

# ============================================================================
# CONFIGURAÇÕES DE SISTEMA
# ============================================================================
SYSTEM_CONFIG = {
    "check_interval": 2000,         # Intervalo de verificação do sistema (ms)
    "max_cpu_usage": 80,            # Limite de CPU (%)
    "max_memory_usage": 85,         # Limite de memória (%)
    "log_level": "INFO",            # Nível de log
}

# ============================================================================
# CAMINHOS PADRÃO
# ============================================================================
import os
HOME_DIR = os.path.expanduser("~")
CONFIG_DIR = os.path.join(HOME_DIR, ".brx_ai")
LOG_DIR = os.path.join(CONFIG_DIR, "logs")
DATA_DIR = os.path.join(CONFIG_DIR, "data")
CACHE_DIR = os.path.join(CONFIG_DIR, "cache")

# Criar diretórios se não existirem
for directory in [CONFIG_DIR, LOG_DIR, DATA_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "brx_ai.log")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
HISTORY_FILE = os.path.join(DATA_DIR, "chat_history.json")

# ============================================================================
# MENSAGENS DO SISTEMA
# ============================================================================
SYSTEM_MESSAGES = {
    "welcome": "Bem-vindo ao BRX AI! Sou seu agente autônomo para Linux.",
    "ready": "Pronto para receber comandos.",
    "processing": "Processando sua solicitação...",
    "error": "Ocorreu um erro ao processar sua solicitação.",
    "success": "Operação concluída com sucesso!",
}

# ============================================================================
# ATALHOS DE TECLADO
# ============================================================================
KEYBOARD_SHORTCUTS = {
    "send_message": "<Return>",
    "new_line": "<Shift-Return>",
    "clear_chat": "<Control-l>",
    "focus_input": "<Control-i>",
}
