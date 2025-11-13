#!/usr/bin/env python3
"""
Script de teste para verificar o fluxo completo: produto → EAN → estoque/preco
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.http_tools import ean_lookup, estoque_preco

def test_fluxo_completo():
    """Testa o fluxo completo de consulta"""
    print("🧪 Testando fluxo completo do agente...")
    print("=" * 50)
    
    # Teste 1: Buscar EAN por nome do produto
    print("\n1️⃣ Buscando EAN para 'coca cola 2L'...")
    try:
        resultado_ean = ean_lookup("coca cola 2L")
        print(f"✅ EAN encontrado: {resultado_ean}")
        
        # Extrair EAN do resultado (assumindo formato JSON)
        if "7894900011516" in resultado_ean:
            ean = "7894900011516"
            print(f"📋 EAN extraído: {ean}")
            
            # Teste 2: Buscar preço/estoque com o EAN
            print(f"\n2️⃣ Buscando preço/estoque para EAN {ean}...")
            try:
                resultado_preco = estoque_preco(ean)
                print(f"✅ Preço/estoque encontrado: {resultado_preco}")
                
                print("\n✨ Fluxo completo funcionando!")
                return True
                
            except Exception as e:
                print(f"❌ Erro ao buscar preço/estoque: {e}")
                return False
        else:
            print("❌ EAN não encontrado no resultado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao buscar EAN: {e}")
        return False

if __name__ == "__main__":
    sucesso = test_fluxo_completo()
    
    if sucesso:
        print("\n🎉 Teste concluído com sucesso!")
        print("O agente está pronto para atender com contexto de supermercado!")
    else:
        print("\n⚠️  Teste falhou - verifique as configurações")
        sys.exit(1)