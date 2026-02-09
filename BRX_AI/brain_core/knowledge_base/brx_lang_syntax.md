# BRX-Lang: Sintaxe e Gramática (v0.1.0)

A BRX-Lang é uma linguagem de programação de alto nível, otimizada para automação de sistemas Linux e integração nativa com o Agente BRX AI.

## Princípios de Design
- **Simplicidade**: Sintaxe limpa e legível.
- **Poder do Sistema**: Comandos de sistema são cidadãos de primeira classe.
- **IA-Native**: Projetada para ser facilmente gerada e lida por modelos DeepSeek.

## Estrutura Básica

### Variáveis e Tipos
```brx
definir nome = "BRX AI"
definir versao = 2.0
```

### Comandos de Sistema Integrados
```brx
executar "ls -la" -> lista_arquivos
exibir lista_arquivos
```

### Estruturas de Controle
```brx
se versao > 1.0 {
    exibir "Sistema Atualizado"
} senao {
    exibir "Necessita Atualização"
}
```

### Funções de Automação
```brx
funcao backup_sistema() {
    sistema.notificar("Iniciando Backup")
    executar "tar -czf backup.tar.gz /home/user"
}
```

## Próximos Passos
1. Implementar o parser inicial em Python.
2. Criar o executor de scripts `.brx`.
3. Integrar com o `intent_map.py` para reconhecimento automático.
