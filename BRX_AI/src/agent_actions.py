import subprocess
import os
from utils import setup_logger

class BRXActionExecutor:
    """
    Executa as ações decididas pelo cérebro da IA no sistema Linux.
    """
    def __init__(self):
        self.logger = setup_logger("BRXActionExecutor")

    def execute_shell(self, command):
        """Executa um comando shell de forma segura"""
        try:
            self.logger.info(f"Executando comando: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)

    def manage_file(self, path, action="read", content=None):
        """Gerencia arquivos no sistema"""
        try:
            if action == "read":
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        return True, f.read()
                return False, "Arquivo não encontrado."
            elif action == "write":
                with open(path, 'w') as f:
                    f.write(content)
                return True, "Arquivo escrito com sucesso."
            return False, "Ação de arquivo desconhecida."
        except Exception as e:
            return False, str(e)
