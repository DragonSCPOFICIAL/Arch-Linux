# BRX AI - Autonomous Programmer Core (Nativo & Ilimitado)

Este é um agente de engenharia focado exclusivamente em **Desenvolvimento de Software**, **Hardware** e **Kernel Linux**. Ele utiliza o modelo **DeepSeek-Coder** rodando localmente para garantir privacidade total e zero custo de API.

Agora, o BRX AI evoluiu para um **Agente Autônomo**, capaz de gerenciar seu próprio repositório Git, ler e editar arquivos, e manter o contexto completo do projeto.

---

## 🎯 Foco do Agente
- **Linguagens**: C, C++, Rust, Python, Assembly e criação de novas linguagens.
- **Sistemas**: Otimização de Kernel Linux, módulos eBPF e drivers.
- **Hardware**: Interação com CPU (AVX-512), GPU e gerenciamento de memória.
- **Automação**: Gerenciamento autônomo de repositórios Git e edição de código.

---

## 🛠️ Instalação Rápida

Para configurar o motor de IA e o agente no seu notebook:

### 1. Clonar e Acessar
```bash
git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git
cd Arch-Linux/BRX_AI
```

### 2. Configurar o Motor (DeepSeek Local)
Este script instalará o Ollama e baixará o modelo `deepseek-coder:1.3b` (~800MB).
```bash
chmod +x setup_engine.sh
./setup_engine.sh
```

### 3. Iniciar o Agente
```bash
python3 main.py
```

---

## 💻 Comandos do Agente

| Comando | Descrição |
| :--- | :--- |
| `[Pergunta]` | Digite qualquer dúvida de código para a IA. Ela agora tem contexto do repositório! |
| `sh [comando]` | Executa comandos diretamente no terminal Linux. |
| `read [arquivo]` | Lê o conteúdo de um arquivo específico. |
| `write [arquivo] [conteúdo]` | Escreve ou sobrescreve um arquivo. |
| `lsfiles` | Lista todos os arquivos do repositório. |
| `summarize [arquivo]` | Gera um resumo inteligente do conteúdo de um arquivo. |
| `context` | Mostra o contexto atual que a IA está utilizando. |
| `git [comando]` | Executa comandos Git (ex: `git status`, `git commit -m "..."`). |
| `sair` | Encerra o agente. |

---

## 🚀 Por que usar esta versão?
- **Autônomo**: O agente pode gerenciar o código e o repositório por conta própria.
- **Consciente**: A IA entende a estrutura do seu projeto através do contexto automático.
- **Leve**: O modelo ocupa menos de 1GB de disco.
- **Privado**: Nada sai do seu notebook.
- **Ilimitado**: Sem taxas de API ou limites de tokens.

**Desenvolvido por DragonSCPOFICIAL & Manus AI**
