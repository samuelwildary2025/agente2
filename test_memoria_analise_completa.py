#!/usr/bin/env python3
"""
Análise completa da memória do agente
"""

import psycopg
from config.settings import settings
from langchain_community.chat_message_histories import PostgresChatMessageHistory

def analisar_memoria_completa():
    """Análise detalhada da memória do agente"""
    
    print("🧠 ANÁLISE COMPLETA DA MEMÓRIA DO AGENTE")
    print("="*70)
    
    try:
        conn = psycopg.connect(settings.postgres_connection_string)
        cursor = conn.cursor()
        
        # Estatísticas gerais
        cursor.execute(f'SELECT COUNT(*) FROM {settings.postgres_table_name}')
        total_mensagens = cursor.fetchone()[0]
        
        cursor.execute(f'SELECT COUNT(DISTINCT session_id) FROM {settings.postgres_table_name}')
        total_sessoes = cursor.fetchone()[0]
        
        print(f"📊 Estatísticas Gerais:")
        print(f"   Total de mensagens: {total_mensagens}")
        print(f"   Total de sessões (telefones): {total_sessoes}")
        print(f"   Média de mensagens por sessão: {total_mensagens/total_sessoes:.1f}")
        
        # Distribuição por sessão
        cursor.execute(f'''
            SELECT session_id, COUNT(*) as msg_count
            FROM {settings.postgres_table_name} 
            GROUP BY session_id 
            ORDER BY msg_count DESC 
        ''')
        sessoes = cursor.fetchall()
        
        print(f"\\n📱 Detalhes por Sessão:")
        for i, (session, count) in enumerate(sessoes, 1):
            print(f"   {i}. {session[:20]}... - {count} mensagens")
        
        # Ver padrão de mensagens (última sessão ativa)
        if sessoes:
            ultima_sessao = sessoes[0][0]
            
            print(f"\\n💬 Análise da Sessão Mais Ativa ({ultima_sessao[:20]}...):")
            
            cursor.execute(f'''
                SELECT id, message 
                FROM {settings.postgres_table_name} 
                WHERE session_id = %s 
                ORDER BY id 
            ''', (ultima_sessao,))
            
            mensagens = cursor.fetchall()
            
            # Parse das mensagens
            import json
            mensagens_parseadas = []
            for msg in mensagens:
                try:
                    msg_data = json.loads(msg[1].replace('\'', '\"'))
                    tipo = msg_data.get('type', 'unknown')
                    conteudo = msg_data.get('data', {}).get('content', '')
                    mensagens_parseadas.append({
                        'id': msg[0],
                        'tipo': tipo,
                        'conteudo': conteudo
                    })
                except:
                    mensagens_parseadas.append({
                        'id': msg[0],
                        'tipo': 'raw',
                        'conteudo': str(msg[1])[:100]
                    })
            
            print(f"   Sequência de mensagens:")
            for i, msg in enumerate(mensagens_parseadas, 1):
                tipo_emoji = "👤" if msg['tipo'] == 'human' else "🤖"
                print(f"      {i}. {tipo_emoji} {msg['conteudo'][:60]}...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def verificar_limitacao_memoria():
    """Verifica se há limitação de memória no LangChain"""
    
    print(f"\\n🔍 VERIFICANDO LIMITAÇÕES DE MEMÓRIA")
    print("="*70)
    
    # Testar comportamento com uma sessão
    telefone_teste = "5585999999999"
    
    history = PostgresChatMessageHistory(
        connection_string=settings.postgres_connection_string,
        session_id=telefone_teste,
        table_name=settings.postgres_table_name
    )
    
    print(f"📋 Comportamento Padrão do PostgresChatMessageHistory:")
    print(f"   ✅ Armazena TODAS as mensagens de uma sessão")
    print(f"   ✅ Não tem limite configurado por padrão")
    print(f"   ✅ Mantém histórico completo da conversa")
    
    # Verificar quantas mensagens existem para este telefone
    try:
        conn = psycopg.connect(settings.postgres_connection_string)
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT COUNT(*) 
            FROM {settings.postgres_table_name} 
            WHERE session_id = %s
        ''', (telefone_teste,))
        
        count = cursor.fetchone()[0]
        print(f"\\n📊 Mensagens existentes para {telefone_teste}: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"   Erro ao verificar: {e}")
    
    print(f"\\n💡 IMPORTANTE:")
    print(f"   O LangChain não limita automaticamente o número de mensagens")
    print(f"   Mas o contexto do LLM tem limite de tokens (geralmente 4k-8k)")
    print(f"   Com muitas mensagens, o agente pode ficar lento ou exceder tokens")

def sugerir_melhorias():
    """Sugere melhorias para gerenciamento de memória"""
    
    print(f"\\n💡 SUGESTÕES DE MELHORIA")
    print("="*70)
    
    print(f"🎯 Problema Potencial:")
    print(f"   Com muitas mensagens, o contexto fica muito longo")
    print(f"   Isso pode causar:")
    print(f"   - Lentidão nas respostas")
    print(f"   - Exceder limite de tokens do LLM")
    print(f"   - Custo maior em tokens de entrada")
    
    print(f"\\n🔧 Soluções Possíveis:")
    print(f"   1. Limitar a últimas N mensagens (ex: 10-20)")
    print(f"   2. Resumir conversas antigas")
    print(f"   3. Limpar mensagens antigas automaticamente")
    print(f"   4. Usar memória resumida por sessão")
    
    print(f"\\n📋 Implementação Recomendada:")
    print(f"   - Manter últimas 10-15 mensagens por sessão")
    print(f"   - Limpar mensagens com mais de 24h")
    print(f"   - Adicionar configuração de limite no settings.py")

if __name__ == "__main__":
    analisar_memoria_completa()
    verificar_limitacao_memoria()
    sugerir_melhorias()