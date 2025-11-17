#!/usr/bin/env python3
"""
Demonstração: Mensagens que o Cliente Recebe
Mostra as respostas exatas do agente em diferentes situações
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demonstrar_mensagens_cliente():
    """Mostra as mensagens exatas que o cliente recebe"""
    
    print("💬 DEMONSTRAÇÃO: Mensagens que o Cliente Recebe")
    print("=" * 70)
    print("📱 Veja como o WhatsApp do cliente mostra as respostas:")
    print()
    
    # Cenário 1: Pedido Ativo (Normal)
    print("🟢 CENÁRIO 1: Pedido Ativo - Cliente faz pergunta normal")
    print("-" * 60)
    print("👤 Cliente: 'Oi, tem arroz integral?'")
    print("⏰ [Pedido está ativo - dentro da 1 hora]")
    print()
    print("🤖 Ana (Assistente):")
    print("   'Olá! Sim, temos arroz integral disponível. O estoque está")
    print("   verde e o preço é R$ 8,90 o kg. Posso adicionar ao seu")
    print("   pedido? Quantos pacotes você gostaria?'")
    print("   ")
    print("   [Resposta completa - processada com LLM]")
    print("   [Custo: ~R$ 0,02 - 350 tokens]")
    print()
    
    # Cenário 2: Pedido Expirado
    print("🔴 CENÁRIO 2: Pedido Expirado - Cliente tenta continuar")
    print("-" * 60)
    print("👤 Cliente: 'E tem feijão também?'")
    print("⏰ [Pedido expirou - passou 1 hora sem interação]")
    print()
    print("🤖 Ana (Assistente):")
    print("   ⏰ Seu pedido anterior expirou após 1 hora de inatividade.")
    print("   Por favor, envie 'pedido' para iniciar um novo atendimento.")
    print("   ")
    print("   [Resposta imediata - sem processar no LLM]")
    print("   [Custo: R$ 0,00 - 0 tokens]")
    print()
    
    # Cenário 3: Cliente Reinicia Corretamente
    print("🟢 CENÁRIO 3: Cliente Reinicia - Após expiração")
    print("-" * 60)
    print("👤 Cliente: 'pedido'")
    print("⏰ [Cliente reinicia o atendimento]")
    print()
    print("🤖 Ana (Assistente):")
    print("   'Olá! Seja bem-vindo(a) de volta! 😊')")
    print("   'Vou iniciar um novo atendimento para você.")
    print("   'O que você gostaria de pedir hoje?'")
    print("   ")
    print("   [Novo pedido criado - timeout renovado para 1 hora]")
    print("   [Custo: ~R$ 0,02 - novo processamento com LLM]")
    print()
    
    # Cenário 4: Cliente Confuso
    print("🟡 CENÁRIO 4: Cliente Confuso - Não entendeu a mensagem")
    print("-" * 60)
    print("👤 Cliente: 'Mas eu já estava conversando!'")
    print("⏰ [Cliente ainda não entendeu que precisa reiniciar]")
    print()
    print("🤖 Ana (Assistente):")
    print("   ⏰ Seu pedido anterior expirou após 1 hora de inatividade.")
    print("   Por favor, envie 'pedido' para iniciar um novo atendimento.")
    print("   ")
    print("   [Mensagem repetida - pedido ainda expirado]")
    print("   [Custo: R$ 0,00 - continua bloqueado]")
    print()
    
    # Comparação de Custos
    print("💰 COMPARAÇÃO DE CUSTOS (60 pedidos/dia)")
    print("=" * 70)
    print("📊 Sem Timeout (todos processados):")
    print("   60 pedidos × R$ 0,02 = R$ 1,20/dia")
    print("   R$ 1,20 × 30 dias = R$ 36,00/mês")
    print()
    print("📊 Com Timeout (30% expiram):")
    print("   42 pedidos ativos × R$ 0,02 = R$ 0,84/dia")
    print("   18 pedidos expirados × R$ 0,00 = R$ 0,00/dia")
    print("   Total: R$ 0,84/dia")
    print("   R$ 0,84 × 30 dias = R$ 25,20/mês")
    print()
    print("💡 ECONOMIA: R$ 10,80/mês (30% de redução)")
    print("   Em 60 pedidos/dia: R$ 129,60/ano de economia!")
    print()
    
    # Vantagens para o Cliente
    print("✅ VANTAGENS PARA O CLIENTE")
    print("-" * 40)
    print("🕐 Clareza: Sabe exatamente quando precisa reiniciar")
    print("💰 Economia: Sistema mais barato = preços melhores")
    print("🧹 Limpeza: Não acumula pedidos antigos perdidos")
    print("⚡ Rapidez: Resposta imediata para pedidos expirados")
    print("🔄 Facilidade: Basta digitar 'pedido' para reiniciar")
    print()
    
    # Vantagens para o Supermercado
    print("🏪 VANTAGENS PARA O SUPERMERCADO")
    print("-" * 40)
    print("💸 Economia: Reduz custos com IA em 30%")
    print("📱 Eficiência: Atende mais clientes com mesmo orçamento")
    print("🧠 Organização: Pedidos ativos sempre relevantes")
    print("📊 Previsão: Custos mais previsíveis e controláveis")
    print("🚀 Escalabilidade: Sistema sustentável em alta demanda")

def main():
    """Executa demonstração"""
    try:
        demonstrar_mensagens_cliente()
        return True
    except KeyboardInterrupt:
        print("\n⚠️ Demonstração interrompida")
        return False
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)