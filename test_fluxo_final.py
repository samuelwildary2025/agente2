#!/usr/bin/env python3
"""
Teste final do fluxo completo: produto → EAN → estoque/preco
Simulando exatamente o que o agente deve fazer
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.http_tools import ean_lookup, estoque_preco

def teste_fluxo_completo_real():
    """Testa o fluxo completo como o agente faria"""
    
    print("🧪 Testando fluxo completo do agente (cenário real)...")
    print("=" * 60)
    
    # Passo 1: Cliente pergunta sobre "arroz"
    produto_cliente = "arroz"
    print(f"📝 Cliente pergunta: '{produto_cliente}'")
    
    # Passo 2: Agente identifica produto e busca EAN
    print(f"\n1️⃣ Buscando EANs para '{produto_cliente}'...")
    try:
        resultado_ean = ean_lookup(produto_cliente)
        print(f"✅ EANs encontrados: {resultado_ean[:300]}...")
        
        # Passo 3: Para cada EAN encontrado, buscar preço/estoque
        # Vamos simular que encontramos estes EANs: 7896220900359, 7890898451069, 78908982424810
        eans_encontrados = ["7896220900359", "7890898451069", "78908982424810"]
        
        print(f"\n2️⃣ Buscando preço/estoque para os EANs encontrados...")
        
        resultados_validos = []
        
        for ean in eans_encontrados:
            print(f"\n📋 Consultando EAN: {ean}")
            try:
                resultado_preco = estoque_preco(ean)
                
                # Verificar se veio vazio []
                if resultado_preco.strip() == "[]":
                    print(f"  ⚠️  Sem dados válidos")
                else:
                    print(f"  ✅ Dados encontrados: {resultado_preco[:150]}...")
                    resultados_validos.append({"ean": ean, "dados": resultado_preco})
                    
            except Exception as e:
                print(f"  ❌ Erro: {e}")
        
        print(f"\n📊 Resumo final:")
        print(f"  - Total de EANs consultados: {len(eans_encontrados)}")
        print(f"  - EANs com dados válidos: {len(resultados_validos)}")
        
        if len(resultados_validos) > 0:
            print(f"\n🎉 SUCESSO! Encontramos {len(resultados_validos)} produto(s) com preço/estoque!")
            print("✅ O agente deve retornar estes produtos para o cliente:")
            
            for i, resultado in enumerate(resultados_validos, 1):
                print(f"  {i}. EAN {resultado['ean']} - {resultado['dados'][:100]}...")
                
            return True
        else:
            print(f"\n⚠️  Nenhum EAN retornou dados válidos")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao buscar EANs: {e}")
        return False

if __name__ == "__main__":
    sucesso = teste_fluxo_completo_real()
    
    if sucesso:
        print("\n🎉 Teste concluído com sucesso!")
        print("✅ O agente agora deve retornar produtos com preço/estoque para o cliente!")
    else:
        print("\n⚠️  Teste falhou - verifique as APIs")