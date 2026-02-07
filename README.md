# 🐉 Arch Linux Projects - DragonSCPOFICIAL

Este repositório contém ferramentas nativas para **Arch Linux**. Os comandos abaixo instalam os projetos como **programas reais** no seu sistema, criando atalhos no menu de aplicativos e comandos globais no terminal.

---

## 🤖 1. BRX AI (Agente Autônomo)
O **BRX AI** é um agente de inteligência artificial com interface nativa moderna.

### 🚀 Instalação como Programa Nativo
Este comando instala o BRX AI em `/opt`, cria o comando `brx_ai_app` e adiciona o atalho ao seu menu:
```bash
if [ -d "Arch-Linux" ]; then cd Arch-Linux && git fetch --all && git reset --hard origin/main; else git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux; fi && cd BRX_AI && sudo bash install.sh
```

### 🗑️ Desinstalação Completa
```bash
sudo bash /opt/brx_ai_app/uninstall.sh
```

---

## 🎮 2. Aether Launcher (Minecraft Elite)
O **Aether Launcher** é um inicializador de Minecraft otimizado para Arch Linux.

### 🚀 Instalação como Programa Nativo
Este comando instala o Aether Launcher em `/opt`, cria o comando `aetherlauncher` e adiciona o atalho ao seu menu:
```bash
if [ -d "Arch-Linux" ]; then cd Arch-Linux && git fetch --all && git reset --hard origin/main; else git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux; fi && cd AetherLauncher && sudo bash install_arch.sh
```

### 🗑️ Desinstalação Completa
```bash
sudo bash /opt/aetherlauncher/uninstall.sh
```

---

## 📂 O que muda após a instalação?
Após rodar os comandos acima, os projetos deixam de ser apenas scripts e passam a ser **programas do sistema**:
1.  **Menu de Aplicativos**: Você encontrará "BRX AI Agent" e "Aether Launcher" no seu menu (GNOME, KDE, XFCE, etc.).
2.  **Terminal Global**: Você pode abrir os programas de qualquer lugar apenas digitando `brx_ai_app` ou `aetherlauncher`.
3.  **Localização Padrão**: Os arquivos ficam organizados em `/opt/`, seguindo o padrão Linux.

---

## 🛠️ Requisitos do Sistema
*   **Python 3.8+**
*   **Tkinter** (`sudo pacman -S tk`)
*   **Git** (`sudo pacman -S git`)

---

**Mantido por [DragonSCPOFICIAL](https://github.com/DragonSCPOFICIAL)**  
*Desenvolvido com ❤️ para a comunidade Linux.*
