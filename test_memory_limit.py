#!/usr/bin/env python3
"""
Test script para verificar o funcionamento do limite de memória do chat
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from config.settings import settings

def test_memory_limit():
    """Testa o limite de memória do chat"""
    
    # Test session ID
    test_session = "test_memory_limit_123"
    
    print("🧪 Testando limite de memória do chat...")
    print(f"Sessão de teste: {test_session}")
    print(f"Limite configurado: 15 mensagens")
    print("-" * 50)
    
    # Create limited memory instance
    memory = LimitedPostgresChatMessageHistory(
        session_id=test_session,
        connection_string=settings.postgres_connection_string,
        table_name=settings.postgres_table_name,
        max_messages=15
    )
    
    # Clear any existing messages
    memory.clear()
    print("✅ Memória limpa")
    
    # Add 20 messages (more than the limit)
    print("\n📨 Adicionando 20 mensagens (limite é 15)...")
    
    for i in range(20):
        # Alternate between human and AI messages
        if i % 2 == 0:
            message = HumanMessage(content=f"Mensagem do usuário {i+1}")
        else:
            message = AIMessage(content=f"Resposta da IA {i+1}")
        
        memory.add_message(message)
        
        # Show progress every 5 messages
        if (i + 1) % 5 == 0:
            count = memory.get_message_count()
            print(f"  → Adicionadas {i+1} mensagens, contagem atual: {count}")
    
    # Final count
    final_count = memory.get_message_count()
    session_info = memory.get_session_info()
    
    print(f"\n📊 Resultado final:")
    print(f"  → Mensagens adicionadas: 20")
    print(f"  → Mensagens armazenadas: {final_count}")
    print(f"  → Limite configurado: {session_info['max_messages']}")
    
    # Verify the limit is working
    if final_count <= 15:
        print("✅ ✅ ✅ SUCESSO: O limite de memória está funcionando!")
        print(f"   O sistema manteve apenas as {final_count} mensagens mais recentes")
    else:
        print("❌ ❌ ❌ FALHA: O limite de memória não está funcionando!")
        print(f"   Esperado: ≤ 15 mensagens")
        print(f"   Encontrado: {final_count} mensagens")
    
    # Show the actual messages
    print(f"\n📝 Mensagens armazenadas:")
    messages = memory.messages
    for i, msg in enumerate(messages, 1):
        msg_type = "👤" if isinstance(msg, HumanMessage) else "🤖"
        print(f"  {i:2d}. {msg_type} {msg.content[:50]}...")
    
    # Cleanup
    print(f"\n🧹 Limpando mensagens de teste...")
    memory.clear()
    print("✅ Teste concluído!")

if __name__ == "__main__":
    test_memory_limit()