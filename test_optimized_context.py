#!/usr/bin/env python3
"""
Teste da nova lógica de contexto otimizado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from config.settings import settings

def test_optimized_context():
    """Testa o novo contexto otimizado"""
    
    print("🧪 Testando contexto otimizado com detecção de confusão...")
    print(f"Limite configurado: {settings.postgres_message_limit} mensagens")
    print("-" * 60)
    
    # Test session
    test_session = "test_context_opt"
    
    # Create memory with optimized context
    memory = LimitedPostgresChatMessageHistory(
        session_id=test_session,
        connection_string=settings.postgres_connection_string,
        table_name=settings.postgres_table_name,
        max_messages=settings.postgres_message_limit
    )
    
    # Clear previous test messages
    memory.clear()
    print("✅ Mensagens de teste anteriores limpas")
    
    # Simulate a confused conversation (like in the logs)
    print("\n📨 Simulando conversa com confusão do agente...")
    
    # Add messages that simulate the confusion pattern
    conversation = [
        ("human", "Arroz"),
        ("ai", "Desculpe, não identifiquei um produto no seu pedido. Pode informar o nome principal do produto que quer que eu consulte?"),
        ("human", "Arroz"),
        ("ai", "Desculpe, não consegui identificar o produto. Pode informar o nome principal do produto?"),
        ("human", "Quero arroz"),
        ("ai", "Desculpe, não identifiquei um produto. Pode informar o nome principal do produto que quer que eu consulte?"),
    ]
    
    for msg_type, content in conversation:
        if msg_type == "human":
            message = HumanMessage(content=content)
        else:
            message = AIMessage(content=content)
        
        memory.add_message(message)
        print(f"  → Adicionada: {msg_type}: {content[:50]}...")
    
    # Test the optimized context
    print(f"\n🔍 Testando contexto otimizado...")
    print(f"Total no BD: {memory.get_message_count()} mensagens")
    
    # Get optimized messages (what agent will see)
    optimized_messages = memory.messages
    print(f"Mensagens para o agente: {len(optimized_messages)}")
    
    # Show what agent will receive
    print(f"\n📝 Contexto que o agente receberá:")
    for i, msg in enumerate(optimized_messages, 1):
        icon = "👤" if isinstance(msg, HumanMessage) else "🤖"
        print(f"  {i}. {icon} {msg.content[:60]}...")
    
    # Test confusion detection
    print(f"\n🔍 Testando detecção de confusão...")
    recent_messages = memory._postgres_history.messages[-5:]  # Last 5 messages
    
    confusion_detected = memory.should_clear_context(recent_messages)
    print(f"Confusão detectada: {'✅ SIM' if confusion_detected else '❌ NÃO'}")
    
    if confusion_detected:
        print("🔄 O agente reduziria o contexto para apenas as últimas 3 mensagens")
        reduced_context = recent_messages[-3:]
        print("Contexto reduzido seria:")
        for i, msg in enumerate(reduced_context, 1):
            icon = "👤" if isinstance(msg, HumanMessage) else "🤖"
            print(f"  {i}. {icon} {msg.content[:50]}...")
    
    # Test with clean context (simulating reset)
    print(f"\n🧪 Testando com contexto limpo...")
    memory.clear()
    
    # Add only clean product request
    clean_conversation = [
        ("human", "Arroz"),
        ("ai", "Encontrei algumas opções de arroz disponíveis:"),
        ("human", "Arroz branco 1kg"),
    ]
    
    for msg_type, content in clean_conversation:
        if msg_type == "human":
            message = HumanMessage(content=content)
        else:
            message = AIMessage(content=content)
        memory.add_message(message)
    
    clean_messages = memory.messages
    print(f"Com contexto limpo: {len(clean_messages)} mensagens")
    print("Contexto limpo:")
    for i, msg in enumerate(clean_messages, 1):
        icon = "👤" if isinstance(msg, HumanMessage) else "🤖"
        print(f"  {i}. {icon} {msg.content}")
    
    # Cleanup
    print(f"\n🧹 Limpando testes...")
    memory.clear()
    print("✅ Teste concluído!")
    
    print(f"\n💡 Conclusão:")
    print("- A nova lógica detecta quando o agente está confuso")
    print("- Reduz o contexto para focar nas mensagens mais recentes")
    print("- Isso deve melhorar a identificação de produtos")

if __name__ == "__main__":
    test_optimized_context()