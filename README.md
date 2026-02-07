# 🐉 Arch Linux Projects - DragonSCPOFICIAL

Este repositório contém ferramentas nativas para **Arch Linux**. Abaixo você encontra os comandos para instalar e desinstalar cada projeto automaticamente pelo terminal, mesmo que você já tenha o repositório baixado.

---

## 🤖 1. BRX AI (Agente Autônomo)
O **BRX AI** é um agente de inteligência artificial com interface nativa inspirada no Manus.

### 🚀 Instalação Automática (Comando Único)
Este comando clona o repositório (ou atualiza se já existir) e inicia a instalação:
```bash
if [ -d "Arch-Linux" ]; then cd Arch-Linux && git pull; else git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux; fi && cd BRX_AI && sudo bash install.sh
```

### 🗑️ Desinstalação Automática
Para remover completamente o BRX AI do sistema:
```bash
sudo bash /opt/brx_ai_app/uninstall.sh
```

---

## 🎮 2. Aether Launcher (Minecraft Elite)
O **Aether Launcher** é um inicializador de Minecraft otimizado para Arch Linux.

### 🚀 Instalação Automática (Comando Único)
Este comando clona o repositório (ou atualiza se já existir) e inicia a instalação:
```bash
if [ -d "Arch-Linux" ]; then cd Arch-Linux && git pull; else git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux; fi && cd AetherLauncher && sudo bash install_arch.sh
```

### 🗑️ Desinstalação Automática
Para remover completamente o Aether Launcher do sistema:
```bash
sudo bash /opt/aetherlauncher/uninstall.sh
```

---

## 📂 Estrutura do Repositório
| Pasta | Projeto | Descrição |
| :--- | :--- | :--- |
| `/BRX_AI` | **BRX AI** | Agente de IA com visão de sistema e automação. |
| `/AetherLauncher` | **Aether Launcher** | Launcher de Minecraft nativo para Arch Linux. |

---

## 🛠️ Requisitos Gerais
*   **Python 3.8+**
*   **Tkinter** (`sudo pacman -S tk`)
*   **Git** (`sudo pacman -S git`)

---

**Mantido por [DragonSCPOFICIAL](https://github.com/DragonSCPOFICIAL)**  
*Desenvolvido com ❤️ para a comunidade Linux.*
