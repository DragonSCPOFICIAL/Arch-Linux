import json
import os
import sys

class BRXAgent:
    def __init__(self, config_path="./brain_core/params/agent_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.name = "BRX AI"
        self.version = self.config.get("agent_identity", {}).get("version", "1.0.0")
        self.specializations = self.config.get("agent_identity", {}).get("specialization", [])
        self.technical_parameters = self.config.get("technical_parameters", [])

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"[ERRO] Arquivo de configuração não encontrado: {self.config_path}")
            print("Por favor, execute o motor de evolução para gerar o agent_config.json.")
            sys.exit(1)
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def greet(self):
        print(f"Olá! Eu sou o {self.name}, versão {self.version}.")
        print(f"Minhas especializações atuais incluem: {', '.join(self.specializations) if self.specializations else 'nenhuma'}.")
        print("Como posso ajudar hoje?")

    def process_command(self, command):
        command = command.lower().strip()

        if "status" in command or "versao" in command:
            return f"Eu sou o {self.name}, versão {self.version}. Estou operando com {len(self.technical_parameters)} conjuntos de parâmetros técnicos." 
        elif "especializacoes" in command or "habilidades" in command:
            if self.specializations:
                return f"Minhas especializações são: {', '.join(self.specializations)}."
            else:
                return "Ainda estou aprendendo novas especializações."
        elif "deepseek" in command or "parametros" in command:
            if self.technical_parameters:
                latest_params = self.technical_parameters[-1].get("data", {})
                deepseek_info = latest_params.get("architecture_feature", "N/A")
                lang_opt = latest_params.get("language_optimization", "N/A")
                kernel_opt = latest_params.get("kernel_optimization", "N/A")
                return f"Meus parâmetros DeepSeek mais recentes incluem: {deepseek_info}. Também estou otimizado para {lang_opt} e {kernel_opt}."
            else:
                return "Ainda não recebi parâmetros técnicos do DeepSeek."
        elif "ajuda" in command or "comandos" in command:
            return "Você pode me perguntar sobre 'status', 'versao', 'especializacoes', 'deepseek', 'parametros' ou 'sair'."
        elif "sair" in command or "tchau" in command:
            return "Até logo! Continue evoluindo o BRX AI."
        else:
            return "Não entendi seu comando. Tente 'ajuda' para ver as opções."

    def run(self):
        self.greet()
        while True:
            try:
                user_input = input("Você: ")
                if user_input.lower().strip() in ["sair", "tchau", "exit"]:
                    print(self.process_command(user_input))
                    break
                response = self.process_command(user_input)
                print(f"{self.name}: {response}")
            except KeyboardInterrupt:
                print("\nDesligando o agente BRX AI.")
                break

if __name__ == "__main__":
    agent = BRXAgent()
    agent.run()
