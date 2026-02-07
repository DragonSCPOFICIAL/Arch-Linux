# Arquitetura do BRX AI

## Visão Geral

O **BRX AI** é um agente autônomo de inteligência artificial para Linux, estruturado em uma arquitetura modular que separa claramente as responsabilidades de cada componente.

## Componentes Principais

### 1. **config.py** - Configurações Globais

Centraliza todas as constantes, configurações e paleta de cores do aplicativo.

**Responsabilidades:**
- Definir paleta de cores "Modo Prime"
- Configurar dimensões da janela e componentes
- Armazenar tipografia padrão
- Definir caminhos de arquivos de configuração
- Armazenar mensagens do sistema

**Estrutura:**
```python
COLORS = {
    "bg_primary": "#0B0E14",
    "accent_primary": "#1793D1",
    # ...
}

FONTS = {
    "title_large": ("Segoe UI", 24, "bold"),
    # ...
}

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
```

### 2. **src/utils.py** - Funções Utilitárias

Fornece funções reutilizáveis para logging, formatação e operações do sistema.

**Responsabilidades:**
- Configurar logging
- Formatar timestamps e datas
- Obter informações do sistema (CPU, memória, disco)
- Carregar/salvar arquivos JSON
- Validar entrada do usuário
- Converter unidades (bytes, segundos, etc.)

**Principais Funções:**
```python
setup_logger(name)          # Configura logging
get_system_info()           # Obtém info do sistema
format_timestamp()          # Formata hora
load_json(filepath)         # Carrega JSON
save_json(filepath, data)   # Salva JSON
```

### 3. **src/ui.py** - Interface Gráfica

Implementa a interface do usuário usando Tkinter com design "Modo Prime".

**Responsabilidades:**
- Criar e gerenciar janelas
- Renderizar componentes (botões, labels, campos de texto)
- Gerenciar navegação entre páginas
- Exibir chat e mensagens
- Atualizar status do sistema

**Principais Classes:**
```python
class BRXAIInterface:
    def __init__(self, root, ai_engine)
    def build_ui()              # Constrói interface
    def show_chat_page()        # Página de chat
    def show_vision_page()      # Página de visão
    def show_automation_page()  # Página de automação
    def show_settings_page()    # Página de configurações
    def append_message()        # Adiciona mensagem ao chat
    def send_message()          # Envia mensagem
```

**Páginas Disponíveis:**
1. **Chat** - Interface de conversação com a IA
2. **Visão** - Monitoramento de tela em tempo real
3. **Automação** - Painel de controle de ferramentas
4. **Configurações** - Ajustes do sistema

### 4. **src/main.py** - Núcleo Principal

Gerencia a inicialização e execução do aplicativo.

**Responsabilidades:**
- Inicializar o engine de IA
- Criar a janela principal
- Gerenciar sinais do sistema (SIGINT, SIGTERM)
- Executar o loop principal da aplicação

**Principais Classes:**
```python
class BRXAIEngine:
    def process(user_input)     # Processa entrada do usuário

class BRXAIApp:
    def __init__()              # Inicializa app
    def run()                   # Executa app
    def on_closing()            # Manipula fechamento
```

### 5. **brx_ai_app.sh** - Script de Inicialização

Script bash que gerencia a execução do aplicativo.

**Responsabilidades:**
- Verificar dependências
- Definir variáveis de ambiente
- Redirecionar output para logs
- Executar main.py

### 6. **install.sh** - Instalador

Script bash para instalar o aplicativo como programa nativo do Linux.

**Responsabilidades:**
- Verificar requisitos do sistema
- Criar diretórios de instalação
- Copiar arquivos
- Instalar dependências Python
- Criar link simbólico
- Criar atalho no menu

### 7. **uninstall.sh** - Desinstalador

Script bash para remover o aplicativo do sistema.

**Responsabilidades:**
- Remover atalhos do menu
- Remover links simbólicos
- Remover diretórios de instalação
- Opcionalmente remover dados do usuário

## Fluxo de Dados

