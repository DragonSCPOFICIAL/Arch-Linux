#!/usr/bin/env python3
"""
BRX AI - Núcleo Principal
Agente autônomo de IA para Linux com interface nativa
"""

import tkinter as tk
import sys
import os
import signal

# Importar configurações, utilidades e interface
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from utils import logger, setup_logger
from ui import create_interface
from src.local_llm import LocalDeepSeekCoder

# ============================================================================
# CLASSE DO ENGINE DE IA
# ============================================================================
class BRXAIEngine:
    """Motor principal da IA com suporte a modelo local DeepSeek-Coder"""
    
    def __init__(self):
        """Inicializa o engine de IA"""
        self.logger = setup_logger("BRXAIEngine")
        self.local_llm = LocalDeepSeekCoder()
        self.model_loaded = False
        self.logger.info("BRX AI Engine inicializado")
    
    def load_local_model(self):
        """Tenta carregar o modelo local"""
        success, message = self.local_llm.load()
        if success:
            self.model_loaded = True
            self.logger.info("DeepSeek-Coder carregado localmente.")
        else:
            self.logger.warning(f"Falha ao carregar modelo local: {message}")
        return success, message

    def process(self, user_input):
        """Processa entrada do usuário"""
        self.logger.info(f"Processando: {user_input}")
        
        if self.model_loaded:
            try:
                response = self.local_llm.generate(user_input)
                return response
            except Exception as e:
                self.logger.error(f"Erro na geração local: {e}")
                return f"Erro ao gerar resposta local: {e}"
        
        return f"BRX AI (Modo Offline/Simulação): Recebi sua mensagem: '{user_input}'. O modelo local DeepSeek-Coder não está carregado."

# ============================================================================
# CLASSE PRINCIPAL DO APLICATIVO
# ============================================================================
class BRXAIApp:
    """Aplicativo principal do BRX AI"""
    
    def __init__(self):
        """Inicializa o aplicativo"""
        self.logger = setup_logger("BRXAIApp")
        self.logger.info(f"Iniciando {APP_NAME} v{APP_VERSION}")
        
        # Criar engine de IA
        self.ai_engine = BRXAIEngine()
        
        # Criar janela principal
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurar sinais
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Criar interface
        self.ui = create_interface(self.root, self.ai_engine)
        
        self.logger.info("Aplicativo iniciado com sucesso")
    
    def signal_handler(self, signum, frame):
        """Manipula sinais do sistema"""
        self.logger.info(f"Sinal {signum} recebido. Encerrando...")
        self.on_closing()
    
    def on_closing(self):
        """Manipula fechamento da janela"""
        self.logger.info("Encerrando BRX AI")
        self.root.quit()
        self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Executa o aplicativo"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Erro durante execução: {e}", exc_info=True)
            sys.exit(1)

# ============================================================================
# PONTO DE ENTRADA
# ============================================================================
def main():
    """Função principal"""
    try:
        app = BRXAIApp()
        app.run()
    except Exception as e:
        logger.error(f"Erro fatal: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
