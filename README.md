# 🤖 Agente de Supermercado - WhatsApp

Agente inteligente para atendimento automatizado de supermercado via WhatsApp com reconhecimento de áudio e timeout inteligente.

## 🚀 Funcionalidades

### ✅ **Reconhecimento de Áudio**
- Transcrição automática de mensagens de voz com OpenAI Whisper
- Suporte para áudios via URL e base64
- Tratamento robusto de erros
- Compatível com mensagens de texto e imagem

### ⏰ **Timeout Natural de 1 Hora**
- Pedidos expiram automaticamente após 1 hora de inatividade
- Verificação automática de continuidade do pedido
- Reinício natural sem necessidade de comandos
- Economia de 30% nos custos (R$ 36 → R$ 25,20/mês)

### 🎯 **Otimização de Tokens**
- Limite de 300 palavras por mensagem (~450 tokens)
- Modo economy disponível para redução de custos
- Gestão inteligente de memória de conversação

### 🔧 **Integração UAZ API**
- Webhook compatível com UAZ API
- Suporte a múltiplos formatos de payload
- Presença ("digitando...") automática
- Buffer de mensagens para agregação inteligente

## 📋 Instalação

```bash
# Clone o repositório
git clone https://github.com/samuelwildary2025/agente2.git
cd agente2

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas chaves
```

## 🔑 Configuração

### Variáveis de Ambiente Obrigatórias:
```env
# OpenAI (para transcrição de áudio)
OPENAI_API_KEY=sk-sua-chave-aqui

# Redis (para timeout e cache)
REDIS_HOST=localhost
REDIS_PORT=6379

# UAZ API (para WhatsApp)
WHATSAPP_API_URL=https://sua-instancia.uazapi.com
WHATSAPP_TOKEN=seu-token-aqui
```

## 🚀 Uso

```bash
# Iniciar o servidor
python server.py

# Testar o agente
python test_mensagens_cliente.py
```

## 📊 Economia com Timeout

| Sem Timeout | Com Timeout | Economia |
|-------------|-------------|----------|
| R$ 36,00/mês | R$ 25,20/mês | **30%** |

*Baseado em 60 pedidos/dia com 300 palavras por resposta*

## 🧪 Testes

Execute os testes para verificar as funcionalidades:

```bash
# Teste de timeout natural
python test_timeout_natural.py

# Teste de reconhecimento de áudio
python test_audio_integration.py

# Demonstração completa
python demo_audio_complete.py
```

## 🔗 Endpoints

### Webhook Principal
- `POST /webhook/whatsapp` - Recebe mensagens do WhatsApp

### Endpoints Auxiliares
- `POST /webhook/uaz` - Alias para compatibilidade UAZ
- `POST /` - Alias adicional
- `GET /health` - Health check
- `POST /agent/dryrun` - Teste direto do agente

## 📞 Fluxo de Conversa

### Exemplo com Áudio:
```
Cliente: [Áudio] "Quero 2 pacotes de arroz"
Agente: "Entendi! Você quer 2 pacotes de arroz. Quantos pacotes?"
Cliente: [Áudio] "Quero 2 pacotes"
Agente: "Perfeito! 2 pacotes de arroz anotados. Total: R$ 25,00"
```

### Exemplo com Timeout:
```
Cliente: "Quero arroz" [10:00]
# ... 1h30min depois ...
Cliente: "E café também" [11:30]
Agente: "Seu pedido anterior expirou. Vamos começar um novo pedido!"
```

## 🛠️ Arquitetura

- **FastAPI** - Servidor web assíncrono
- **LangGraph** - Orquestração do agente
- **OpenAI** - LLM e transcrição de áudio
- **Redis** - Cache e timeout
- **PostgreSQL** - Histórico de mensagens
- **UAZ API** - Integração WhatsApp

## 📈 Performance

- Processamento em background para resposta rápida
- Buffer de mensagens para evitar spam
- Cooldown de 60s após resposta do agente
- Presença automática ("digitando...")

## 🔐 Segurança

- Validação de tokens de API
- Sanitização de números de telefone
- Logs mascarados para segurança
- Sem armazenamento de dados sensíveis

## 📝 Licença

Este projeto é privado e desenvolvido para uso específico.

---

**Desenvolvido com ❤️ para automação de atendimento de supermercado**