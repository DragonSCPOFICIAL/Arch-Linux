import os
import torch
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
from brain_core.intent_map import BRXIntentMapper

class BRXAgentBrain:
    """
    O 'Cérebro' do Agente BRX. 
    Focado em transformar intenções em ações técnicas usando DeepSeek-Coder.
    """
    def __init__(self, model_path="./models/deepseek-coder"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.is_loaded = False
        self.intent_mapper = BRXIntentMapper()
        
        # Carregar parâmetros locais do brain_core
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "brain_core/params/agent_config.json")
        try:
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {"llm_params": {"temperature": 0.1, "max_new_tokens": 256}}

        self.system_prompts = {
            "reasoning": self.config.get("system_identity", "Você é o BRX AI Agent.") + " Analise e decomponha em passos lógicos.",
            "code_gen": "Gere apenas o comando shell ou script Python necessário. Sem explicações.",
            "analysis": "Analise o log/erro e identifique a causa e solução."
        }

    def load(self):
        """Carrega o modelo da memória local"""
        if not os.path.exists(self.model_path):
            return False, f"Modelo não encontrado em {self.model_path}."
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            self.is_loaded = True
            return True, "Cérebro do Agente carregado."
        except Exception as e:
            return False, f"Erro ao carregar o cérebro: {str(e)}"

    def think(self, user_input, task_type="reasoning"):
        """
        Executa um processo de pensamento específico baseado no tipo de tarefa.
        Evita diálogos aleatórios.
        """
        if not self.is_loaded:
            return "Erro: Cérebro não carregado."
        
        prompt_template = self.system_prompts.get(task_type, self.system_prompts["reasoning"])
        full_prompt = f"### System: {prompt_template}\n### User: {user_input}\n### Response:"
        
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        
        # Configuração para geração técnica curta e precisa
        outputs = self.model.generate(
            **inputs, 
            max_new_tokens=256,
            temperature=0.2, # Baixa temperatura para mais precisão e menos 'conversa'
            top_p=0.9,
            do_sample=True
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extrair apenas a parte da resposta após o marcador
        if "### Response:" in response:
            return response.split("### Response:")[-1].strip()
        return response
