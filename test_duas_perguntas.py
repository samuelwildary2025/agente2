#!/usr/bin/env python3
"""
Teste para simular o cenário: 
1ª pergunta: agente diz que não tem disponível
2ª pergunta: mesmo produto, agente responde corretamente
"""

import asyncio
import time
from agent import run_agent
from config.logger import setup_logger

logger = setup_logger(__name__)

# Testar com produtos que sabemos que existem
PRODUTOS_TESTE = [
    "arroz tio joão 5kg",
    "feijão carioca 1kg",
    "leite condensado moça 395g"
]

def test_duas_perguntas():
    """Testa o comportamento de duas perguntas seguidas com o mesmo produto"""
    
    for produto in PRODUTOS_TESTE:
        print(f"\n{'='*60}")
        print(f"🧪 TESTANDO PRODUTO: {produto}")
        print(f"{'='*60}")
        
        # Simular telefone fixo para manter histórico
        telefone = "5511999990001"
        
        # Primeira pergunta
        print(f"\n🔍 PRIMEIRA PERGUNTA:")
        print(f"Usuário: {produto}")
        
        try:
            resultado1 = run_agent(telefone, produto)
            print(f"Agente: {resultado1['output']}")
            
            if resultado1.get('error'):
                print(f"❌ Erro: {resultado1['error']}")
                continue
                
        except Exception as e:
            print(f"❌ Erro na primeira pergunta: {e}")
            continue
        
        # Pequena pausa entre perguntas
        time.sleep(1)
        
        # Segunda pergunta (mesmo produto)
        print(f"\n🔍 SEGUNDA PERGUNTA (mesmo produto):")
        print(f"Usuário: {produto}")
        
        try:
            resultado2 = run_agent(telefone, produto)
            print(f"Agente: {resultado2['output']}")
            
            if resultado2.get('error'):
                print(f"❌ Erro: {resultado2['error']}")
                
        except Exception as e:
            print(f"❌ Erro na segunda pergunta: {e}")
            continue
        
        # Comparar respostas
        print(f"\n📊 COMPARAÇÃO:")
        print(f"Resposta 1: {resultado1['output']}")
        print(f"Resposta 2: {resultado2['output']}")
        
        # Verificar se são diferentes
        if resultado1['output'] != resultado2['output']:
            print(f"⚠️  RESPOSTAS DIFERENTES DETECTADAS!")
            print(f"   Primeira: {resultado1['output'][:100]}...")
            print(f"   Segunda:  {resultado2['output'][:100]}...")
        else:
            print(f"✅ Respostas iguais")
        
        print(f"\n{'-'*60}")

if __name__ == "__main__":
    print("🚀 Iniciando teste de inconsistência entre perguntas repetidas")
    test_duas_perguntas()
    print("\n✅ Teste concluído!")