#!/usr/bin/env python3
"""
Teste para investigar inconsistência nas respostas do agente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.http_tools import ean_lookup, estoque_preco

def testar_inconsistencia():
    """Testa múltiplas chamadas com o mesmo produto"""
    
    produto = "arroz"  # Produto que você mencionou
    
    print("🧪 Testando inconsistência nas respostas...")
    print("=" * 60)
    print(f"📝 Produto testado: '{produto}'")
    print()
    
    # Testar 3 vezes o mesmo produto
    for i in range(1, 4):
        print(f"🔍 Teste #{i}:")
        print("-" * 30)
        
        try:
            # Passo 1: Buscar EAN
            print("  1️⃣ Buscando EAN...")
            resultado_ean = ean_lookup(produto)
            print(f"  ✅ EANs: {resultado_ean[:200]}...")
            
            # Extrair EANs do resultado (simplificado)
            eans = ["7896220900359", "7890898451069", "78908982424810"]  # EANs que vimos antes
            resultados_validos = 0
            
            # Passo 2: Buscar preço/estoque para cada EAN
            print("  2️⃣ Buscando preço/estoque...")
            for ean in eans:
                try:
                    resultado_preco = estoque_preco(ean)
                    if resultado_preco.strip() != "[]":
                        resultados_validos += 1
                        print(f"    ✅ EAN {ean}: Dados encontrados")
                    else:
                        print(f"    ⚠️  EAN {ean}: Sem dados")
                except Exception as e:
                    print(f"    ❌ EAN {ean}: Erro - {e}")
            
            print(f"  📊 Resultado: {resultados_validos} produto(s) com dados")
            
        except Exception as e:
            print(f"  ❌ Erro no teste: {e}")
        
        print()
    
    print("📋 Análise:")
    print("Se os resultados forem diferentes entre os testes, indica inconsistência!")

if __name__ == "__main__":
    testar_inconsistencia()