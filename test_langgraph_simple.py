#!/usr/bin/env python3
"""
Testar o agente LangGraph simplificado
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_langgraph_simple import run_agent

def testar_agente_langgraph_simple():
    """Testa o agente LangGraph simplificado com diferentes cenários"""
    
    print("🧪 Testando agente LangGraph simplificado...")
    print("=" * 60)
    
    # Teste 1: Primeira pergunta sobre arroz
    print("📝 Teste 1: Primeira pergunta sobre 'arroz'")
    telefone = "5511999999999"
    
    resposta1 = run_agent(telefone, "arroz")
    print(f"Resposta 1: {resposta1['output']}")
    print(f"Erro: {resposta1['error']}")
    print()
    
    # Teste 2: Segunda pergunta sobre arroz (mesma sessão)
    print("📝 Teste 2: Segunda pergunta sobre 'arroz' (mesma sessão)")
    
    resposta2 = run_agent(telefone, "arroz")
    print(f"Resposta 2: {resposta2['output']}")
    print(f"Erro: {resposta2['error']}")
    print()
    
    # Teste 3: Pergunta diferente
    print("📝 Teste 3: Pergunta sobre 'feijão'")
    
    resposta3 = run_agent(telefone, "feijão")
    print(f"Resposta 3: {resposta3['output']}")
    print(f"Erro: {resposta3['error']}")
    
if __name__ == "__main__":
    testar_agente_langgraph_simple()