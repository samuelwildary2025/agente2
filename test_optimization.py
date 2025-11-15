#!/usr/bin/env python3
"""
Teste de otimização de tokens para o agente
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_langgraph_simple import run_agent_langgraph

def test_optimization():
    """Testa o agente com modo econômico ativado"""
    
    print("🧪 Testando agente com modo econômico OTIMIZADO")
    print("=" * 60)
    
    # Teste com uma pergunta típica de cliente
    telefone = "5585999999999"
    mensagens = [
        {
            "role": "user",
            "content": "Oi, quero saber se tem leite condensado e qual o preço?"
        }
    ]
    
    print(f"📱 Telefone: {telefone}")
    print(f"💬 Mensagem: {mensagens[0]['content']}")
    print()
    
    try:
        # Executa o agente
        resultado = run_agent_langgraph(
            telefone=telefone,
            mensagem=mensagens[0]['content']
        )
        
        resposta = resultado.get('output', 'Sem resposta')
        
        print(f"✅ Resposta do agente:")
        print(f"""{resposta}""")
        print()
        
        # Análise da resposta
        palavras = len(resposta.split())
        caracteres = len(resposta)
        
        print(f"📊 Análise da resposta:")
        print(f"   - Palavras: {palavras}")
        print(f"   - Caracteres: {caracteres}")
        print(f"   - Estimativa de tokens: ~{caracteres // 4}")
        
        if resultado.get('error'):
            print(f"⚠️  Erro detectado: {resultado['error']}")
        
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_optimization()