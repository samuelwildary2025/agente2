#!/usr/bin/env python3
"""
Teste para verificar se apenas produtos com estoque real são considerados disponíveis
"""

import json
from tools.http_tools import estoque_preco

def testar_apenas_com_estoque():
    """Testa se apenas produtos com quantidade > 0 são considerados disponíveis"""
    
    # Testar com vários EANs para ver quais têm estoque real
    eans_para_testar = [
        "7898944991064",  # ARROZ PARBO TIO ALEMAO 1kg - quantidade 0.0
        "7898922012019",  # FEIJAO CARIOCA DONA DE 1kg - quantidade 0.0  
        "7891000100103",  # LEITE COND MOCA LT 395g - quantidade 3.0
        "7896038337057",  # ARROZ BRANCO TRES MOINHOS 1kg - testar novo
    ]
    
    print("🧪 TESTANDO: Apenas produtos com estoque real > 0")
    print("="*60)
    
    disponiveis = 0
    indisponiveis = 0
    
    for ean in eans_para_testar:
        print(f"\n🔍 Testando EAN: {ean}")
        resultado = estoque_preco(ean)
        
        try:
            dados = json.loads(resultado)
            if dados and len(dados) > 0:
                produto = dados[0]
                quantidade = produto.get('quantidade', 0)
                disponibilidade = produto.get('disponibilidade', False)
                
                print(f"   Nome: {produto.get('produto', 'N/A')}")
                print(f"   Preço: R$ {produto.get('preco', 'N/A')}")
                print(f"   Disponibilidade no sistema: {disponibilidade}")
                print(f"   Quantidade: {quantidade}")
                
                # O importante: tem estoque real?
                if quantidade and float(quantidade) > 0:
                    print(f"   🟢 PRODUTO COM ESTOQUE REAL!")
                    disponiveis += 1
                else:
                    print(f"   🔴 Produto sem estoque (quantidade = 0)")
                    indisponiveis += 1
            else:
                print(f"   🔴 Nenhum produto encontrado")
                indisponiveis += 1
                
        except json.JSONDecodeError:
            print(f"   🔴 Erro ao processar JSON: {resultado[:100]}...")
            indisponiveis += 1
    
    print(f"\n📊 RESUMO:")
    print(f"   ✅ Produtos com estoque real: {disponiveis}")
    print(f"   ❌ Produtos sem estoque: {indisponiveis}")

if __name__ == "__main__":
    testar_apenas_com_estoque()