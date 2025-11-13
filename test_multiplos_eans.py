#!/usr/bin/env python3
"""
Teste para simular o que o agente está fazendo com múltiplos EANs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.http_tools import estoque_preco

def testar_multiplos_eans():
    """Testa exatamente o que o agente está fazendo"""
    
    # EANs que aparecem no log
    eans = ["7896220900359", "7890898451069", "78908982424810"]
    
    print("🧪 Testando múltiplos EANs como o agente faz...")
    print("=" * 60)
    
    resultados = []
    
    for ean in eans:
        print(f"\n📋 Testando EAN: {ean}")
        try:
            resultado = estoque_preco(ean)
            print(f"✅ Resultado: {resultado[:200]}...")
            resultados.append({"ean": ean, "resultado": resultado, "sucesso": True})
        except Exception as e:
            print(f"❌ Erro: {e}")
            resultados.append({"ean": ean, "resultado": str(e), "sucesso": False})
    
    print(f"\n📊 Resumo:")
    sucessos = [r for r in resultados if r["sucesso"]]
    falhas = [r for r in resultados if not r["sucesso"]]
    
    print(f"  - Sucessos: {len(sucessos)}")
    print(f"  - Falhas: {len(falhas)}")
    
    if len(sucessos) == 0:
        print("\n⚠️  Todos os EANs falharam! Isso explica a mensagem 'não há registros'")
    else:
        print(f"\n✅ {len(sucessos)} EAN(s) retornaram dados válidos")

if __name__ == "__main__":
    testar_multiplos_eans()