import json
import re

class BRXIntentMapper:
    """
    Mapeia entradas do usuário diretamente para intenções de ação,
    reduzindo a necessidade de processamento pesado de LLM para tarefas comuns.
    """
    def __init__(self):
        self.patterns = {
            "terminal_exec": r"(execute|rode|comando|terminal|bash|sh)\s+(.*)",
            "file_manage": r"(crie|leia|edite|delete|arquivo|pasta)\s+(.*)",
            "system_status": r"(status|como está|memória|cpu|uso|hardware)",
            "update_system": r"(atualize|update|upgrade|pacman|system)",
            "app_launcher": r"(abra|inicie|lançe|app|aplicativo)\s+(.*)"
        }

    def identify(self, text):
        text = text.lower()
        for intent, pattern in self.patterns.items():
            match = re.search(pattern, text)
            if match:
                return {
                    "intent": intent,
                    "raw_match": match.group(0),
                    "params": match.groups() if len(match.groups()) > 0 else None
                }
        return {"intent": "complex_reasoning", "params": None}
