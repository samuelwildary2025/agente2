#!/usr/bin/env python3
"""
Análise detalhada do que o estoque_preco retorna
"""

import json
from tools.http_tools import estoque_preco

def analisar_estoque_detalhado(ean: str):
    """Analisa detalhadamente o que o estoque_preco retorna"""
    
    print(f"\n🔍 ANALISANDO EAN: {ean}")
    print("="*60)
    
    resultado = estoque_preco(ean)
    print("📋 RESULTADO BRUTO:")
    print(resultado)
    
    # Tentar parsear como JSON
    try:
        dados = json.loads(resultado)
        print(f"\n📊 ESTRUTURA JSON:")
        print(f"Tipo: {type(dados)}")
        
        if isinstance(dados, list):
            print(f"Itens na lista: {len(dados)}")
            for i, item in enumerate(dados):
                print(f"\n  Item {i+1}:")
                for chave, valor in item.items():
                    print(f"    {chave}: {valor}")
        elif isinstance(dados, dict):
            for chave, valor in dados.items():
                print(f"  {chave}: {valor}")
                
    except json.JSONDecodeError:
        print("\n⚠️  Não é JSON válido, tratando como texto")
        linhas = resultado.split('\n')
        for i, linha in enumerate(linhas[:10]):  # Primeiras 10 linhas
            print(f"  {i+1}: {linha}")

# Testar com os EANs que usamos anteriormente
eans_para_testar = [
    "7898944991064",  # ARROZ PARBO TIO ALEMAO 1kg
    "7898922012019",  # FEIJAO CARIOCA DONA DE 1kg  
    "7891000100103"   # LEITE COND MOCA LT 395g
]

print("🚀 ANÁLISE DETALHADA DOS RESULTADOS")
print("Este teste mostra exatamente o que o estoque_preco retorna")

for ean in eans_para_testar:
    analisar_estoque_detalhado(ean)
    print("\n" + "="*80 + "\n")