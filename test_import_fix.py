#!/usr/bin/env python3
"""
Teste rápido para verificar se o import do psycopg2 está funcionando
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_psycopg_import():
    """Testa o import do psycopg2"""
    print("🧪 Testando import do psycopg2...")
    
    try:
        # Testa o import com fallback
        try:
            import psycopg2
            import psycopg2.extras
            print("✅ psycopg2 importado com sucesso")
            version = psycopg2.__version__ if hasattr(psycopg2, '__version__') else "desconhecida"
            print(f"📋 Versão: {version}")
        except ImportError:
            print("⚠️ psycopg2 não encontrado, tentando psycopg 3.x...")
            import psycopg as psycopg2
            from psycopg import sql
            print("✅ psycopg 3.x importado com sucesso")
            
        # Testa conexão básica
        from config.settings import settings
        print(f"📋 Testando conexão com: {settings.postgres_connection_string}")
        
        # Tenta conectar
        try:
            with psycopg2.connect(settings.postgres_connection_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    print(f"✅ Conexão bem sucedida! Resultado: {result}")
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True

def test_memory_import():
    """Testa o import da memória limitada"""
    print("\n🧪 Testando import da LimitedPostgresChatMessageHistory...")
    
    try:
        from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
        print("✅ LimitedPostgresChatMessageHistory importado com sucesso")
        
        # Testa criação básica
        from config.settings import settings
        memory = LimitedPostgresChatMessageHistory(
            session_id="test_import",
            connection_string=settings.postgres_connection_string,
            table_name=settings.postgres_table_name,
            max_messages=5
        )
        print("✅ Instância criada com sucesso")
        print(f"📋 Tabela: {settings.postgres_table_name}")
        print(f"📋 Limite: {settings.postgres_message_limit}")
        
    except Exception as e:
        print(f"❌ Erro no import da memória: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    return True

if __name__ == "__main__":
    print("🔧 Teste de Import do PostgreSQL")
    print("=" * 40)
    
    psycopg_ok = test_psycopg_import()
    memory_ok = test_memory_import()
    
    print("\n" + "=" * 40)
    if psycopg_ok and memory_ok:
        print("✅ ✅ ✅ Todos os imports funcionando!")
    else:
        print("❌ ❌ ❌ Problemas detectados nos imports")
        
    print("\n💡 Se houver problemas, instale:")
    print("   pip install psycopg2-binary")
    print("   OU")
    print("   pip install psycopg[binary]")