# 🎮 Aether Launcher - Minecraft Launcher Elite

O **Aether Launcher** é um inicializador de Minecraft otimizado especificamente para o **Arch Linux**, oferecendo uma instalação nativa e integração completa com o sistema.

## ✨ Características

- **Instalação Nativa**: Script de instalação dedicado para Arch Linux (`pacman`).
- **Integração com o Menu**: Cria automaticamente um atalho no menu de aplicativos.
- **Leve e Rápido**: Desenvolvido em Python para baixo consumo de recursos.
- **Atualizador Integrado**: Sistema de atualização automática.

## 🚀 Instalação Rápida (Comando Único)

Para instalar ou atualizar para a versão mais recente, utilize o comando abaixo. Ele limpa qualquer rastro de instalações anteriores para evitar erros:

```bash
sudo rm -rf Arch-Linux && git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux/AetherLauncher && sudo bash install_arch.sh
```

> **Nota**: Após a instalação, você pode abrir o launcher pelo menu de aplicativos ou digitando `aetherlauncher` no terminal.

## 🗑️ Desinstalação Completa

Este comando remove o launcher, todos os dados do Minecraft, configurações e atalhos do sistema de forma definitiva:

```bash
sudo bash /opt/aetherlauncher/uninstall.sh
```

---

## 📋 Requisitos do Sistema

- **Sistema**: Arch Linux (ou derivados como Manjaro, EndeavourOS)
- **Dependências**: Instaladas automaticamente pelo script (Python 3, Tkinter, Pillow, Requests).

---
**Desenvolvido por DragonSCPOFICIAL**
