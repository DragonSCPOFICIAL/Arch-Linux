# BRX AI - Guia Rápido de Instalação

## Instalação em 3 Passos

### 1. Navegue até o diretório
```bash
cd /caminho/para/brx_ai_improved
```

### 2. Execute o instalador
```bash
sudo bash install.sh
```

### 3. Inicie a aplicação
```bash
brx_ai_app
```

## Alternativas de Inicialização

### Via Terminal
```bash
brx_ai_app
```

### Via Menu de Aplicativos
Procure por "BRX AI Agent" no menu de aplicativos do seu desktop.

### Via Atalho
Clique no atalho criado em `~/.local/share/applications/brx_ai_app.desktop`

## Desinstalação

```bash
sudo /opt/brx_ai_app/uninstall.sh
```

## Troubleshooting

### Erro: "Python 3 não encontrado"
```bash
# Arch Linux
sudo pacman -S python

# Debian/Ubuntu
sudo apt install python3
```

### Erro: "tkinter não encontrado"
```bash
# Arch Linux
sudo pacman -S tk

# Debian/Ubuntu
sudo apt install python3-tk
```

### Erro: "Permissão negada"
```bash
sudo bash install.sh
```

## Verificar Instalação

```bash
# Verificar se está instalado
which brx_ai_app

# Ver logs
tail -f ~/.brx_ai_app.log

# Verificar diretório de instalação
ls -la /opt/brx_ai_app
```

## Próximos Passos

1. Leia o README.md para mais informações
2. Consulte ARCHITECTURE.md para entender a estrutura
3. Veja DEVELOPMENT.md para contribuir

---

**Versão**: 2.0.0