```
┌─────────────────────────────────────────────────────────┐
│                    BRXAIApp (main.py)                   │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         BRXAIInterface (ui.py)                     │ │
│  │                                                    │ │
│  │  ┌──────────────┐  ┌──────────────┐              │ │
│  │  │ Sidebar      │  │ Main Area    │              │ │
│  │  │              │  │              │              │ │
│  │  │ - Chat       │  │ - Chat Page  │              │ │
│  │  │ - Vision     │  │ - Vision Page│              │ │
│  │  │ - Automation │  │ - Automation │              │ │
│  │  │ - Settings   │  │ - Settings   │              │ │
│  │  └──────────────┘  └──────────────┘              │ │
│  │                                                    │ │
│  │  Usa: config.py (cores, fontes, dimensões)       │ │
│  │  Usa: utils.py (logging, formatação, sistema)    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         BRXAIEngine (main.py)                      │ │
│  │                                                    │ │
│  │  Processa entrada do usuário                      │ │
│  │  Integra com LLMs (futuro)                        │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Estrutura de Diretórios

```
brx_ai_improved/
├── config.py                    # Configurações globais
├── brx_ai_app.sh               # Script de inicialização
├── install.sh                  # Instalador
├── uninstall.sh                # Desinstalador
├── requirements.txt            # Dependências Python
├── README.md                   # Documentação principal
├── src/
│   ├── main.py                 # Núcleo principal
│   ├── ui.py                   # Interface gráfica
│   └── utils.py                # Funções utilitárias
├── config/                     # Arquivos de configuração
├── assets/                     # Ícones e recursos
└── docs/
    ├── ARCHITECTURE.md         # Este arquivo
    └── DEVELOPMENT.md          # Guia de desenvolvimento
```

## Paleta de Cores - "Modo Prime"

| Elemento | Cor | Código |
|----------|-----|--------|
| Fundo Principal | Deep Space | `#0B0E14` |
| Sidebar | Midnight Blue | `#10141B` |
| Cards | Card Background | `#161B22` |
| Acento Primário | Azul Arch | `#1793D1` |
| Acento Secundário | Cyan Neon | `#00E5FF` |
| Sucesso | Verde Neon | `#00FF9C` |
| Aviso | Amarelo | `#FFD700` |
| Erro | Vermelho | `#FF6B6B` |
| Texto Primário | Branco | `#E6EDF3` |
| Texto Secundário | Cinza | `#7D8590` |
| Bordas | Cinza Escuro | `#30363D` |

## Ciclo de Vida da Aplicação

### 1. Inicialização (Startup)

```
brx_ai_app.sh
    ↓
Verifica dependências
    ↓
Define variáveis de ambiente
    ↓
Executa src/main.py
    ↓
BRXAIApp.__init__()
    ↓
Cria BRXAIEngine
    ↓
Cria janela Tkinter
    ↓
Cria BRXAIInterface
    ↓
Exibe página inicial (Chat)
```

### 2. Execução (Runtime)

```
Usuário digita mensagem
    ↓
send_message() chamado
    ↓
Mensagem exibida no chat
    ↓
process_message() em thread separada
    ↓
BRXAIEngine.process() processa
    ↓
Resposta exibida no chat
    ↓
Aguarda próxima mensagem
```

### 3. Encerramento (Shutdown)

```
Usuário clica em fechar
    ↓
on_closing() chamado
    ↓
Registra encerramento em log
    ↓
root.quit()
    ↓
root.destroy()
    ↓
sys.exit(0)
```

## Dependências

### Dependências do Sistema

- Python 3.8+
- tkinter (geralmente incluído)
- Gerenciador de pacotes (pacman, apt, etc.)

### Dependências Python

- `psutil` - Monitoramento de sistema
- `pillow` - Processamento de imagens (opcional)
- `requests` - Requisições HTTP (opcional)

## Extensibilidade

### Adicionar Nova Página

1. Crie um método `show_nova_pagina()` em `BRXAIInterface`
2. Adicione um botão de navegação em `build_sidebar()`
3. Implemente a lógica da página

### Integrar com LLM

1. Crie uma classe `LLMIntegration` em novo arquivo
2. Implemente método `generate_response()`
3. Chame em `BRXAIEngine.process()`

### Adicionar Novo Componente

1. Crie uma classe em `ui.py`
2. Reutilize cores de `config.py`
3. Siga o padrão de nomenclatura

## Performance

- **Rendering**: Tkinter (nativo, rápido)
- **Threading**: Usado para operações longas
- **Logging**: Assíncrono para não bloquear UI
- **Monitoramento**: Atualizado a cada 2 segundos

## Segurança

- Validação de entrada do usuário
- Logging completo de ações
- Isolamento de processos
- Permissões de arquivo apropriadas

## Testes

### Testes de Sintaxe

```bash
python3 -m py_compile config.py src/main.py src/ui.py src/utils.py
```

### Testes de Importação

```bash
python3 -c "import config; import src.main; import src.ui; import src.utils"
```

### Testes de Execução

```bash
python3 src/main.py
```

## Roadmap

- [ ] Integração com OpenAI API
- [ ] Suporte a plugins
- [ ] Interface web alternativa
- [ ] Sincronização em nuvem
- [ ] Modo offline melhorado
- [ ] Temas customizáveis
- [ ] Suporte a múltiplos idiomas

---

**Versão**: 2.0.0  
**Última Atualização**: Fevereiro de 2026
