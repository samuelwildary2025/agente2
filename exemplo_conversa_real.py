#!/usr/bin/env python3
"""
Exemplo de conversa REAL com timeout natural

Mostra exatamente como ficaria a troca de mensagens no WhatsApp.
"""

def mostrar_conversa_real():
    """Mostra a conversa real como seria no WhatsApp"""
    
    print("📱 CONVERSA REAL NO WHATSAPP")
    print("="*50)
    print("Supermercado Queiroz - Atendimento Virtual")
    print("="*50)
    
    # Parte 1: Cliente pede arroz pela manhã
    print("\n🕘 09:15 - Segunda-feira de manhã")
    print("📱 Cliente: Oi bom dia, quero arroz")
    print("🤖 Agente: Bom dia! Sou o assistente virtual do Supermercado Queiroz! 😊")
    print("🤖 Agente: Encontrei arroz branco 1kg por R$ 6,90. Quantos pacotes você quer?")
    print("📱 Cliente: [NÃO RESPONDE]")
    
    print("\n⏰ [Pedido ativo por 1 hora...]")
    print("🔄 [Pedido expira automaticamente às 10:15]")
    
    print("\n" + "="*50)
    print("😴 [Cliente some por horas...]")
    print("="*50)
    
    # Parte 2: Cliente retorna à noite
    print("\n🕓 18:45 - Mesma segunda-feira à noite")
    print("📱 Cliente: Vou querer feijão também")
    
    print("\n🤖 [Agente detecta timeout automaticamente]")
    print("🤖 Agente: ⏰ Opa! Percebi que seu pedido anterior expirou após 1 hora de inatividade.")
    print("🤖 Agente: Como se passou bastante tempo, precisei iniciar um novo atendimento.")
    print("🤖 Agente: Por favor, me diga tudo que você quer começando do início.")
    print("🤖 Agente: Estou aqui para ajudar! 😊")
    
    print("\n📱 Cliente: Ah entendi, quero arroz e feijão então")
    print("🤖 Agente: Perfeito! Vou verificar arroz e feijão para você.")
    print("🤖 Agente: Encontrei: Arroz branco 1kg R$ 6,90 e Feijão carioca 1kg R$ 8,50")
    print("🤖 Agente: Quantos de cada você quer?")
    
    print("\n📱 Cliente: 2 pacotes de arroz e 1 de feijão")
    print("🤖 Agente: Ótimo! 2x Arroz (R$ 13,80) + 1x Feijão (R$ 8,50) = Total: R$ 22,30")
    print("🤖 Agente: Posso confirmar seu pedido?")
    
    print("\n📱 Cliente: Sim, pode confirmar")
    print("🤖 Agente: ✅ Pedido confirmado! Total: R$ 22,30")
    print("🤖 Agente: Seu pedido será preparado e entregue em breve!")
    
    print("\n" + "="*50)
    print("✅ CONVERSA CONCLUÍDA COM SUCESSO")
    print("="*50)

def mostrar_comparacao():
    """Mostra a diferença entre antes e depois do timeout natural"""
    
    print("\n📊 COMPARAÇÃO: Antes vs Depois do Timeout Natural")
    print("="*70)
    
    print("\n❌ ANTES (Sem timeout natural):")
    print("📱 Cliente: Vou querer feijão também")
    print("🤖 Agente: ❓ Não entendi. Você tem um pedido ativo?")
    print("📱 Cliente: Sim, pedi arroz hoje de manhã")
    print("🤖 Agente: ❓ Não encontro seu pedido. Envie 'pedido' para iniciar novo")
    print("📱 Cliente: ???")
    print("😤 Cliente frustrado e confuso")
    
    print("\n✅ DEPOIS (Com timeout natural):")
    print("📱 Cliente: Vou querer feijão também")
    print("🤖 Agente: ⏰ Opa! Percebi que seu pedido anterior expirou...")
    print("🤖 Agente: Por favor, me diga tudo que você quer começando do início.")
    print("📱 Cliente: Ah entendi, quero arroz e feijão")
    print("🤖 Agente: Perfeito! Vou verificar para você...")
    print("😊 Cliente entende e continua normalmente")
    
    print("\n💡 DIFERENÇA PRINCIPAL:")
    print("• Antes: Cliente precisava adivinhar que pedido expirou")
    print("• Depois: Agente explica proativamente a situação")
    print("• Resultado: Experiência muito mais natural e amigável!")

def main():
    mostrar_conversa_real()
    mostrar_comparacao()
    
    print("\n🎯 CONCLUSÃO:")
    print("O timeout natural transforma uma situação potencialmente")
    print("frustrante em uma experiência fluida e compreensível!")

if __name__ == "__main__":
    main()