#!/usr/bin/env python3
"""
Teste para verificar se a correção resolveu de fato o problema
"""

import json
from tools.http_tools import estoque_preco

def testar_disponibilidade_real():
    """Testa produtos que sabemos que tinham quantidade 0.0 antes"""
    
    # EANs que antes retornavam quantidade 0.0
    eans_problema = [
        "7898944991064",  # ARROZ PARBO TIO ALEMAO 1kg - antes quantidade 0.0
        "7898922012019",  # FEIJAO CARIOCA DONA DE 1kg - antes quantidade 0.0  
    ]
    
    print("🧪 TESTANDO DISPONIBILIDADE APÓS CORREÇÃO")
    print("="*60)
    
    for ean in eans_problema:
        print(f"\n🔍 Testando EAN: {ean}")
        resultado = estoque_preco(ean)
        
        try:
            dados = json.loads(resultado)
            if dados and len(dados) > 0:
                produto = dados[0]
                print(f"✅ PRODUTO ENCONTRADO!")
                print(f"   Nome: {produto.get('produto', 'N/A')}")
                print(f"   Preço: R$ {produto.get('preco', 'N/A')}")
                print(f"   Disponibilidade: {produto.get('disponibilidade', 'N/A')}")
                print(f"   Ativo: {produto.get('ativo', 'N/A')}")
                print(f"   Quantidade: {produto.get('quantidade', 'N/A')}")
                
                # O mais importante: tem preço e está disponível?
                if produto.get('preco') and produto.get('disponibilidade') is True:
                    print(f"   🟢 PRODUTO DISPONÍVEL PARA VENDA!")
                else:
                    print(f"   🔴 Produto não disponível")
            else:
                print(f"   🔴 Nenhum produto encontrado")
                
        except json.JSONDecodeError:
            print(f"   🔴 Erro ao processar JSON: {resultado[:100]}...")

if __name__ == "__main__":
    testar_disponibilidade_real()