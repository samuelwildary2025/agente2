#!/usr/bin/env python3
"""
Implementação alternativa: Detecção de timeout por timestamp no prompt

Mostra como o agente poderia detectar timeout apenas com timestamps das mensagens.
"""

def criar_prompt_com_timestamp():
    """Cria prompt que instrui o agente a detectar timeout por timestamp"""
    
    prompt_timestamp = """
# Contexto de Tempo e Timeout

Você tem acesso ao histórico de mensagens com timestamps. IMPORTANTE: 

## DETECÇÃO DE TIMEOUT POR TIMESTAMP:

1. Analise o timestamp da PRIMEIRA mensagem do histórico
2. Compare com o horário atual (sistema)
3. Se a PRIMEIRA mensagem tem mais de 1 hora (3600 segundos):
   - O pedido EXPIROU por inatividade
   - Informe o cliente educadamente
   - Reinicie o atendimento

4. Se a PRIMEIRA mensagem tem menos de 1 hora:
   - Continue normalmente
   - Renove o timeout do pedido

## MENSAGEM PARA CLIENTE APÓS TIMEOUT:

"⏰ Percebi que seu pedido anterior expirou após 1 hora de inatividade. 
Como se passou bastante tempo, precisei iniciar um novo atendimento. 
Por favor, me diga tudo que você quer começando do início. 
Estou aqui para ajudar! 😊"

## EXEMPLO DE DETECÇÃO:

Histórico:
09:15:30 - Cliente: "Oi, quero arroz"
09:16:45 - Agente: "Encontrei arroz R$ 6,90"

Cliente agora (18:45): "Vou querer feijão também"

Sua análise:
- Primeira mensagem: 09:15:30
- Hora atual: 18:45:00  
- Diferença: 9 horas e 30 minutos
- Conclusão: PEDIDO EXPIROU (mais de 1 hora)
- Ação: Informar timeout e reiniciar

## REGRAS IMPORTANTES:

✅ SEMPRE analise timestamp antes de processar mensagens
✅ SEMPRE informe timeout de forma amigável  
✅ NUNCA mencione produtos do pedido expirado
✅ SEMPRE convide a refazer pedido do início
✅ USE o contexto anterior (preços, preferências) se útil

## FORMATO DE TIMESTAMP:

As mensagens têm este formato:
{
  "type": "human",
  "content": "mensagem",
  "timestamp": "2024-11-16 09:15:30"
}

Analise o campo "timestamp" para detectar timeout.
"""
    
    return prompt_timestamp

def comparar_abordagens():
    """Compara as duas abordagens: Tool vs Timestamp no Prompt"""
    
    print("🔍 COMPARAÇÃO: Tool vs Timestamp no Prompt")
    print("="*70)
    
    print("\n✅ ABORDAGEM ATUAL (com tool):")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Agente: Preciso verificar timeout                        │")
    print("│ Ferramenta: verificar_continuar_pedido_tool()            │")
    print("│ Redis: Retorna 'expirou' ou 'ativo'                     │")
    print("│ Agente: Recebe resposta pronta                         │")
    print("│ Resultado: Simples e direto                            │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    print("\n💡 SUA SUGESTÃO (timestamp no prompt):")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│ Agente: Analiso timestamps das mensagens                 │")
    print("│ Prompt: 'Compare primeira msg com hora atual'          │")
    print("│ Agente: Calcula diferença de tempo                     │")
    print("│ Agente: Decide se expirou ou não                       │")
    print("│ Resultado: Mais complexo mas sem tool extra            │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    print("\n📊 VANTAGENS E DESVANTAGENS:")
    print("─"*50)
    
    print("\n✅ COM TOOL:")
    print("• Simples: Agente só pergunta, Redis responde")
    print("• Confiável: TTL é exato em segundos")
    print("• Rápido: Redis.get() é instantâneo")
    print("• Separado: Timeout não mistura com lógica de chat")
    print("• Escalável: Funciona com milhares de clientes")
    
    print("\n💡 COM TIMESTAMP NO PROMPT:")
    print("• Sem tool extra: Só precisa do prompt")
    print("• Inteligente: Agente entende contexto de tempo")
    print("• Flexível: Pode ajustar lógica facilmente")
    print("• Mas complexo: Agente precisa calcular e decidir")
    print("• Menos confiável: Depende de timestamp preciso")

def mostrar_exemplo_timestamp():
    """Mostra como ficaria o exemplo com timestamp no prompt"""
    
    print("\n" + "="*70)
    print("💬 EXEMPLO: Timestamp no Prompt")
    print("="*70)
    
    print("\n🕘 09:15 - Mensagens no histórico:")
    mensagens = [
        {"type": "human", "content": "Oi, quero arroz", "timestamp": "2024-11-16 09:15:30"},
        {"type": "ai", "content": "Encontrei arroz R$ 6,90", "timestamp": "2024-11-16 09:16:45"},
        {"type": "human", "content": "Quero 2 pacotes", "timestamp": "2024-11-16 09:17:20"}
    ]
    
    for i, msg in enumerate(mensagens, 1):
        print(f"{i}. {msg['timestamp']} - {msg['type']}: {msg['content']}")
    
    print(f"\n⏰ Primeira mensagem: {mensagens[0]['timestamp']}")
    print(f"⏰ Hora atual simulada: 2024-11-16 18:45:00")
    print(f"📊 Diferença: 9 horas e 30 minutos")
    
    print("\n🤖 Agente com prompt de timestamp:")
    print("'Analisando timestamps... primeira mensagem tem 9 horas!'")
    print("'PEDIDO EXPIROU! Mais de 1 hora de inatividade.'")
    print("'Vou informar o cliente e reiniciar o atendimento...'")
    
    print("\n💬 Resposta do agente:")
    print("🤖 Agente: ⏰ Percebi que seu pedido anterior expirou após 1 hora de inatividade.")
    print("🤖 Agente: Como se passou bastante tempo, precisei iniciar um novo atendimento.")
    print("🤖 Agente: Vi que você pediu arroz esta manhã! Quer arroz e feijão então?")

def main():
    prompt = criar_prompt_com_timestamp()
    comparar_abordagens()
    mostrar_exemplo_timestamp()
    
    print("\n" + "="*70)
    print("🎯 CONCLUSÃO:")
    print("Você está certo! Timestamp no prompt FUNCIONARIA!")
    print("Mas a tool é mais simples e confiável para produção.")
    print("Sua ideia é inteligente e poderia ser implementada! 👍")

if __name__ == "__main__":
    main()