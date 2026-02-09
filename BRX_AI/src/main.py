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
from src.local_llm import BRXAgentBrain
from src.agent_actions import BRXActionExecutor

# ============================================================================
# CLASSE DO ENGINE DE IA
# ============================================================================
class BRXAIEngine:
    """Motor do Agente BRX focado em ações e raciocínio técnico"""
    
    def __init__(self):
        """Inicializa o engine do agente"""
        self.logger = setup_logger("BRXAIEngine")
        self.brain = BRXAgentBrain()
        self.executor = BRXActionExecutor()
        self.model_loaded = False
        self.logger.info("BRX Agent Engine inicializado")
    
    def load_local_model(self):
        """Carrega o cérebro da IA"""
        success, message = self.brain.load()
        if success:
            self.model_loaded = True
        return success, message

    def handle_request(self, user_input):
        """
        Fluxo de Agente: 
        1. Pensar (Raciocínio)
        2. Agir (Execução se necessário)
        3. Reportar
        """
        if not self.model_loaded:
            return "Aguardando carregamento do modelo local para agir..."

        # 1. Fase de Pensamento
        self.logger.info(f"Agente pensando sobre: {user_input}")
        plan = self.brain.think(user_input, task_type="reasoning")
        
        # 2. Fase de Decisão de Código (se o plano envolver execução)
        if "comando" in plan.lower() or "executar" in plan.lower():
            code = self.brain.think(user_input, task_type="code_gen")
            # Aqui poderíamos pedir confirmação na UI antes de executar
            # success, output = self.executor.execute_shell(code)
            return f"Plano do Agente:\n{plan}\n\nCódigo Sugerido:\n{code}"
        
        return f"Raciocínio do Agente:\n{plan}"

    def process(self, user_input):
        """Interface compatível com a UI antiga"""
        return self.handle_request(user_input)

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
