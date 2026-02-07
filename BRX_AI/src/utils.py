"""
BRX AI - Funções Utilitárias
Logging, formatação, e funções auxiliares gerais
"""

import logging
import json
import os
from datetime import datetime
import psutil
import sys

# Importar configurações
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOG_FILE, LOG_DIR, SYSTEM_CONFIG

# ============================================================================
# CONFIGURAÇÃO DE LOGGING
# ============================================================================
def setup_logger(name=__name__):
    """Configura o logger para o aplicativo"""
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, SYSTEM_CONFIG["log_level"]))
    
    # Handler para arquivo
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger("BRX_AI")

# ============================================================================
# FUNÇÕES DE FORMATAÇÃO
# ============================================================================
def format_timestamp(dt=None):
    """Formata timestamp para exibição"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%H:%M:%S")

def format_date(dt=None):
    """Formata data para exibição"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%d/%m/%Y")

def format_message(sender, message, timestamp=True):
    """Formata mensagem para exibição no chat"""
    time_str = format_timestamp() if timestamp else ""
    return f"[{time_str}] {sender}: {message}" if timestamp else f"{sender}: {message}"

# ============================================================================
# FUNÇÕES DE SISTEMA
# ============================================================================
def get_system_info():
    """Obtém informações do sistema"""
    try:
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total / (1024**3),  # GB
            "memory_available": psutil.virtual_memory().available / (1024**3),  # GB
        }
    except Exception as e:
        logger.error(f"Erro ao obter informações do sistema: {e}")
        return {}

def get_cpu_usage():
    """Obtém uso de CPU em porcentagem"""
    try:
        return psutil.cpu_percent(interval=1)
    except Exception as e:
        logger.error(f"Erro ao obter uso de CPU: {e}")
        return 0

def get_memory_usage():
    """Obtém uso de memória em porcentagem"""
    try:
        return psutil.virtual_memory().percent
    except Exception as e:
        logger.error(f"Erro ao obter uso de memória: {e}")
        return 0

def get_disk_usage():
    """Obtém uso de disco em porcentagem"""
    try:
        return psutil.disk_usage('/').percent
    except Exception as e:
        logger.error(f"Erro ao obter uso de disco: {e}")
        return 0

def check_system_health():
    """Verifica a saúde do sistema"""
    cpu = get_cpu_usage()
    memory = get_memory_usage()
    
    health = {
        "status": "OK",
        "warnings": [],
        "cpu": cpu,
        "memory": memory,
    }
    
    if cpu > SYSTEM_CONFIG["max_cpu_usage"]:
        health["status"] = "WARNING"
        health["warnings"].append(f"CPU acima do limite: {cpu}%")
    
    if memory > SYSTEM_CONFIG["max_memory_usage"]:
        health["status"] = "WARNING"
        health["warnings"].append(f"Memória acima do limite: {memory}%")
    
    return health

# ============================================================================
# FUNÇÕES DE ARQUIVO
# ============================================================================
def load_json(filepath):
    """Carrega arquivo JSON"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logger.error(f"Erro ao carregar JSON {filepath}: {e}")
        return {}

def save_json(filepath, data):
    """Salva arquivo JSON"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao salvar JSON {filepath}: {e}")
        return False

# ============================================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================================
def is_valid_command(command):
    """Valida se um comando é válido"""
    if not command or not isinstance(command, str):
        return False
    return len(command.strip()) > 0

def sanitize_input(user_input):
    """Sanitiza entrada do usuário"""
    if not isinstance(user_input, str):
        return ""
    return user_input.strip()

# ============================================================================
# FUNÇÕES DE CONVERSÃO
# ============================================================================
def bytes_to_gb(bytes_value):
    """Converte bytes para GB"""
    return round(bytes_value / (1024**3), 2)

def bytes_to_mb(bytes_value):
    """Converte bytes para MB"""
    return round(bytes_value / (1024**2), 2)

def seconds_to_time_string(seconds):
    """Converte segundos para formato HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
