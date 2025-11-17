#!/usr/bin/env python3
"""
Teste de consumo de tokens em conversa longa com cliente
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_langgraph_simple import run_agent_langgraph

def simular_conversa_longa():
    """Simula uma conversa longa e realista com cliente de supermercado"""
    
    print("🧪 Simulando CONVERSA LONGA com cliente (modo econômico)")
    print("=" * 70)
    
    telefone = "558587520060"  # Usar o mesmo telefone do exemplo real
    
    # Simulação de uma conversa real longa com idas e vindas
    conversa = [
        {
            "role": "user", 
            "content": "Oi Ana, boa noite! Vim aqui pedir umas coisinhas para minha vovó que tá de visita em casa. Preciso de coisas agora porque amanhã não sei se eu dou conta, tá tudo uma correria aqui. Pode me ajudar?"
        },
        {
            "role": "user", 
            "content": "Quero arroz, mas aquele agulhinha que vocês têm. É 5kg ou maior? E também preciso de pão, mas o Pullman que ele gosta. Ah, e leite condensado também para fazer um doce."
        },
        {
            "role": "user", 
            "content": "Esqueci de falar do leite condensado. É daquele de lata mesmo, o tradicional. Qual marca vocês têm? Tem da Nestlé ou da Moça?"
        },
        {
            "role": "user", 
            "content": "Pera aí Ana, tira esse arroz agulhinha que eu falei. Meu avô não gosta muito desse. Coloca no lugar o arroz parboilizado mesmo, aquele branquinho. E quanto ao leite condensado, coloca o da Nestlé de 395g."
        },
        {
            "role": "user", 
            "content": "Ah, e tira o pão Pullman também! Esqueci que ele tá de dieta. Coloca o pão integral de forma, aquele mesmo. Quantos gramas tem esse aí?"
        },
        {
            "role": "user", 
            "content": "Ótimo! Agora me fala uma coisa: vocês têm mortadela? Mas não aquela com olho que ele não gosta. É a sem olho, sabe? Aquele pedaço inteiro que a gente corta em fatias."
        },
        {
            "role": "user", 
            "content": "Perfeito! E quanto é tudo isso que já temos aí? Só para eu ir me organizando. Dá um total aí pra mim ver se preciso tirar ou colocar mais alguma coisa."
        },
        {
            "role": "user", 
            "content": "Espera Ana! Acabei de lembrar que preciso de mais uma coisa. Meu vô gosta de tomar café da tarde com aquele biscoito cream cracker. Vocês têm? É daquele de pacote, sabe? Qual marca vocês têm?" 
        },
        {
            "role": "user", 
            "content": "Tá bom, coloca o cream cracker mesmo. Agora é só isso mesmo! Qual é o total final? E me fala: é melhor eu retirar na loja ou vocês entregam em casa? Qual é mais rápido?"
        },
        {
            "role": "user", 
            "content": "Então coloca para entrega em casa. Me confirma tudo de novo pra eu ter certeza: arroz parboilizado 5kg, pão integral de forma, leite condensado Nestlé 395g, mortadela sem olho e cream cracker. Está tudo certo?"
        }
    ]
    
    print(f"📱 Cliente: {telefone}")
    print(f"📝 Simulando conversa com {len(conversa)} trocas de mensagens")
    print(f"🎯 Modo: ECONÔMICO (respostas curtas)")
    print()
    
    total_tokens_estimado = 0
    total_caracteres = 0
    
    for i, mensagem in enumerate(conversa, 1):
        print(f"🔄 Mensagem {i}/{len(conversa)}")
        print(f"👤 Cliente: {mensagem['content'][:80]}...")
        
        try:
            resultado = run_agent_langgraph(
                telefone=telefone,
                mensagem=mensagem['content']
            )
            
            resposta = resultado.get('output', 'Sem resposta')
            
            # Análise da resposta
            caracteres = len(resposta)
            palavras = len(resposta.split())
            tokens_estimados = caracteres // 4  # Estimativa conservadora
            
            print(f"🤖 Ana: {resposta[:80]}...")
            print(f"📊 Métricas: {palavras} palavras, {caracteres} caracteres, ~{tokens_estimados} tokens")
            print()
            
            total_tokens_estimado += tokens_estimados
            total_caracteres += caracteres
            
            if resultado.get('error'):
                print(f"⚠️  Erro: {resultado['error']}")
                break
                
        except Exception as e:
            print(f"❌ Erro ao processar mensagem {i}: {e}")
            break
    
    print("=" * 70)
    print("📈 RESUMO DA CONVERSA:")
    print(f"   Total de mensagens: {len(conversa)}")
    print(f"   Total de caracteres: {total_caracteres:,}")
    print(f"   Total estimado de tokens: {total_tokens_estimado:,}")
    print()
    
    # Cálculo de custo com GPT-5-mini
    custo_entrada = (total_tokens_estimado * 0.8) * 0.00000025  # 80% para entrada
    custo_saida = (total_tokens_estimado * 0.2) * 0.00000200     # 20% para saída
    custo_total = custo_entrada + custo_saida
    
    print("💰 CUSTO ESTIMADO (GPT-5-mini):")
    print(f"   Entrada: US$ {custo_entrada:.6f}")
    print(f"   Saída: US$ {custo_saida:.6f}")
    print(f"   Total: US$ {custo_total:.6f}")
    print(f"   Em Reais: R$ {custo_total * 6:.4f}")
    print()
    
    # Projeção mensal
    print("📊 PROJEÇÃO MENSAL (50 conversas longas/dia):")
    custo_mensal = custo_total * 50 * 30
    print(f"   Custo mensal: US$ {custo_mensal:.2f}")
    print(f"   Custo mensal: R$ {custo_mensal * 6:.2f}")
    
    # Comparação com modo não econômico
    print()
    print("🔍 COMPARAÇÃO:")
    print(f"   Com modo econômico: R$ {custo_mensal * 6:.2f}/mês")
    print(f"   Sem modo econômico: R$ {custo_mensal * 6 * 2:.2f}/mês")
    print(f"   Economia mensal: R$ {custo_mensal * 6:.2f}")

if __name__ == "__main__":
    simular_conversa_longa()