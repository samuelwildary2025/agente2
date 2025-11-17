#!/usr/bin/env python3
"""
Teste: Como fica a memória do agente com timeout (últimas 20 mensagens)

Demonstra o que acontece com o histórico quando pedido expira.
"""

def mostrar_memoria_timeout():
    """Mostra como fica a memória do agente"""
    
    print("💾 MEMÓRIA DO AGENTE: Timeout vs Histórico de 20 Mensagens")
    print("="*70)
    
    print("\n📋 CONFIGURAÇÃO ATUAL:")
    print("• O agente usa as últimas 20 mensagens como contexto")
    print("• Mensagens são armazenadas no PostgreSQL")
    print("• Timeout de pedido é controlado pelo Redis (1 hora)")
    print("• São sistemas INDEPENDENTES!")
    
    print("\n" + "="*70)
    print("🕘 09:15 - Conversa da manhã:")
    print("📱 Cliente: Oi, quero arroz")
    print("🤖 Agente: Encontrei arroz por R$ 6,90")
    print("📱 Cliente: Quero 2 pacotes")
    print("🤖 Agente: Ok, anotado!")
    print("📨 [4 mensagens adicionadas ao histórico PostgreSQL]")
    
    print("\n⏰ [Pedido expira às 10:15 - Redis apaga a chave]")
    print("💡 [PostgreSQL MANTÉM todas as mensagens!]")
    
    print("\n" + "="*70)
    print("🕓 18:45 - Cliente retorna (9 horas depois):")
    print("📱 Cliente: Vou querer feijão também")
    
    print("\n🤖 [Agente verifica timeout com Redis]")
    print("🔍 Redis: Pedido expirado (chave não existe mais)")
    print("🤖 Agente: 'Seu pedido anterior expirou...'")
    
    print("\n📊 HISTÓRICO POSTGRESQL (20 mensagens mais recentes):")
    print("1. Cliente: 'Vou querer feijão também'")
    print("2. Agente:  'Seu pedido anterior expirou...'")
    print("3. Cliente: 'Ah entendi, quero arroz e feijão'")
    print("4. Agente:  'Perfeito! Vou verificar...'")
    print("...")
    print("20. Agente: 'Ok, anotado!' (da manhã)")
    
    print("\n💡 O QUE O AGENTE VÊ:")
    print("• As mensagens da manhã AINDA ESTÃO na memória!")
    print("• Mas o pedido NO Redis expirou")
    print("• O agente sabe que precisa reiniciar")
    print("• Mas tem contexto do que foi falado antes")

def explicar_diferenca_sistemas():
    """Explica a diferença entre Redis e PostgreSQL"""
    
    print("\n" + "="*70)
    print("🔧 DIFERENÇA ENTRE OS SISTEMAS:")
    
    print("\n📦 REDIS (Timeout de Pedido):")
    print("• Guarda: Status do pedido (ativo/expirado)")
    print("• Tempo: 1 hora (TTL automático)")
    print("• Quando expira: APAGA tudo completamente")
    print("• Função: Controlar se pedido está válido")
    
    print("\n🗄️ POSTGRESQL (Histórico de Conversação):")
    print("• Guarda: Todas as mensagens da conversa")
    print("• Tempo: Para sempre (ou até limpar manualmente)")
    print("• Quando expira: NUNCA apaga automaticamente")
    print("• Função: Dar contexto ao agente")
    
    print("\n🔄 COMO FUNCIONAM JUNTOS:")
    print("1. Redis expira → Pedido reinicia")
    print("2. PostgreSQL mantém → Agente tem memória")
    print("3. Agente sabe que pedido novo, mas lembra contexto")
    print("4. Cliente tem experiência natural")

def mostrar_exemplo_pratico():
    """Mostra exemplo prático de como fica"""
    
    print("\n" + "="*70)
    print("💬 EXEMPLO PRÁTICO NA CONVERSA:")
    
    print("\n🕘 Manhã - PostgreSQL guarda:")
    print("Cliente: 'Oi, quero arroz'")
    print("Agente:  'Encontrei arroz R$ 6,90'")
    
    print("\n🕓 Noite - PostgreSQL ainda tem:")
    print("Cliente: 'Vou querer feijão também'")
    print("Agente:  'Seu pedido anterior expirou...'")
    print("Cliente: 'Ah entendi, quero arroz e feijão'")
    print("Agente:  'Perfeito! Arroz R$ 6,90 e Feijão R$ 8,50'")
    print("          ↑")
    print("          Agente AINDA lembra preço do arroz!")
    
    print("\n💡 VANTAGEM:")
    print("• Agente tem contexto histórico")
    print("• Mas sabe que é novo pedido")
    print("• Pode usar informações anteriores se relevante")
    print("• Experiência mais personalizada")

def main():
    mostrar_memoria_timeout()
    explicar_diferenca_sistemas()
    mostrar_exemplo_pratico()
    
    print("\n" + "="*70)
    print("✅ CONCLUSÃO:")
    print("O PostgreSQL mantém histórico completo (20 mensagens)")
    print("mas o Redis controla timeout do pedido.")
    print("Agente tem MEMÓRIA mas sabe que pedido reiniciou!")

if __name__ == "__main__":
    main()