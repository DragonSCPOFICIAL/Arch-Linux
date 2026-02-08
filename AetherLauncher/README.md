# 🎮 Aether Launcher v3.0 - Minecraft Elite Linux (Nativo)

O **Aether Launcher** é um inicializador de Minecraft de alta performance, otimizado especificamente para sistemas **Linux (Arch Linux e derivados)**. Ele oferece uma experiência nativa, rápida e visualmente moderna, aproveitando ao máximo o hardware através de drivers nativos.

## ✨ Novidades da Versão 3.0

- **🚀 Performance Nativa Absurda**: Sem Wine, sem emulação. Execução direta para o máximo de FPS.
- **🛠️ Engine de Compatibilidade**: Suporte exclusivo para hardware antigo através de *Mesa Overrides*, permitindo rodar versões modernas em GPUs limitadas.
- **📦 Gestão de Instâncias**: Cada perfil possui sua própria pasta isolada (`mods`, `config`, etc.).
- **🔌 Mod Loaders Automáticos**: Instalação de **Forge** e **Fabric** integrada e automática.
- **💎 Interface Moderna**: UI redesenhada com base em padrões modernos, limpa e intuitiva.

---

## 🚀 Instalação Rápida (Comando Único)

Para realizar uma **instalação limpa** ou **atualizar** para a versão mais recente, copie e cole o comando abaixo no seu terminal:

```bash
sudo rm -rf Arch-Linux && git clone https://github.com/DragonSCPOFICIAL/Arch-Linux.git && cd Arch-Linux/AetherLauncher && sudo bash install.sh
```

> **Nota**: O script `install.sh` agora configura automaticamente todas as novas dependências (Java 17, bibliotecas de download, etc.).

---

## 🗑️ Desinstalação Total

Se você deseja remover o launcher e todos os seus arquivos:

```bash
sudo bash /opt/aetherlauncher/uninstall.sh
```

---

## 📂 Estrutura do Projeto

- `src/main.py`: Interface gráfica e lógica de fluxo.
- `src/utils.py`: Motor de compatibilidade e utilitários de sistema.
- `AetherLauncher.sh`: Script de inicialização otimizado.
- `install.sh`: Instalador automatizado.

---
**Desenvolvido e Mantido por [DragonSCPOFICIAL](https://github.com/DragonSCPOFICIAL)**
