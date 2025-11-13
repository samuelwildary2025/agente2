#!/usr/bin/env python3
"""
Configuração de limite de memória para o agente
"""

import psycopg
from config.settings import settings
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferWindowMemory
from typing import Optional
import json

class LimitedPostgresChatMessageHistory(PostgresChatMessageHistory):
    """
    Extensão do PostgresChatMessageHistory com limite de mensagens
    """
    
    def __init__(self, *args, max_messages: int = 10, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_messages = max_messages
    
    @property
    def messages(self):
        """Retorna apenas as últimas N mensagens"""
        all_messages = super().messages
        return all_messages[-self.max_messages:] if len(all_messages) > self.max_messages else all_messages
    
    def add_message(self, message):
        """Adiciona mensagem e mantém apenas as últimas N"""
        super().add_message(message)
        
        # Se tiver muitas mensagens, remover as mais antigas
        all_messages = super().messages
        if len(all_messages) > self.max_messages:
            # Remover mensagens antigas (manter apenas as últimas N)
            messages_to_remove = len(all_messages) - self.max_messages
            self._remove_oldest_messages(messages_to_remove)
    
    def _remove_oldest_messages(self, count: int):
        """Remove as mensagens mais antigas do banco"""
        try:
            conn = psycopg.connect(self.connection_string)
            cursor = conn.cursor()
            
            # Pegar IDs das mensagens mais antigas
            cursor.execute(f'''
                SELECT id FROM {self.table_name} 
                WHERE session_id = %s 
                ORDER BY id ASC 
                LIMIT %s
            ''', (self.session_id, count))
            
            ids_to_delete = [row[0] for row in cursor.fetchall()]
            
            if ids_to_delete:
                cursor.execute(f'''
                    DELETE FROM {self.table_name} 
                    WHERE id = ANY(%s)
                ''', (ids_to_delete,))
                
                conn.commit()
                print(f"🧹 Removidas {len(ids_to_delete)} mensagens antigas")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Erro ao remover mensagens antigas: {e}")

def testar_memoria_limitada():
    """Testa a memória com limite"""
    
    print("🧪 TESTANDO MEMÓRIA LIMITADA")
    print("="*50)
    
    telefone_teste = "5585999999999"
    max_msgs = 5  # Limite pequeno para teste
    
    # Criar histórico com limite
    history = LimitedPostgresChatMessageHistory(
        connection_string=settings.postgres_connection_string,
        session_id=telefone_teste,
        table_name=settings.postgres_table_name,
        max_messages=max_msgs
    )
    
    print(f"📱 Testando com limite de {max_msgs} mensagens")
    
    # Adicionar várias mensagens
    for i in range(1, 8):
        print(f"\\n➕ Adicionando mensagem {i}...")
        history.add_user_message(f"Teste mensagem {i}")
        history.add_ai_message(f"Resposta {i}")
        
        # Ver quantas mensagens tem agora
        msgs = history.messages
        print(f"   Mensagens na memória: {len(msgs)}")
        
        if len(msgs) > 0:
            print(f"   Última mensagem: {msgs[-1].content[:30]}...")
    
    print(f"\\n✅ Teste concluído!")
    print(f"📊 Resultado final: {len(history.messages)} mensagens mantidas")
    
    # Limpar mensagens de teste
    try:
        conn = psycopg.connect(settings.postgres_connection_string)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {settings.postgres_table_name} WHERE session_id = %s', (telefone_teste,))
        conn.commit()
        conn.close()
        print(f"🧹 Mensagens de teste removidas")
    except Exception as e:
        print(f"⚠️  Erro ao limpar: {e}")

if __name__ == "__main__":
    testar_memoria_limitada()