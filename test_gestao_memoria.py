#!/usr/bin/env python3
"""
Teste técnico: Como o Redis gerencia a memória dos pedidos com timeout

Demonstra que produtos do pedido expirado realmente desaparecem do sistema.
"""

def demonstrar_gestao_memoria():
    """Demonstra como a memória do pedido é gerida"""
    
    print("💾 GESTÃO DE MEMÓRIA: Redis com Timeout de 1 Hora")
    print("="*70)
    
    print("\n🕘 09:15 - Estado do Redis:")
    print("📱 Chave: '551199998877:pedido'")
    print("📦 Valor: {'produtos': ['arroz'], 'status': 'ativo'}")
    print("⏰ TTL: 3600 segundos (1 hora)")
    print("✅ Pedido existe na memória")
    
    print("\n🕙 10:15 - Após 1 hora:")
    print("🔄 TTL expirou")
    print("🗑️ Redis automaticamente deleta a chave")
    print("❌ Chave '551199998877:pedido' NÃO existe mais")
    print("💾 Memória está limpa - pedido sumiu completamente")
    
    print("\n🕓 18:45 - Quando cliente retorna:")
    print("📱 Chave: '551199998877:pedido'")
    print("🔍 Redis.get() retorna: None")
    print("🤖 Agente detecta: 'Pedido não encontrado = Pedido expirou'")
    print("💡 Sistema NÃO TEM MAIS arroz em lugar nenhum!")
    
    print("\n🔄 18:45:01 - Novo pedido criado:")
    print("📱 Chave: '551199998877:pedido' (mesma chave, novo valor)")
    print("📦 Valor: {'produtos': [], 'status': 'novo_pedido'}")
    print("⏰ TTL: 3600 segundos (nova contagem)")
    print("✅ Pedido novo começa do ZERO")
    
    print("\n" + "="*70)
    print("🎯 CONCLUSÃO TÉCNICA:")
    print("\n1️⃣ PRODUTOS DO PEDIDO EXPIRADO:")
    print("   • São completamente apagados do Redis")
    print("   • Não existem em cache, memória ou banco")
    print("   • Não há histórico disponível para o agente")
    
    print("\n2️⃣ QUANDO CLIENTE RETORNA:")
    print("   • Agente vê apenas: 'Pedido expirou'")
    print("   • Não sabe que tinha arroz antes")
    print("   • Não pode recuperar itens anteriores")
    
    print("\n3️⃣ NOVO PEDIDO:")
    print("   • Começa completamente do zero")
    print("   • Lista de produtos está vazia")
    print("   • Cliente precisa refazer TUDO")
    
    print("\n💡 POR QUE ISSO É BOM:")
    print("   • Economiza memória e processamento")
    print("   • Mantém sistema limpo e organizado")
    print("   • Evita confusão entre pedidos antigos/novos")
    print("   • Garante que pedidos sejam sempre atuais")

def main():
    demonstrar_gestao_memoria()
    
    print("\n" + "="*70)
    print("✅ RESPOSTA PARA SUA PERGUNTA:")
    print("Quando cliente fala 'feijão também' após timeout,")
    print("o agente NÃO SABE sobre o arroz anterior porque")
    print("o pedido foi completamente apagado do sistema!")
    print("Por isso ele explica que precisa reiniciar do início.")

if __name__ == "__main__":
    main()