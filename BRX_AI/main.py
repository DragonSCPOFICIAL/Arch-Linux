import json
import os
import sys
import platform
import subprocess
import requests
import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class BRXAgent:
    def __init__(self):
        self.name = "BRX AI (PROGRAMMER CORE)"
        self.version = "4.0.0-STABLE"
        self.model = "deepseek-coder:1.3b"
        self.api_url = "http://localhost:11434/api/generate"

    def log(self, message, type="INFO"):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        color = Colors.BLUE if type == "INFO" else Colors.GREEN
        if type == "AI": color = Colors.HEADER
        print(f"{Colors.BOLD}[{time}] {color}[{type}]{Colors.ENDC} {message}")

    def ask_ai(self, prompt):
        """Envia a pergunta para o modelo DeepSeek local."""
        self.log("Pensando...", "AI")
        payload = {
            "model": self.model,
            "prompt": f"Você é um especialista em Linux, Hardware e Programação. Ajude o usuário com: {prompt}",
            "stream": False
        }
        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", "Sem resposta do modelo.")
            return f"Erro na API: {response.status_code}"
        except Exception as e:
            return f"Erro de conexão: Certifique-se que o Ollama está rodando. ({str(e)})"

    def execute_shell(self, command):
        try:
            self.log(f"Executando: {command}", "SHELL")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)

    def greet(self):
        print(f"\n{Colors.HEADER}{Colors.BOLD}=== {self.name} ==={Colors.ENDC}")
        print(f"{Colors.BLUE}Motor:{Colors.ENDC} DeepSeek-Coder (Local)")
        print(f"{Colors.BLUE}Foco:{Colors.ENDC} Linux Kernel, Hardware & Nova Linguagem")
        print("-" * 45)

    def run(self):
        self.greet()
        while True:
            try:
                user_input = input(f"{Colors.BOLD}BRX_AI > {Colors.ENDC}")
                if not user_input: continue
                
                if user_input.lower().startswith("sh "):
                    print(self.execute_shell(user_input[3:]))
                elif user_input.lower() in ["sair", "exit"]:
                    break
                else:
                    # Qualquer outra entrada é tratada como uma pergunta de programação para a IA
                    response = self.ask_ai(user_input)
                    print(f"\n{Colors.GREEN}DeepSeek:{Colors.ENDC}\n{response}\n")
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    agent = BRXAgent()
    agent.run()
