#!/usr/bin/env python3
"""
Teste para verificar quantas mensagens o agente está usando da memória
"""

import psycopg
from config.settings import settings
from langchain_community.chat_message_histories import PostgresChatMessageHistory

def verificar_memoria_detalhada():
    """Verifica detalhes da memória do PostgreSQL"""
    
    print("🔍 VERIFICANDO MEMÓRIA DO AGENTE")
    print("="*60)
    
    try:
        conn = psycopg.connect(settings.postgres_connection_string)
        cursor = conn.cursor()
        
        # Ver estrutura completa da tabela
        cursor.execute(f'''
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = \'{settings.postgres_table_name}\' 
            ORDER BY ordinal_position
        ''')
        columns = cursor.fetchall()
        print(f'📊 Estrutura da tabela {settings.postgres_table_name}:')
        for col in columns:
            print(f'  {col[0]}: {col[1]} (nullable: {col[2]})')
        
        # Total de mensagens
        cursor.execute(f'SELECT COUNT(*) FROM {settings.postgres_table_name}')
        total_messages = cursor.fetchone()[0]
        print(f'\\n📈 Total de mensagens armazenadas: {total_messages}')
        
        # Mensagens por sessão (telefone)
        cursor.execute(f'''
            SELECT session_id, COUNT(*) as msg_count,
                   MIN(created_at) as primeira_msg,
                   MAX(created_at) as ultima_msg
            FROM {settings.postgres_table_name} 
            GROUP BY session_id 
            ORDER BY msg_count DESC 
            LIMIT 5
        ''')
        sessions = cursor.fetchall()
        
        print(f'\\n📱 Top 5 sessões (telefones) com mais mensagens:')
        for i, (session, count, primeira, ultima) in enumerate(sessions, 1):
            print(f'  {i}. Telefone: {session[:15]}...')
            print(f'     Mensagens: {count}')
            print(f'     Primeira: {primeira}')
            print(f'     Última: {ultima}')
            print()
        
        # Ver mensagens de uma sessão específica
        if sessions:
            sessao_mais_ativa = sessions[0][0]
            print(f'💬 Mensagens da sessão mais ativa ({sessao_mais_ativa[:15]}...):')
            
            cursor.execute(f'''
                SELECT id, message, created_at 
                FROM {settings.postgres_table_name} 
                WHERE session_id = %s 
                ORDER BY id DESC 
                LIMIT 5
            ''', (sessao_mais_ativa,))
            
            mensagens = cursor.fetchall()
            for msg in mensagens:
                msg_data = eval(msg[1])  # O message é uma string JSON
                msg_tipo = msg_data.get('type', 'unknown')
                msg_conteudo = msg_data.get('data', {}).get('content', '')[:60]
                print(f'   {msg[0]}: [{msg_tipo}] {msg_conteudo}...')
        
        conn.close()
        
    except Exception as e:
        print(f'❌ Erro: {e}')

def testar_limite_memoria():
    """Testa se há limite de mensagens por sessão"""
    
    print("\\n🧪 TESTANDO LIMITES DE MEMÓRIA")
    print("="*60)
    
    try:
        # Testar com uma sessão específica
        telefone_teste = "5585999999999"
        
        history = PostgresChatMessageHistory(
            connection_string=settings.postgres_connection_string,
            session_id=telefone_teste,
            table_name=settings.postgres_table_name
        )
        
        # Adicionar várias mensagens de teste
        print(f"Adicionando 10 mensagens de teste para {telefone_teste}...")
        
        for i in range(1, 6):
            history.add_user_message(f"Mensagem de teste {i}")
            history.add_ai_message(f"Resposta do agente {i}")
        
        # Ver quantas mensagens foram armazenadas
        messages = history.messages
        print(f"✅ Mensagens armazenadas: {len(messages)}")
        
        # Ver últimas mensagens
        print(f"\\nÚltimas 3 mensagens:")
        for msg in messages[-3:]:
            tipo = "Usuário" if msg.type == "human" else "Agente"
            print(f"   [{tipo}]: {msg.content[:50]}...")
        
        # Limpar mensagens de teste
        print(f"\\n🧹 Limpando mensagens de teste...")
        conn = psycopg.connect(settings.postgres_connection_string)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {settings.postgres_table_name} WHERE session_id = %s', (telefone_teste,))
        conn.commit()
        conn.close()
        print(f"✅ Mensagens de teste removidas")
        
    except Exception as e:
        print(f'❌ Erro no teste: {e}')

if __name__ == "__main__":
    verificar_memoria_detalhada()
    testar_limite_memoria()