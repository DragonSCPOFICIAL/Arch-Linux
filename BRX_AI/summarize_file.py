import sys

def summarize_file(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Para arquivos de código, podemos tentar extrair funções, classes, etc.
        # Para outros arquivos, um resumo simples das primeiras e últimas linhas pode ser suficiente.
        
        lines = content.split('\n')
        if len(lines) > 20: # Se o arquivo for muito grande, resumir
            summary = "Primeiras 10 linhas:\n"
            summary += "\n".join(lines[:10])
            summary += "\n\nÚltimas 10 linhas:\n"
            summary += "\n".join(lines[-10:])
            summary += f"\n\n(Arquivo contém {len(lines)} linhas no total)"
        else:
            summary = content # Arquivos pequenos, mostrar tudo
            
        return summary
    except Exception as e:
        return f"Erro ao resumir arquivo {filepath}: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        print(summarize_file(filepath))
    else:
        print("Uso: python3 summarize_file.py <filepath>")
