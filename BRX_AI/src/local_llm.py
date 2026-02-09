import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

class LocalDeepSeekCoder:
    def __init__(self, model_path="./models/deepseek-coder"):
        self.model_path = model_path
        self.tokenizer = None
        self.model = None
        self.is_loaded = False

    def load(self):
        """Carrega o modelo da memória local"""
        if not os.path.exists(self.model_path):
            return False, f"Modelo não encontrado em {self.model_path}. Execute download_model.py primeiro."
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, trust_remote_code=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            self.is_loaded = True
            return True, "Modelo carregado com sucesso."
        except Exception as e:
            return False, f"Erro ao carregar o modelo: {str(e)}"

    def generate(self, prompt, max_new_tokens=512):
        if not self.is_loaded:
            return "Erro: Modelo não carregado."
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
