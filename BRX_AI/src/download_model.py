import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def download_deepseek_coder(model_name="deepseek-ai/deepseek-coder-1.3b-instruct", save_path="./models/deepseek-coder"):
    """
    Realiza o download e salva o modelo DeepSeek-Coder localmente.
    """
    print(f"Iniciando download do modelo: {model_name}")
    
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    print("Baixando tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.save_pretrained(save_path)
    
    print("Baixando modelo (isso pode demorar e requer bastante espaço/RAM)...")
    model = AutoModelForCausalLM.from_pretrained(
        model_name, 
        trust_remote_code=True, 
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    model.save_pretrained(save_path)
    
    print(f"Modelo salvo com sucesso em: {save_path}")

if __name__ == "__main__":
    # Nota: No ambiente sandbox do Manus, isso provavelmente falhará por timeout ou espaço.
    # O usuário deve executar isso em sua máquina local.
    download_deepseek_coder()
