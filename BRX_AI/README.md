# BRX AI - Agente Autônomo para Linux

**BRX AI** é um agente de inteligência artificial autônomo projetado especificamente para Linux, com uma interface nativa moderna inspirada no Manus. O aplicativo funciona como um programa nativo do sistema, oferecendo visão de tela, controle de mouse/teclado e automação de tarefas, agora com suporte a execução local e ilimitada via DeepSeek-Coder.

## 🎯 Características Principais

- **Interface Moderna**: Design "Modo Prime" com dark mode otimizado.
- **IA Local e Ilimitada**: Integração com DeepSeek-Coder para processamento offline.
- **Visão do Sistema**: Monitoramento de tela em tempo real.
- **Painel de Automação**: Controle de mouse, teclado e terminal.
- **Instalação Nativa**: Integração completa com o menu de aplicativos do Linux.

## 📋 Requisitos de Sistema

- **Sistema Operacional**: Linux (Arch, Debian/Ubuntu, Fedora, etc.)
- **Python**: 3.8 ou superior
- **Hardware Recomendado**: 8GB+ RAM (para rodar o modelo local de 1.3b)

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git
cd Arch-Linux/BRX_AI
```

### 2. Instalar Dependências
Para que a IA funcione localmente, instale as bibliotecas necessárias:
```bash
pip install -r requirements.txt
pip install transformers torch accelerate
```

### 3. Baixar o Modelo Local (Obrigatório para Modo Offline)
Execute o script de download para baixar o modelo DeepSeek-Coder (aprox. 2.6GB):
```bash
python3 src/download_model.py
```

### 4. Instalação Nativa no Linux
Para integrar o BRX AI ao seu sistema como um aplicativo nativo:
```bash
sudo bash install.sh
```

## 💻 Uso

### Iniciar via Terminal
```bash
brx_ai_app
```
*Ou execute diretamente o núcleo:*
```bash
python3 src/main.py
```

### Iniciar via Menu de Aplicativos
Procure por **"BRX AI Agent"** no menu do seu ambiente de desktop (GNOME, KDE, XFCE, etc.).

## 📁 Estrutura do Projeto

- `src/main.py`: Núcleo principal e motor da IA.
- `src/local_llm.py`: Gerenciador do modelo DeepSeek-Coder local.
- `src/download_model.py`: Script para baixar os pesos do modelo.
- `src/ui.py`: Interface gráfica em Tkinter.
- `install.sh`: Script de automação de instalação no Linux.

## 🚀 Roadmap

- [x] Integração com DeepSeek-Coder (Local/Offline)
- [ ] Suporte a plugins de sistema
- [ ] Interface de Visão Computacional ativa
- [ ] Sincronização de contexto entre sessões
- [ ] Temas customizáveis (Neon/Glassmorphism)

---

**Desenvolvido com ❤️ para Linux por DragonSCPOFICIAL**
