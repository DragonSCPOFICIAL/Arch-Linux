# BRX AI - Agente Autônomo Nativo para Linux

O **BRX AI** é um ecossistema de inteligência artificial de alto nível, projetado para operar nativamente no Linux. Ele utiliza arquiteturas avançadas inspiradas no **DeepSeek-V3** para automação de sistemas, desenvolvimento de baixo nível e evolução autônoma de parâmetros.

## 🚀 Motor de Evolução Autônoma (Autonomous Engine)

O projeto agora conta com um **Motor de Evolução Contínua** que minera conhecimentos técnicos e injeta parâmetros reais no núcleo do agente.

### Funcionalidades Atuais:
- **Extração DeepSeek Core**: Integração real com parâmetros de arquitetura MoE (Mixture-of-Experts) e MLA (Multi-head Latent Attention).
- **Expansão Massiva de Conhecimento**: Injeção automática de otimizações para C++, Rust, Assembly e Kernel Linux.
- **Sincronização GitHub**: Atualizações em tempo real do arquivo `agent_config.json` via automação.
- **Hardware Aware**: Otimizações focadas em AVX-512, HugePages e IO_uring.

## 🧠 Brain Core (Núcleo de Inteligência)

O "Cérebro" do agente reside em `brain_core/params/agent_config.json`. Este arquivo é expandido dinamicamente pelo motor de evolução, aumentando a base de conhecimento técnica e a versão do agente a cada ciclo de análise.

### Parâmetros Monitorados:
- **Especializações**: Novas linguagens e técnicas de otimização adquiridas.
- **Technical Parameters**: Logs estruturados de cada nova descoberta injetada.
- **Versão**: Evolução incremental (ex: `3.0.x-CORE`) baseada em novos marcos de conhecimento.

## 🛠️ Instalação e Uso

Para instalar o BRX AI como um programa nativo no seu sistema:

1. **Acesse a pasta do projeto**:
   ```bash
   cd ~/Arch-Linux/BRX_AI
   ```

2. **Execute o instalador**:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### O que a instalação faz:
- Configura um ambiente Python isolado.
- Instala dependências críticas (Torch, Transformers, eBPF tools).
- Registra o comando `brx-ai` globalmente no sistema.

## 📈 Próximos Passos
- Implementação de análise de hardware em tempo real para ajuste fino de parâmetros.
- Expansão da base de conhecimento para sistemas distribuídos.
- Integração profunda com o kernel via módulos eBPF.

---
**Desenvolvido por DragonSCPOFICIAL & Manus AI**
