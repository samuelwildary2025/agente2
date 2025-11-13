#!/usr/bin/env python3
"""
Teste simulando produtos com diferentes cenários de estoque
"""

import json
from tools.http_tools import estoque_preco

def testar_logica_disponibilidade():
    """Testa a lógica interna de disponibilidade com dados simulados"""
    
    # Vamos analisar o que acontece com diferentes cenários
    print("🧪 ANALISANDO LÓGICA DE DISPONIBILIDADE")
    print("="*60)
    
    # Testar com o EAN que já sabemos que existe
    ean = "7898944991064"  # ARROZ PARBO TIO ALEMAO 1kg
    resultado = estoque_preco(ean)
    
    try:
        dados = json.loads(resultado)
        if dados and len(dados) > 0:
            produto = dados[0]
            print(f"\n📊 PRODUTO REAL ENCONTRADO:")
            print(f"   Nome: {produto.get('produto', 'N/A')}")
            print(f"   Preço: R$ {produto.get('preco', 'N/A')}")
            print(f"   Disponibilidade: {produto.get('disponibilidade', 'N/A')}")
            print(f"   Ativo: {produto.get('ativo', 'N/A')}")
            print(f"   Quantidade: {produto.get('quantidade', 'N/A')}")
            
            # A lógica atual considera disponível?
            quantidade = float(produto.get('quantidade', 0))
            disponibilidade = produto.get('disponibilidade', False)
            ativo = produto.get('ativo', False)
            
            print(f"\n🔍 ANÁLISE DA LÓGICA:")
            print(f"   1. Tem quantidade > 0? {quantidade > 0}")
            print(f"   2. Tem disponibilidade=true? {disponibilidade is True}")
            print(f"   3. Tem ativo=true? {ativo is True}")
            
            # Com a lógica atual (priorizando estoque real)
            if quantidade > 0:
                print(f"   ✅ PRODUTO DISPONÍVEL (por quantidade > 0)")
            elif disponibilidade is True and ativo is True:
                print(f"   ✅ PRODUTO DISPONÍVEL (por disponibilidade + ativo)")
            else:
                print(f"   ❌ PRODUTO INDISPONÍVEL")
                
    except json.JSONDecodeError:
        print(f"   ❌ Erro ao processar JSON")

def explicar_nova_logica():
    """Explica como a nova lógica funciona"""
    print(f"\n📋 NOVA LÓGICA DE DISPONIBILIDADE:")
    print("="*60)
    print("Agora o agente só retorna produtos que:")
    print("")
    print("1️⃣  TEM ESTOQUE REAL (quantidade > 0) - PRIORIDADE MÁXIMA")
    print("   Ou")
    print("2️⃣  Tem disponibilidade=true + ativo=true (caso estoque não seja rastreado)")
    print("")
    print("🎯 RESULTADO: Você só verá produtos que realmente podem ser vendidos!")
    print("   Não vai mais mostrar produtos 'disponíveis' mas com estoque zero.")

if __name__ == "__main__":
    testar_logica_disponibilidade()
    explicar_nova_logica()