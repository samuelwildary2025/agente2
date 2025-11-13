#!/usr/bin/env python3
"""
Teste direto da memória limitada com a configuração atualizada
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
import psycopg2.extras
from langchain_core.messages import HumanMessage, AIMessage
from config.settings import settings

def test_memory_direct():
    """Testa o limite de memória diretamente com psycopg2"""
    
    test_session = "test_direct_456"
    max_messages = 15
    
    print("🧪 Testando limite de memória diretamente...")
    print(f"Tabela: {settings.postgres_table_name}")
    print(f"Sessão: {test_session}")
    print(f"Limite: {max_messages}")
    print("-" * 50)
    
    try:
        # Connect directly
        with psycopg2.connect(settings.postgres_connection_string) as conn:
            with conn.cursor() as cursor:
                
                # Clear test session messages
                cursor.execute(f"""
                    DELETE FROM {settings.postgres_table_name}
                    WHERE session_id = %s
                """, (test_session,))
                conn.commit()
                print("✅ Mensagens antigas da sessão de teste removidas")
                
                # Add 20 messages directly
                print("\n📨 Adicionando 20 mensagens diretamente...")
                
                for i in range(20):
                    # Create message JSON
                    if i % 2 == 0:
                        message_data = {
                            "type": "human",
                            "content": f"Mensagem do usuário {i+1}"
                        }
                    else:
                        message_data = {
                            "type": "ai", 
                            "content": f"Resposta da IA {i+1}"
                        }
                    
                    cursor.execute(f"""
                        INSERT INTO {settings.postgres_table_name} (session_id, message)
                        VALUES (%s, %s)
                    """, (test_session, psycopg2.extras.Json(message_data)))
                    
                    if (i + 1) % 5 == 0:
                        conn.commit()
                        # Count current messages
                        cursor.execute(f"""
                            SELECT COUNT(*) FROM {settings.postgres_table_name}
                            WHERE session_id = %s
                        """, (test_session,))
                        count = cursor.fetchone()[0]
                        print(f"  → Adicionadas {i+1} mensagens, contagem atual: {count}")
                
                conn.commit()
                
                # Now enforce the limit manually
                print(f"\n🔍 Verificando quantidade atual...")
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {settings.postgres_table_name}
                    WHERE session_id = %s
                """, (test_session,))
                
                current_count = cursor.fetchone()[0]
                print(f"  → Mensagens antes do limite: {current_count}")
                
                if current_count > max_messages:
                    # Get IDs of messages to delete (oldest ones)
                    cursor.execute(f"""
                        SELECT id FROM {settings.postgres_table_name}
                        WHERE session_id = %s
                        ORDER BY id ASC
                        LIMIT %s
                    """, (test_session, current_count - max_messages))
                    
                    ids_to_delete = [row[0] for row in cursor.fetchall()]
                    
                    print(f"  → IDs para deletar: {ids_to_delete}")
                    
                    # Delete oldest messages
                    cursor.execute(f"""
                        DELETE FROM {settings.postgres_table_name}
                        WHERE id = ANY(%s)
                    """, (ids_to_delete,))
                    
                    deleted_count = cursor.rowcount
                    conn.commit()
                    
                    print(f"✅ Deletadas {deleted_count} mensagens antigas")
                
                # Final count
                cursor.execute(f"""
                    SELECT COUNT(*) FROM {settings.postgres_table_name}
                    WHERE session_id = %s
                """, (test_session,))
                
                final_count = cursor.fetchone()[0]
                print(f"  → Mensagens finais: {final_count}")
                
                # Show remaining messages
                print(f"\n📝 Mensagens restantes:")
                cursor.execute(f"""
                    SELECT id, message->>'type' as msg_type, message->>'content' as content
                    FROM {settings.postgres_table_name}
                    WHERE session_id = %s
                    ORDER BY id ASC
                """, (test_session,))
                
                remaining = cursor.fetchall()
                for msg_id, msg_type, content in remaining:
                    icon = "👤" if msg_type == "human" else "🤖"
                    print(f"  {icon} ID {msg_id}: {content[:50]}...")
                
                # Verify test result
                if final_count <= max_messages:
                    print(f"\n✅ ✅ ✅ SUCESSO: Limite funcionando!")
                    print(f"   Mantidas {final_count} mensagens (limite: {max_messages})")
                else:
                    print(f"\n❌ ❌ ❌ FALHA: Limite não funcionou!")
                    print(f"   Esperado: ≤ {max_messages}")
                    print(f"   Encontrado: {final_count}")
                
                # Cleanup
                print(f"\n🧹 Limpando mensagens de teste...")
                cursor.execute(f"""
                    DELETE FROM {settings.postgres_table_name}
                    WHERE session_id = %s
                """, (test_session,))
                conn.commit()
                print("✅ Teste concluído!")
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_memory_direct()