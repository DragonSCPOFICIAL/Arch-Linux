import os
import json
import subprocess
from utils import setup_logger

class BRXSelfExpansion:
    """
    Módulo responsável pela auto-evolução do BRX AI.
    Analisa o repositório, identifica melhorias e realiza commits automáticos.
    """
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.logger = setup_logger("BRXSelfExpansion")
        self.config_path = os.path.join(repo_path, "brain_core/params/agent_config.json")
        
    def load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def analyze_repository(self):
        """Analisa a estrutura para encontrar arquivos da nova linguagem ou melhorias no core"""
        self.logger.info("Iniciando análise de auto-expansão...")
        # Lógica para escanear a pasta knowledge_base e src
        files = []
        for root, dirs, filenames in os.walk(self.repo_path):
            for f in filenames:
                if f.endswith(('.py', '.md', '.json')):
                    files.append(os.path.join(root, f))
        return files

    def suggest_improvements(self, brain):
        """Usa o cérebro da IA para sugerir melhorias no próprio código"""
        config = self.load_config()
        if not config["action_thresholds"]["self_expansion_enabled"]:
            return "Auto-expansão desativada nas configurações."

        self.logger.info("Solicitando sugestões de melhoria ao cérebro...")
        # Aqui o agente leria seu próprio código e proporia mudanças
        return "Análise concluída. Pronto para expandir a sintaxe da nova linguagem."

    def auto_commit(self, message):
        """Realiza o push automático das melhorias para o GitHub"""
        try:
            os.chdir(self.repo_path)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"[BRX-AI Auto-Expansion] {message}"], check=True)
            subprocess.run(["git", "push"], check=True)
            self.logger.info(f"Auto-commit realizado: {message}")
            return True
        except Exception as e:
            self.logger.error(f"Erro no auto-commit: {str(e)}")
            return False
