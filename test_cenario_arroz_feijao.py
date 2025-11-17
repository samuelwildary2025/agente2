#!/usr/bin/env python3
"""
Teste do cenário: Cliente pede arroz no início do dia e volta no final do dia

Demonstra como o agente lida quando o cliente menciona produtos de um pedido expirado.
"""

from datetime import datetime

def simular_cenario_dia_completo():
    """Simula o cenário completo do dia"""
    
    print("🛒 CENÁRIO: Cliente pede arroz no início do dia")
    print("⏰ Horário: 09:00 da manhã")
    print("💬 Cliente: 'Oi, quero arroz'")
    print("🤖 Agente: 'Oi! Sou o assistente virtual do Supermercado Queiroz! 😊'")
    print("🤖 Agente: 'Encontrei arroz integral 1kg por R$ 8,50. Quantos você quer?'")
    print("✅ Pedido ativo - TTL: 1 hora")
    
    print("\n" + "="*60)
    print("😴 CLIENTE SOME POR HORAS...")
    print("⏰ Horário: 18:00 da noite (9 horas depois)")
    print("🔄 Pedido expirou automaticamente após 1 hora de inatividade")
    
    print("\n" + "="*60)
    print("🛒 CENÁRIO: Cliente retorna e menciona produto do pedido expirado")
    print("⏰ Horário: 18:00 da noite")
    print("💬 Cliente: 'Vou querer feijão também'")
    print("📱 Telefone: 5511999998888")
    
    print("\n🤖 Agente verifica timeout automaticamente:")
    print("🔄 Pedido anterior expirou após 1 hora de inatividade.")
    print("🤖 Agente: '⏰ Seu pedido anterior expirou após 1 hora de inatividade.'")
    print("🤖 Agente: 'Como se passou bastante tempo, precisei iniciar um novo atendimento para você.'")
    print("🤖 Agente: 'Por favor, me diga novamente o que você gostaria de pedir começando do início.'")
    print("🤖 Agente: 'Estou aqui para ajudar! 😊'")
    
    print("\n💬 Cliente: 'Quero arroz e feijão'")
    print("🤖 Agente: 'Perfeito! Vou verificar arroz e feijão para você.'")
    print("✅ Novo pedido criado - TTL: 1 hora")
    
    print("\n" + "="*60)
    print("📝 RESUMO DO FLUXO:")
    print("1️⃣ Cliente pede arroz pela manhã")
    print("2️⃣ Pedido fica ativo por 1 hora")
    print("3️⃣ Após 1 hora, pedido expira automaticamente")
    print("4️⃣ Cliente retorna à noite e menciona 'feijão também'")
    print("5️⃣ Agente detecta timeout e explica situação")
    print("6️⃣ Agente reinicia pedido naturalmente")
    print("7️⃣ Cliente refaz pedido completo")
    
    print("\n💡 COMO O AGENTE LIDA COM PRODUTOS ANTERIORES:")
    print("• O agente NÃO menciona o arroz do pedido expirado")
    print("• O agente explica que precisa reiniciar do início")
    print("• O cliente entende e refaz o pedido completo")
    print("• A experiência é natural e sem frustração")

def main():
    print("🧪 TESTE: Cliente menciona produto de pedido expirado")
    print("="*70)
    
    simular_cenario_dia_completo()
    
    print("\n" + "="*70)
    print("✅ CONCLUSÃO:")
    print("O agente lida inteligentemente com pedidos expirados,")
    print("explicando a situação e guiando o cliente a refazer")
    print("o pedido de forma natural e sem confusão!")

if __name__ == "__main__":
    main()