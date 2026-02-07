# Guia de Desenvolvimento - BRX AI

Este documento fornece instruções para desenvolvedores que desejam contribuir ou estender o BRX AI.

## Configuração do Ambiente de Desenvolvimento

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/brx_ai_improved.git
cd brx_ai_improved
```

### 2. Instale Dependências

```bash
# Dependências do sistema
sudo pacman -S python tk python-pillow python-requests python-pip  # Arch
# ou
sudo apt install python3 python3-tk python3-pil python3-requests python3-pip  # Debian/Ubuntu

# Dependências Python
pip3 install -r requirements.txt
```

### 3. Execute em Modo Desenvolvimento

```bash
python3 src/main.py
```

## Estrutura do Código

### Convenções de Nomenclatura

- **Classes**: `PascalCase` (ex: `BRXAIInterface`)
- **Funções**: `snake_case` (ex: `show_chat_page`)
- **Constantes**: `UPPER_CASE` (ex: `WINDOW_WIDTH`)
- **Variáveis privadas**: `_snake_case` (ex: `_is_processing`)

### Estilo de Código

Seguimos as convenções PEP 8:

```python
# Bom
def calculate_cpu_usage():
    """Calcula o uso de CPU"""
    return psutil.cpu_percent(interval=1)

# Ruim
def calc_cpu():
    return psutil.cpu_percent(interval=1)
```

### Documentação

Todas as funções devem ter docstrings:

```python
def process_message(self, message):
    """
    Processa uma mensagem do usuário.
    
    Args:
        message (str): Mensagem do usuário
        
    Returns:
        str: Resposta da IA
        
    Raises:
        ValueError: Se a mensagem estiver vazia
    """
    pass
```

## Adicionando Novas Funcionalidades

### 1. Adicionar Nova Página

**Exemplo: Adicionar página de "Histórico"**

1. **Edite `src/ui.py`**:

```python
def show_history_page(self):
    """Mostra a página de histórico"""
    self.clear_main_area()
    
    container = tk.Frame(self.main_area, bg=COLORS["bg_primary"], padx=20, pady=20)
    container.pack(fill="both", expand=True)
    
    title = tk.Label(
        container,
        text="Histórico de Mensagens",
        font=FONTS["title_medium"],
        bg=COLORS["bg_primary"],
        fg=COLORS["text_primary"]
    )
    title.pack(anchor="w", pady=(0, 20))
    
    # Adicione componentes aqui
```

2. **Adicione botão de navegação em `build_sidebar()`**:

```python
nav_items = [
    ("💬 Chat", "chat", self.show_chat_page),
    ("📜 Histórico", "history", self.show_history_page),  # Novo
    # ... outros itens
]
```

### 2. Adicionar Nova Configuração

1. **Edite `config.py`**:

```python
NEW_SETTING = {
    "enabled": True,
    "value": 100,
}
```

2. **Use em `src/ui.py` ou `src/main.py`**:

```python
from config import NEW_SETTING

if NEW_SETTING["enabled"]:
    # Fazer algo
    pass
```

### 3. Adicionar Nova Função Utilitária

1. **Edite `src/utils.py`**:

```python
def nova_funcao(parametro):
    """
    Descrição da função.
    
    Args:
        parametro: Descrição
        
    Returns:
        Tipo: Descrição
    """
    logger.info(f"Executando nova_funcao com {parametro}")
    # Implementação
    return resultado
```

2. **Use em outro arquivo**:

```python
from utils import nova_funcao

resultado = nova_funcao("valor")
```

## Debugging

### Ativar Modo Debug

Edite `config.py`:

```python
SYSTEM_CONFIG = {
    "log_level": "DEBUG",  # Mude de INFO para DEBUG
    # ...
}
```

### Visualizar Logs

```bash
# Em tempo real
tail -f ~/.brx_ai_app.log

# Últimas 50 linhas
tail -50 ~/.brx_ai_app.log

# Filtrar por erro
grep ERROR ~/.brx_ai_app.log
```

### Usar Debugger

```python
import pdb

# Adicione em qualquer lugar do código
pdb.set_trace()

# Ou use breakpoint() (Python 3.7+)
breakpoint()
```

## Testes

### Teste de Sintaxe

```bash
python3 -m py_compile config.py src/main.py src/ui.py src/utils.py
```

### Teste de Importação

```bash
python3 -c "
import config
from src import main
from src import ui
from src import utils
print('✓ Todas as importações funcionaram')
"
```

### Teste de Execução

```bash
python3 src/main.py
```

### Teste de Instalação

```bash
sudo bash install.sh
brx_ai_app  # Verificar se funciona
```

## Commits e Pull Requests

### Mensagens de Commit

Siga o padrão Conventional Commits:

```
feat: adiciona nova página de histórico
fix: corrige bug no chat
docs: atualiza README
style: formata código
refactor: reorganiza estrutura de ui.py
test: adiciona testes para utils.py
chore: atualiza dependências
```

### Exemplo de PR

```
# Título
feat: integração com OpenAI API

# Descrição
- Adiciona suporte a OpenAI API
- Implementa cache de respostas
- Adiciona configuração de modelo

# Testes
- [x] Sintaxe verificada
- [x] Importações funcionam
- [x] Aplicação inicia
- [x] Chat funciona

# Checklist
- [x] Código segue PEP 8
- [x] Docstrings adicionadas
- [x] Logs implementados
- [x] README atualizado
```

## Performance

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Código a ser analisado
# ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Otimizações Comuns

1. **Use threading para operações longas**:
```python
thread = threading.Thread(target=funcao_longa)
thread.daemon = True
thread.start()
```

2. **Cache resultados**:
```python
@functools.lru_cache(maxsize=128)
def funcao_cara(parametro):
    return resultado
```

3. **Lazy loading**:
```python
def get_data():
    if not hasattr(self, '_data'):
        self._data = carregar_dados()
    return self._data
```

## Troubleshooting

### Problema: ImportError ao executar

**Solução**: Verifique se está no diretório correto
```bash
cd /home/ubuntu/brx_ai_improved
python3 src/main.py
```

### Problema: Tkinter não encontrado

**Solução**: Instale tkinter
```bash
sudo pacman -S tk  # Arch
sudo apt install python3-tk  # Debian/Ubuntu
```

### Problema: Permissão negada ao instalar

**Solução**: Use sudo
```bash
sudo bash install.sh
```

### Problema: Aplicação congelada

**Solução**: Use threading para operações longas
```python
thread = threading.Thread(target=operacao_longa)
thread.daemon = True
thread.start()
```

## Recursos Úteis

- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

## Roadmap de Desenvolvimento

### Curto Prazo (v2.1)
- [ ] Melhorar interface de chat
- [ ] Adicionar temas customizáveis
- [ ] Implementar histórico de chat persistente

### Médio Prazo (v2.5)
- [ ] Integração com OpenAI API
- [ ] Suporte a plugins
- [ ] Interface web alternativa

### Longo Prazo (v3.0)
- [ ] Sincronização em nuvem
- [ ] Modo offline melhorado
- [ ] Suporte a múltiplos idiomas
- [ ] Aplicativo mobile

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Última Atualização**: Fevereiro de 2026
