# BRX AI - Agente Autônomo para Linux

**BRX AI** é um agente de inteligência artificial autônomo projetado especificamente para Linux, com uma interface nativa moderna inspirada no Manus. O aplicativo funciona como um programa nativo do sistema, oferecendo visão de tela, controle de mouse/teclado e automação de tarefas.

## 🎯 Características Principais

- **Interface Moderna**: Design "Modo Prime" com dark mode otimizado
- **Chat em Tempo Real**: Interação contínua com a IA
- **Visão do Sistema**: Monitoramento de tela em tempo real
- **Painel de Automação**: Controle de mouse, teclado e terminal
- **Configurações Avançadas**: Ajustes de desempenho e segurança
- **Instalação Nativa**: Integração completa com o menu de aplicativos do Linux
- **Logs Detalhados**: Rastreamento de todas as ações

## 📋 Requisitos

- **Sistema Operacional**: Linux (Arch, Debian/Ubuntu, Fedora, etc.)
- **Python**: 3.8 ou superior
- **Bibliotecas Python**:
  - `tkinter` (geralmente incluído com Python)
  - `psutil` (será instalado automaticamente)
  - `pillow` (opcional, para processamento de imagens)
- `transformers` (para execução do modelo local)
- `torch` (para execução do modelo local)
- `accelerate` (para otimização de hardware)

## 🚀 Instalação

### Instalação Rápida

```bash
cd /caminho/para/brx_ai_improved
sudo bash install.sh
```

### Instalação Manual

1. **Clone ou baixe o repositório**:
```bash
git clone https://github.com/seu-usuario/brx_ai_improved.git
cd brx_ai_improved
```

2. **Execute o instalador**:
```bash
sudo bash install.sh
```

3. **Siga as instruções na tela**

## 💻 Uso

### Iniciar via Terminal

```bash
brx_ai_app
```

### Iniciar via Menu de Aplicativos

Procure por "BRX AI Agent" no menu de aplicativos do seu desktop environment.

### Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Enter` | Enviar mensagem |
| `Shift + Enter` | Nova linha no input |
| `Ctrl + L` | Limpar chat |
| `Ctrl + I` | Focar no input |

## 📁 Estrutura de Arquivos

```
brx_ai_improved/
├── config.py              # Configurações globais e paleta de cores
├── brx_ai_app.sh         # Script de inicialização
├── install.sh            # Instalador
├── uninstall.sh          # Desinstalador
├── README.md             # Este arquivo
├── src/
│   ├── main.py           # Núcleo principal da IA
│   ├── ui.py             # Interface gráfica
│   └── utils.py          # Funções utilitárias
├── config/               # Arquivos de configuração
├── assets/               # Ícones e recursos
└── docs/                 # Documentação adicional
```

## ⚙️ Configuração

### Arquivos de Configuração

Os arquivos de configuração são armazenados em:

```
~/.brx_ai/
├── config.json           # Configurações do usuário
├── logs/
│   └── brx_ai.log       # Arquivo de log principal
├── data/
│   └── chat_history.json # Histórico de chat
└── cache/               # Cache de dados
```

### Variáveis de Ambiente

Você pode configurar as seguintes variáveis de ambiente:

```bash
export BRX_AI_LOG_LEVEL=DEBUG      # Nível de log (DEBUG, INFO, WARNING, ERROR)
export BRX_AI_CONFIG_DIR=~/.brx_ai # Diretório de configuração
```

## 🔧 Desenvolvimento

### Estrutura do Código

- **config.py**: Paleta de cores, dimensões, tipografia e constantes
- **src/main.py**: Classe principal da aplicação e engine de IA
- **src/ui.py**: Interface gráfica com Tkinter
- **src/utils.py**: Logging, formatação e funções auxiliares

### Adicionar Novas Funcionalidades

1. Edite os arquivos relevantes em `src/`
2. Atualize `config.py` se necessário
3. Teste localmente: `python3 src/main.py`
4. Reinstale se necessário: `sudo bash install.sh`

## 📊 Paleta de Cores

O BRX AI utiliza a paleta "Modo Prime" otimizada para conforto visual:

| Cor | Código | Uso |
|-----|--------|-----|
| Deep Space | `#0B0E14` | Fundo principal |
| Midnight Blue | `#10141B` | Sidebar |
| Card Background | `#161B22` | Cards e containers |
| Azul Arch | `#1793D1` | Acentos primários |
| Cyan Neon | `#00E5FF` | Destaques |
| Verde Neon | `#00FF9C` | Sucesso |
| Amarelo | `#FFD700` | Avisos |
| Vermelho | `#FF6B6B` | Erros |

## 🔐 Segurança

- **Controle de Permissões**: O aplicativo requer confirmação para ações sensíveis
- **Logging Completo**: Todas as ações são registradas em `~/.brx_ai_app.log`
- **Isolamento**: A IA roda em um ambiente controlado

## 🐛 Solução de Problemas

### Problema: "Python 3 não encontrado"

**Solução**: Instale Python 3
```bash
# Arch Linux
sudo pacman -S python

# Debian/Ubuntu
sudo apt install python3
```

### Problema: "tkinter não encontrado"

**Solução**: Instale tkinter
```bash
# Arch Linux
sudo pacman -S tk

# Debian/Ubuntu
sudo apt install python3-tk
```

### Problema: "Permissão negada ao instalar"

**Solução**: Use `sudo` para executar o instalador
```bash
sudo bash install.sh
```

### Problema: Arquivo de log cresce muito

**Solução**: Limpe os logs antigos
```bash
rm ~/.brx_ai/logs/brx_ai.log
```

## 📝 Logs

Os logs são salvos em: `~/.brx_ai_app.log`

Para visualizar em tempo real:
```bash
tail -f ~/.brx_ai_app.log
```

## 🗑️ Desinstalação

Para remover completamente o BRX AI:

```bash
sudo /opt/brx_ai_app/uninstall.sh
```

Ou manualmente:

```bash
sudo rm -rf /opt/brx_ai_app
sudo rm -f /usr/local/bin/brx_ai_app
rm -f ~/.local/share/applications/brx_ai_app.desktop
rm -rf ~/.brx_ai
```

## 📄 Licença

Este projeto é mantido por **DragonSCPOFICIAL**.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:

1. Reportar bugs
2. Sugerir melhorias
3. Enviar pull requests
4. Melhorar a documentação

## 📞 Suporte

Para suporte, abra uma issue no repositório ou entre em contato com o mantenedor.

## 🎨 Customização

### Alterar Cores

Edite `config.py` e modifique o dicionário `COLORS`:

```python
COLORS = {
    "bg_primary": "#0B0E14",  # Altere para sua cor preferida
    # ... outras cores
}
```

### Alterar Dimensões

Edite `config.py` e modifique as dimensões:

```python
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
```

### Alterar Tipografia

Edite `config.py` e modifique o dicionário `FONTS`:

```python
FONTS = {
    "title_large": ("Segoe UI", 24, "bold"),
    # ... outras fontes
}
```

## 🚀 Roadmap

- [x] Integração com DeepSeek-Coder (Local/Offline)
- [ ] Suporte a plugins de sistema
- [ ] Interface de Visão Computacional ativa
- [ ] Sincronização de contexto entre sessões
- [ ] Temas customizáveis (Neon/Glassmorphism)

## 📚 Referências

- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [psutil Documentation](https://psutil.readthedocs.io/)
- [Python Desktop Applications](https://wiki.python.org/moin/GuiProgramming)

---

**Desenvolvido com ❤️ para Linux**

Última atualização: Fevereiro de 2026
