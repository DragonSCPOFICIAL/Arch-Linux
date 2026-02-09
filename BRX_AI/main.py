import json
import os
import sys
import platform
import subprocess
import requests
import datetime
import glob
import time

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
        repo_context = self.get_repo_context()
        payload = {
            "model": self.model,
            "prompt": f"Você é um especialista em Linux, Hardware e Programação. Ajude o usuário com: {prompt}\n\nContexto do Repositório:\n{repo_context}",
            "stream": False
        }

        try:
            response = requests.post(self.api_url, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json().get("response", "Sem resposta do modelo.")
            return f"Erro na API: {response.status_code}"
        except Exception as e:
            return f"Erro de conexão: Certifique-se que o Ollama está rodando. ({str(e)})"

    def read_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Erro ao ler arquivo: {str(e)}"

    def write_file(self, filepath, content):
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return f"Arquivo {filepath} escrito com sucesso."
        except Exception as e:
            return f"Erro ao escrever arquivo: {str(e)}"

    def git_command(self, command):
        try:
            self.log(f"Executando Git: {command}", "GIT")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Erro Git: {result.stderr}"
        except Exception as e:
            return f"Erro ao executar comando Git: {str(e)}"

    def setup_git_credentials(self):
        self.log("Configurando credenciais Git...", "INFO")
        try:
            # Configura o Git para usar o helper de credenciais do gh CLI
            self.execute_shell("git config --global credential.helper cache")
            self.execute_shell("git config --global user.email \"brx-ai@example.com\"") # Email genérico para o agente
            self.execute_shell("git config --global user.name \"BRX AI Agent\"") # Nome genérico para o agente
            self.log("Credenciais Git configuradas com sucesso.", "INFO")
        except Exception as e:
            self.log(f"Erro ao configurar credenciais Git: {str(e)}", "ERROR")

    def list_repo_files(self):
        self.log("Listando arquivos do repositório...", "INFO")
        try:
            # Usar glob para listar todos os arquivos no diretório atual e subdiretórios
            # Excluir o diretório .git para evitar listar arquivos internos do Git
            all_files = [f for f in glob.glob("**", recursive=True) if ".git" not in f and os.path.isfile(f)]
            return "\n".join(all_files)
        except Exception as e:
            return f"Erro ao listar arquivos do repositório: {str(e)}"

    def get_repo_context(self):
        self.log("Gerando contexto do repositório...", "INFO")
        context = ""
        # Adicionar o Guia de Evolução se ele existir
        if os.path.exists("ulx_evolution_guide.md"):
            with open("ulx_evolution_guide.md", "r") as f:
                context += f"Guia de Evolução ULX:\n{f.read()}\n\n"
        
        context += "Arquivos no repositório BRX_AI:\n"
        try:
            all_files = [f for f in glob.glob("**", recursive=True) if ".git" not in f and os.path.isfile(f)]
            for f in all_files:
                context += f"- {f}\n"
            
            # Adicionar contexto do repositório ULX se ele existir no mesmo nível de diretório
            ulx_path = "../ULX-Repo" # Ajuste conforme a estrutura local do usuário
            if os.path.exists(ulx_path):
                context += "\nRepositório de Referência (ULX):\n"
                ulx_files = [f for f in glob.glob(f"{ulx_path}/**", recursive=True) if ".git" not in f and os.path.isfile(f)]
                for f in ulx_files[:20]: # Limitar a 20 arquivos para não estourar o contexto
                    context += f"- {f}\n"
                if len(ulx_files) > 20:
                    context += f"... e mais {len(ulx_files) - 20} arquivos.\n"
            
            return context
        except Exception as e:
            return f"Erro ao gerar contexto do repositório: {str(e)}"

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

    def autonomous_run(self):
        self.log("Iniciando modo autônomo...", "AI")
        while True:
            self.log("Pensando na próxima ação para evoluir ULX...", "AI")
            # A IA decide a próxima ação com base no contexto do repositório e no objetivo de evoluir ULX
            ai_decision_prompt = "Com base no contexto do repositório e na sintaxe da linguagem ULX, qual é a próxima ação para evoluir a linguagem? Pense em termos de leitura, escrita, execução de shell ou comandos git. Responda com um comando BRX_AI (ex: read <file>, write <file> <content>, sh <command>, git <command>)."
            ai_response = self.ask_ai(ai_decision_prompt)
            self.log(f"Decisão da IA: {ai_response}", "AI")

            if ai_response.lower().startswith("sh "):
                print(self.execute_shell(ai_response[3:]))
            elif ai_response.lower().startswith("read "):
                print(self.read_file(ai_response[5:]))
            elif ai_response.lower().startswith("write "):
                parts = ai_response[6:].split(" ", 1)
                if len(parts) == 2:
                    filepath, content = parts
                    print(self.write_file(filepath, content))
                else:
                    self.log("Erro: Comando write mal formatado no modo autônomo.", "ERROR")
            elif ai_response.lower().startswith("git "):
                print(self.git_command(ai_response[4:]))
            elif ai_response.lower() == "exit" or ai_response.lower() == "sair":
                self.log("Modo autônomo encerrado pela IA.", "AI")
                break
            else:
                self.log(f"Comando da IA não reconhecido ou inválido: {ai_response}", "ERROR")
            
            # Pequena pausa para evitar loop infinito e dar tempo para o sistema
            time.sleep(5)


    def run(self):
        self.greet()
        self.setup_git_credentials()
        while True:
            try:
                user_input = input(f"{Colors.BOLD}BRX_AI > {Colors.ENDC}")
                if not user_input: continue
                
                if user_input.lower() == "autonomo":
                    self.autonomous_run()
                elif user_input.lower().startswith("sh "):
                    print(self.execute_shell(user_input[3:]))
                elif user_input.lower().startswith("read "):
                    print(self.read_file(user_input[5:]))
                elif user_input.lower().startswith("write "):
                    parts = user_input[6:].split(" ", 1)
                    if len(parts) == 2:
                        filepath, content = parts
                        print(self.write_file(filepath, content))
                    else:
                        print("Uso: write <filepath> <content>")
                elif user_input.lower() == "lsfiles":
                    print(self.list_repo_files())
                elif user_input.lower().startswith("summarize "):
                    filepath_to_summarize = user_input[10:]
                    summary_output = self.execute_shell(f"python3 summarize_file.py {filepath_to_summarize}")
                    print(summary_output)
                elif user_input.lower() == "context":
                    print(self.get_repo_context())
                elif user_input.lower().startswith("git "):
                    print(self.git_command(user_input[4:]))
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
