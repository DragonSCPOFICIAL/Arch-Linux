# BRX AI - Autonomous Programmer Core (Manus Local)

Este é um agente de engenharia autônomo focado em **Desenvolvimento de Software**, **Hardware** e **Kernel Linux**. Ele funciona como um "Manus Local", capaz de evoluir a linguagem **ULX** de forma independente diretamente no seu notebook.

---

## 🎯 Capacidades do Agente
- **Modo Autônomo**: Ciclo fechado de pensamento e ação para evoluir código.
- **Conector de Identidade**: Integração nativa com Git sem necessidade de tokens manuais.
- **Consciência de Contexto**: Analisa o repositório inteiro e o guia de evolução da ULX.
- **Privacidade Total**: Roda 100% local via Ollama e DeepSeek-Coder.

---

## 🛠️ Instalação e Ativação

Siga estes passos para configurar e rodar o seu agente:

### 1. Clonar e Acessar
```bash
git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git
cd Arch-Linux/BRX_AI
```

### 2. Configurar o Motor e Permissões
Este script instala o Ollama, baixa o modelo DeepSeek e configura as permissões de segurança do Git.
**Nota:** É necessário dar permissão de execução ao script.
```bash
chmod +x setup_engine.sh
./setup_engine.sh
```

### 3. Iniciar o Agente
```bash
python3 main.py
```

---

## 💻 Comandos Disponíveis

| Comando | Descrição |
| :--- | :--- |
| `autonomo` | **Ativa o Modo Manus Local.** O agente começa a evoluir a linguagem ULX sozinho. |
| `[Pergunta]` | Chat direto com a IA sobre código, hardware ou Linux. |
| `sh [comando]` | Executa comandos no terminal do seu notebook. |
| `git [comando]` | Gerencia o repositório (status, commit, push) via agente. |
| `lsfiles` | Lista todos os arquivos do projeto. |
| `summarize [arquivo]` | Gera um resumo inteligente do conteúdo de um arquivo. |
| `context` | Mostra o que a IA está "vendo" no momento (Arquivos + Guia ULX). |
| `sair` | Encerra a sessão do agente. |

---

## 🚀 Guia de Evolução ULX
O agente segue as diretrizes do arquivo `ulx_evolution_guide.md` para garantir que a linguagem cresça com foco em:
1. **Simplicidade** na sintaxe.
2. **Performance** de baixo nível.
3. **Integração** profunda com o Kernel Linux.

---

## ⚠️ Solução de Problemas
- **Permission Denied:** Se receber erro ao rodar scripts, use `chmod +x nome_do_script.sh`.
- **Erro de Conexão:** Certifique-se de que o Ollama está rodando (`ollama serve`).

**Desenvolvido por DragonSCPOFICIAL & Manus AI**
