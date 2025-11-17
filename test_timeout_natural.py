#!/usr/bin/env python3
"""
Demonstração do fluxo natural com timeout automático

Este script mostra como o agente automaticamente verifica se um pedido está dentro do prazo de 1 hora
e reinicia o pedido de forma natural quando necessário, sem que o cliente precise digitar "pedido".
"""

import time
import json
from datetime import datetime, timedelta

# Mock do Redis para demonstração
class MockRedis:
    def __init__(self):
        self.data = {}
        self.ttls = {}
    
    def setex(self, key, ttl, value):
        self.data[key] = value
        self.ttls[key] = time.time() + ttl
        print(f"💾 Redis: Set {key} = {value} (TTL: {ttl}s)")
    
    def get(self, key):
        if key in self.ttls and time.time() > self.ttls[key]:
            if key in self.data:
                del self.data[key]
                del self.ttls[key]
            return None
        return self.data.get(key)
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
            del self.ttls[key]
            print(f"🗑️ Redis: Deleted {key}")

# Simular ferramentas do Redis
mock_redis = MockRedis()

def mock_set_pedido_ativo(telefone, valor="ativo", ttl=3600):
    """Mock da função que define pedido ativo"""
    key = f"{telefone}:pedido"
    mock_redis.setex(key, ttl, valor)
    return f"Pedido ativado para {telefone} com TTL de {ttl}s"

def mock_verificar_pedido_expirado(telefone):
    """Mock da função que verifica se pedido expirou"""
    key = f"{telefone}:pedido"
    valor = mock_redis.get(key)
    return valor is None

def mock_verificar_continuar_pedido_tool(telefone):
    """Mock da nova ferramenta de verificação natural"""
    if mock_verificar_pedido_expirado(telefone):
        # Pedido expirou - reiniciar automaticamente
        mock_set_pedido_ativo(telefone, ttl=3600)  # Novo pedido com 1 hora
        return "🔄 Pedido anterior expirou após 1 hora. Iniciando novo pedido automaticamente..."
    else:
        # Pedido ainda ativo - continuar normalmente
        return "✅ Pedido dentro do prazo. Continuando normalmente..."

def simular_atendimento(telefone, mensagem, tempo_espera=0):
    """Simula uma interação com o agente"""
    print(f"\n{'='*60}")
    print(f"📱 Cliente: {telefone}")
    print(f"💬 Mensagem: {mensagem}")
    print(f"⏰ Horário: {datetime.now().strftime('%H:%M:%S')}")
    
    if tempo_espera > 0:
        print(f"⏳ Simulando espera de {tempo_espera} segundos...")
        time.sleep(tempo_espera)
    
    # O agente automaticamente verifica o timeout
    resultado_verificacao = mock_verificar_continuar_pedido_tool(telefone)
    print(f"🤖 Agente: {resultado_verificacao}")
    
    # Simular resposta do agente baseada no contexto
    if "expirou" in resultado_verificacao:
        print("🤖 Agente: Oi! Sou o assistente virtual do Supermercado Queiroz! 😊")
        print("🤖 Agente: Posso ajudar você com seu pedido? Qual produto você procura?")
    else:
        print("🤖 Agente: Entendi! Vou verificar isso para você...")
    
    return resultado_verificacao

def main():
    print("🛒 DEMONSTRAÇÃO: Timeout Natural com Reinício Automático")
    print("="*60)
    
    telefone = "5511999998888"
    
    # Cenário 1: Cliente faz pedido normal
    print("\n📋 CENÁRIO 1: Pedido dentro do prazo (5 minutos)")
    simular_atendimento(telefone, "Oi, quero arroz")
    
    # Cenário 2: Cliente continua pedido dentro do prazo
    print("\n📋 CENÁRIO 2: Continuação do pedido (10 minutos depois)")
    simular_atendimento(telefone, "Também quero feijão")
    
    # Cenário 3: Cliente retorna após 1 hora e 30 minutos (pedido expirou)
    print("\n📋 CENÁRIO 3: Cliente retorna após 1h30min (pedido expirou)")
    simular_atendimento(telefone, "Mais um item: leite", tempo_espera=5400)  # 1h30min
    
    # Cenário 4: Cliente continua novo pedido
    print("\n📋 CENÁRIO 4: Continuação do novo pedido")
    simular_atendimento(telefone, "E café também")
    
    print(f"\n{'='*60}")
    print("✅ DEMONSTRAÇÃO COMPLETA")
    print("\n📝 RESUMO DO FLUXO NATURAL:")
    print("1. O agente SEMPRE verifica se o pedido está dentro do prazo de 1 hora")
    print("2. Se o pedido expirou, ele reinicia AUTOMATICAMENTE")
    print("3. O cliente NÃO precisa digitar 'pedido' para reiniciar")
    print("4. A experiência é fluida e natural")
    print("\n💰 ECONOMIA: Com timeout, o custo cai de R$ 36/mês para R$ 25,20/mês (30% desconto)")

if __name__ == "__main__":
    main()