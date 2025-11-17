#!/usr/bin/env python3
"""
Teste: Verificar se o agente pode identificar mensagens antigas por timestamp

Analisa se o PostgreSQL armazena timestamps e como o agente poderia usá-los.
"""

def analisar_estrutura_mensagens():
    """Analisa como as mensagens são estruturadas"""
    
    print("🔍 ANÁLISE: Timestamp nas Mensagens do PostgreSQL")
    print("="*70)
    
    print("\n📋 ESTRUTURA TÍPICA DA TABELA message_store/memoria:")
    print("┌─────────────┬──────────────┬─────────────────────┐")
    print("│ Campo       │ Tipo         │ Descrição           │")
    print("├─────────────┼──────────────┼─────────────────────┤")
    print("│ id          │ SERIAL/INT   │ ID único da msg     │")
    print("│ session_id  │ VARCHAR      │ ID da sessão        │")
    print("│ message     │ JSONB        │ Conteúdo da msg     │")
    print("│ created_at  │ TIMESTAMP    │ ⏰ QUANDO foi criada │")
    print("└─────────────┴──────────────┴─────────────────────┘")
    
    print("\n💡 A TABELA TEM TIMESTAMP! Mas o agente não usa...")
    
    print("\n🔍 EXEMPLO DE MENSAGEM COM TIMESTAMP:")
    exemplo_mensagem = {
        "type": "human",
        "content": "Oi, quero arroz",
        "timestamp": "2024-11-16 09:15:30"
    }
    
    print(f"📄 Mensagem JSON: {exemplo_mensagem}")
    print("⏰ Timestamp está disponível!")

def mostrar_possivel_implementacao():
    """Mostra como poderia funcionar com timestamp"""
    
    print("\n" + "="*70)
    print("🤖 IMPLEMENTAÇÃO ALTERNATIVA: Detecção por Timestamp")
    print("="*70)
    
    print("\n💭 LÓGICA SEM TOOL (usando timestamp):")
    print("""
    def verificar_timeout_por_timestamp(telefone, mensagens):
        # Pegar timestamp da mensagem mais antiga
        primeira_msg = mensagens[0]  # Primeira mensagem
        tempo_primeira = primeira_msg.get('timestamp', 'agora')
        
        # Calcular diferença de tempo
        agora = datetime.now()
        diferenca = agora - tempo_primeira
        
        # Se passou mais de 1 hora
        if diferenca > timedelta(hours=1):
            return "Pedido expirou por inatividade"
        else:
            return "Pedido ativo"
    """)
    
    print("\n📊 COMPARAÇÃO: Tool vs Timestamp")
    print("─"*50)
    
    print("✅ COM TOOL (atual):")
    print("• Redis controla timeout independente")
    print("• Agente não precisa calcular tempo")
    print("• Sistema mais simples e confiável")
    print("• Timeout é exato e imediato")
    
    print("\n❌ COM TIMESTAMP (sem tool):")
    print("• Agente precisa calcular diferença de tempo")
    print("• Depende de timestamp preciso nas mensagens")
    print("• Mais complexo para detectar inatividade")
    print("• Pode ter problemas com fuso horário")

def explicar_porque_tool_eh_melhor():
    """Explica por que a tool é melhor que timestamp"""
    
    print("\n" + "="*70)
    print("🎯 POR QUE A TOOL É MELHOR QUE TIMESTAMP")
    print("="*70)
    
    print("\n1️⃣ CONFIABILIDADE:")
    print("   ✅ Tool: Redis TTL é exato (segundos precisos)")
    print("   ❌ Timestamp: Depende de relógio do sistema")
    
    print("\n2️⃣ PERFORMANCE:")
    print("   ✅ Tool: Verificação instantânea (Redis.get())")
    print("   ❌ Timestamp: Calcula diferença toda vez")
    
    print("\n3️⃣ SIMPLICIDADE:")
    print("   ✅ Tool: Agente só pergunta 'pedido expirou?'")
    print("   ❌ Timestamp: Agente precisa analisar histórico")
    
    print("\n4️⃣ ESCABILIDADE:")
    print("   ✅ Tool: Redis é ultra-rápido para milhares de verificações")
    print("   ❌ Timestamp: Consulta e cálculo para cada mensagem")
    
    print("\n5️⃣ MANUTENÇÃO:")
    print("   ✅ Tool: Sistema independente, fácil de debugar")
    print("   ❌ Timestamp: Mistura lógica de timeout com lógica de chat")

def main():
    analisar_estrutura_mensagens()
    mostrar_possivel_implementacao()
    explicar_porque_tool_eh_melhor()
    
    print("\n" + "="*70)
    print("🏆 CONCLUSÃO:")
    print("A tool é melhor porque é mais simples, rápida e confiável!")
    print("O timestamp existe, mas usar a tool é a escolha certa!")

if __name__ == "__main__":
    main()