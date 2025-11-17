#!/usr/bin/env python3
"""
Demonstração rápida do fluxo natural com timeout automático

Versão otimizada sem delays longos para mostrar o funcionamento.
"""

from datetime import datetime

def simular_verificacao_timeout(telefone, minutos_passados):
    """Simula a verificação de timeout do agente"""
    print(f"\n{'='*50}")
    print(f"📱 Cliente: {telefone}")
    print(f"⏰ Tempo desde última interação: {minutos_passados} minutos")
    
    if minutos_passados > 60:
        print("🤖 Agente: 🔄 Pedido anterior expirou após 1 hora. Iniciando novo pedido automaticamente...")
        print("🤖 Agente: Oi! Sou o assistente virtual do Supermercado Queiroz! 😊")
        print("🤖 Agente: Posso ajudar você com seu pedido? Qual produto você procura?")
        return "expirado"
    else:
        print("🤖 Agente: ✅ Pedido dentro do prazo. Continuando normalmente...")
        print("🤖 Agente: Entendi! Vou verificar isso para você...")
        return "ativo"

def main():
    print("🛒 DEMONSTRAÇÃO RÁPIDA: Timeout Natural com Reinício Automático")
    print("="*60)
    
    telefone = "5511999998888"
    
    # Cenário 1: Cliente faz pedido (0 minutos - pedido novo)
    print("\n📋 CENÁRIO 1: Pedido novo (0 minutos)")
    simular_verificacao_timeout(telefone, 0)
    
    # Cenário 2: Cliente continua pedido (30 minutos - dentro do prazo)
    print("\n📋 CENÁRIO 2: Continuação do pedido (30 minutos)")
    simular_verificacao_timeout(telefone, 30)
    
    # Cenário 3: Cliente retorna após 90 minutos (pedido expirou)
    print("\n📋 CENÁRIO 3: Cliente retorna após 90 minutos (pedido expirou)")
    simular_verificacao_timeout(telefone, 90)
    
    # Cenário 4: Cliente continua novo pedido (15 minutos - dentro do prazo)
    print("\n📋 CENÁRIO 4: Continuação do novo pedido (15 minutos)")
    simular_verificacao_timeout(telefone, 15)
    
    print(f"\n{'='*60}")
    print("✅ DEMONSTRAÇÃO COMPLETA")
    print("\n📝 COMO FUNCIONA O FLUXO NATURAL:")
    print("1️⃣ O agente SEMPRE verifica automaticamente se está dentro da 1 hora")
    print("2️⃣ Se o pedido expirou, ele reinicia AUTOMATICAMENTE")
    print("3️⃣ O cliente NÃO precisa digitar 'pedido' para reiniciar")
    print("4️⃣ A transição é suave e natural")
    print("\n💰 BENEFÍCIOS DO TIMEOUT:")
    print("• Economia de 30% no custo mensal")
    print("• Pedidos sempre relevantes e atuais")
    print("• Experiência mais fluida para o cliente")
    print("• Sistema mais escalável e sustentável")

if __name__ == "__main__":
    main()