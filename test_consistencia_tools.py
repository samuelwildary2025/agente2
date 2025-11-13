#!/usr/bin/env python3
"""
Teste direto das ferramentas para investigar inconsistência
Simula o fluxo completo: produto → EAN → estoque_preco (duas vezes)
"""

import time
from tools.http_tools import ean_lookup, estoque_preco
from config.logger import setup_logger

logger = setup_logger(__name__)

def test_fluxo_completo_duas_vezes(produto: str):
    """Testa o fluxo completo duas vezes seguidas"""
    
    print(f"\n🧪 TESTANDO FLUXO PARA: {produto}")
    print("="*60)
    
    # Primeira execução
    print("\n🔍 PRIMEIRA EXECUÇÃO:")
    print("1. Buscando EANs...")
    
    try:
        eans_resultado1 = ean_lookup(produto)
        print(f"✅ EANs encontrados: {len(str(eans_resultado1))} caracteres")
        
        # Extrair EANs do resultado
        import re
        eans1 = re.findall(r'(\d{8,14})', str(eans_resultado1))
        print(f"   EANs extraídos: {eans1[:3]}...")  # Mostrar primeiros 3
        
        if eans1:
            print("2. Buscando estoque/preço...")
            estoque_resultado1 = estoque_preco(eans1[0])
            print(f"✅ Estoque/preço retornado: {len(str(estoque_resultado1))} caracteres")
            
            # Verificar se tem produtos disponíveis
            if "disponível" in str(estoque_resultado1).lower() or "estoque" in str(estoque_resultado1).lower():
                print("✅ Produto marcado como disponível")
            else:
                print("⚠️  Produto não parece disponível")
        else:
            print("❌ Nenhum EAN encontrado")
            
    except Exception as e:
        print(f"❌ Erro na primeira execução: {e}")
        return
    
    # Pequena pausa
    time.sleep(1)
    
    # Segunda execução (mesmo produto)
    print("\n🔍 SEGUNDA EXECUÇÃO:")
    print("1. Buscando EANs...")
    
    try:
        eans_resultado2 = ean_lookup(produto)
        print(f"✅ EANs encontrados: {len(str(eans_resultado2))} caracteres")
        
        # Extrair EANs do resultado
        eans2 = re.findall(r'(\d{8,14})', str(eans_resultado2))
        print(f"   EANs extraídos: {eans2[:3]}...")
        
        if eans2:
            print("2. Buscando estoque/preço...")
            estoque_resultado2 = estoque_preco(eans2[0])
            print(f"✅ Estoque/preço retornado: {len(str(estoque_resultado2))} caracteres")
            
            # Verificar se tem produtos disponíveis
            if "disponível" in str(estoque_resultado2).lower() or "estoque" in str(estoque_resultado2).lower():
                print("✅ Produto marcado como disponível")
            else:
                print("⚠️  Produto não parece disponível")
        else:
            print("❌ Nenhum EAN encontrado")
            
    except Exception as e:
        print(f"❌ Erro na segunda execução: {e}")
        return
    
    # Comparar resultados
    print(f"\n📊 COMPARAÇÃO:")
    
    # Comparar EANs
    if str(eans_resultado1) == str(eans_resultado2):
        print("✅ Resultados EAN idênticos")
    else:
        print("⚠️  Resultados EAN diferentes!")
        print(f"   Primeiro: {str(eans_resultado1)[:100]}...")
        print(f"   Segundo:  {str(eans_resultado2)[:100]}...")
    
    # Comparar estoque
    if str(estoque_resultado1) == str(estoque_resultado2):
        print("✅ Resultados estoque/preço idênticos")
    else:
        print("⚠️  Resultados estoque/preço diferentes!")
        print(f"   Primeiro: {str(estoque_resultado1)[:100]}...")
        print(f"   Segundo:  {str(estoque_resultado2)[:100]}...")

def main():
    """Testa múltiplos produtos"""
    
    produtos = [
        "arroz tio joão 5kg",
        "feijão carioca 1kg", 
        "leite condensado moça 395g"
    ]
    
    print("🚀 TESTE DE CONSISTÊNCIA DAS FERRAMENTAS")
    print("="*60)
    print("Este teste verifica se as APIs retornam resultados consistentes")
    print("ao serem chamadas duas vezes seguidas com o mesmo produto.")
    
    for produto in produtos:
        test_fluxo_completo_duas_vezes(produto)
        time.sleep(2)  # Pausa entre produtos
    
    print("\n✅ Teste concluído!")

if __name__ == "__main__":
    main()