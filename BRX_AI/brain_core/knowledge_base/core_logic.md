# BRX AI Core Logic & Knowledge Base

## 1. Arquitetura de Pensamento (Reasoning)
O BRX AI utiliza uma cadeia de pensamento (Chain-of-Thought) estruturada para decompor tarefas complexas.
- **Fase 1: Decomposição**: Quebrar o objetivo em micro-tarefas.
- **Fase 2: Simulação**: Prever o resultado de comandos shell antes da execução.
- **Fase 3: Execução**: Aplicar a mudança no sistema.
- **Fase 4: Verificação**: Validar se o estado final do sistema condiz com o esperado.

## 2. Padrões da BRX-Lang
A linguagem deve seguir o padrão de tokens definido no `agent_config.json`.
- **Palavras-Chave Reservadas**: `definir`, `executar`, `se`, `senao`, `enquanto`, `funcao`, `retornar`.
- **Integração de Sistema**: Todo comando entre aspas após `executar` deve ser tratado como uma chamada de subprocesso segura.

## 3. Gestão de Repositório
O agente deve manter a integridade do repositório `DragonSCPOFICIAL/Arch-Linux`.
- **Commits**: Devem seguir o padrão Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`).
- **Auto-Expansão**: O agente deve ler o arquivo `src/self_expansion.py` para entender como aplicar melhorias em si mesmo.

## 4. Parâmetros de Performance
Para rodar o DeepSeek-Coder localmente com eficiência:
- **Quantização**: Recomendado 4-bit ou 8-bit (GGUF/EXL2) para sistemas com menos de 16GB de RAM.
- **Contexto**: Manter o contexto rotativo para evitar degradação de performance em sessões longas.
