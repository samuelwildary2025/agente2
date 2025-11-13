#!/usr/bin/env python3
"""
Teste da configuração de limite via variável de ambiente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

def test_configurable_limit():
    """Testa o limite configurável via variável de ambiente"""
    
    print("🧪 Testando limite configurável via ENV...")
    print(f"Limite atual: {settings.postgres_message_limit} mensagens")
    print(f"Tabela: {settings.postgres_table_name}")
    print("-" * 50)
    
    # Test session
    test_session = "test_config_789"
    
    # Create memory with configurable limit
    memory = LimitedPostgresChatMessageHistory(
        session_id=test_session,
        connection_string=settings.postgres_connection_string,
        table_name=settings.postgres_table_name,
        max_messages=settings.postgres_message_limit
    )
    
    # Clear test messages
    memory.clear()
    print("✅ Mensagens de teste anteriores limpas")
    
    # Add more messages than the limit
    total_messages = settings.postgres_message_limit + 5
    print(f"\n📨 Adicionando {total_messages} mensagens (limite é {settings.postgres_message_limit})...")
    
    for i in range(total_messages):
        if i % 2 == 0:
            message = HumanMessage(content=f"Mensagem do usuário {i+1}")
        else:
            message = AIMessage(content=f"Resposta da IA {i+1}")
        
        memory.add_message(message)
        
        if (i + 1) % 5 == 0:
            print(f"  → Adicionadas {i+1} mensagens")
    
    # Test the messages property (what the agent sees)
    print(f"\n🔍 Verificando o que o agente receberá...")
    
    agent_messages = memory.messages
    total_stored = memory.get_message_count()
    
    print(f"  → Total armazenado no BD: {total_stored}")
    print(f"  → Mensagens para o agente: {len(agent_messages)}")
    
    # Show first few messages the agent will see
    print(f"\n📝 Primeiras 5 mensagens que o agente receberá:")
    for i, msg in enumerate(agent_messages[:5], 1):
        icon = "👤" if isinstance(msg, HumanMessage) else "🤖"
        print(f"  {i}. {icon} {msg.content[:40]}...")
    
    # Show last few messages
    print(f"\n📝 Últimas 5 mensagens que o agente receberá:")
    for i, msg in enumerate(agent_messages[-5:], len(agent_messages)-4):
        icon = "👤" if isinstance(msg, HumanMessage) else "🤖"
        print(f"  {i}. {icon} {msg.content[:40]}...")
    
    # Verify configuration is working
    if len(agent_messages) <= settings.postgres_message_limit:
        print(f"\n✅ ✅ ✅ SUCESSO: Configuração funcionando!")
        print(f"   Armazenado: {total_stored} mensagens")
        print(f"   Para agente: {len(agent_messages)} mensagens")
        print(f"   Limite configurado: {settings.postgres_message_limit}")
    else:
        print(f"\n❌ ❌ ❌ FALHA: Configuração não aplicada!")
    
    # Test different limit via environment (simulate)
    print(f"\n🔄 Testando com limite diferente (simulação)...")
    
    # Create memory with different limit
    memory_test = LimitedPostgresChatMessageHistory(
        session_id=f"{test_session}_test5",
        connection_string=settings.postgres_connection_string,
        table_name=settings.postgres_table_name,
        max_messages=5  # Test with 5 messages
    )
    
    memory_test.clear()
    
    # Add 10 messages
    for i in range(10):
        message = HumanMessage(content=f"Test message {i+1}")
        memory_test.add_message(message)
    
    test_messages = memory_test.messages
    print(f"  → Com limite 5: {len(test_messages)} mensagens para o agente")
    
    memory_test.clear()
    
    # Cleanup
    print(f"\n🧹 Limpando testes...")
    memory.clear()
    print("✅ Teste concluído!")
    
    print(f"\n💡 Para alterar o limite, configure a variável:")
    print(f"   POSTGRES_MESSAGE_LIMIT=30  # Exemplo: 30 mensagens")
    print(f"   POSTGRES_MESSAGE_LIMIT=0   # 0 = ilimitado (padrão antigo)")

if __name__ == "__main__":
    test_configurable_limit()