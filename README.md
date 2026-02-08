# Arch Linux Projects - DragonSCPOFICIAL

Este repositório contém ferramentas nativas para **Arch Linux**. Os comandos abaixo instalam os projetos como **programas reais** no seu sistema, resolvendo automaticamente problemas de permissão e conflitos.

---

## 1. BRX AI (Agente Autônomo)
O **BRX AI** é um agente de inteligência artificial com interface nativa moderna.

### Instalação Automática (Correção de Permissões Inclusa)
Este comando resolve erros de "insufficient permission" no Git e instala o programa:
```bash
if [ -d "Arch-Linux" ]; then sudo chown -R $USER:$USER Arch-Linux && cd Arch-Linux && git fetch --all && git reset --hard origin/main; else git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux; fi && cd BRX_AI && sudo bash install.sh
```

### Desinstalação Completa
O desinstalador agora suporta o modo automático via interface e remoção completa via terminal:
```bash
sudo bash /opt/brx_ai_app/uninstall.sh
```

---

## 2. Aether Launcher (Minecraft Elite)
O **Aether Launcher** é um inicializador de Minecraft otimizado para Arch Linux.

### Instalação Automática (Correção de Permissões Inclusa)
Este comando resolve erros de "insufficient permission" no Git e instala o programa:
```bash
if [ -d "Arch-Linux" ]; then sudo chown -R $USER:$USER Arch-Linux && cd Arch-Linux && git fetch --all && git reset --hard origin/main; else git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux; fi && cd AetherLauncher && sudo bash install_arch.sh
```

### Desinstalação Completa
O desinstalador agora suporta o modo automático via interface e remoção completa via terminal:
```bash
sudo bash /opt/aetherlauncher/uninstall.sh
```

---

## O que muda após a instalação?
Após rodar os comandos acima, os projetos são integrados ao sistema:
1.  **Menu de Aplicativos**: Procure por "BRX AI Agent" ou "Aether Launcher" no seu menu.
2.  **Terminal Global**: Abra os programas digitando `brx_ai_app` ou `aetherlauncher`.
3.  **Localização Padrão**: Arquivos instalados em `/opt/` para maior segurança.

---

## Requisitos do Sistema
*   **Python 3.8+**
*   **Tkinter** (`sudo pacman -S tk`)
*   **Git** (`sudo pacman -S git`)

---

**Mantido por [DragonSCPOFICIAL](https://github.com/DragonSCPOFICIAL)**  
*Desenvolvido para a comunidade Linux.*
