#!/usr/bin/env python3
"""
Demonstração do Sistema de Timeout de Pedido - 1 Hora
Simula o funcionamento sem depender do Redis
"""

import time
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config.logger import setup_logger

logger = setup_logger(__name__)

class MockRedisClient:
    """Simulação do Redis para demonstração"""
    
    def __init__(self):
        self.data = {}
        self.expirations = {}
        
    def set(self, key: str, value: str, ex: int = 3600):
        """Define valor com expiração"""
        self.data[key] = value
        self.expirations[key] = datetime.now() + timedelta(seconds=ex)
        print(f"💾 Redis SET: {key} = {value} (expira em {ex}s)")
        
    def get(self, key: str) -> Optional[str]:
        """Obtém valor se não expirou"""
        if key not in self.data:
            print(f"🔍 Redis GET: {key} = None (não existe)")
            return None
            
        if key in self.expirations:
            if datetime.now() > self.expirations[key]:
                print(f"⏰ Redis GET: {key} = None (expirou)")
                del self.data[key]
                del self.expirations[key]
                return None
                
        value = self.data[key]
        print(f"🔍 Redis GET: {key} = {value}")
        return value
        
    def exists(self, key: str) -> bool:
        """Verifica se chave existe e não expirou"""
        return self.get(key) is not None
        
    def expire(self, key: str, ex: int):
        """Renova expiração"""
        if key in self.data:
            self.expirations[key] = datetime.now() + timedelta(seconds=ex)
            print(f"🔄 Redis EXPIRE: {key} renovado para {ex}s")
            return True
        return False

class SistemaTimeoutPedido:
    """Sistema de timeout de pedido com 1 hora"""
    
    def __init__(self):
        self.redis = MockRedisClient()
        
    def set_pedido_ativo(self, telefone: str, valor: str = "ativo", ttl: int = 3600) -> str:
        """Define pedido ativo com timeout"""
        key = f"{telefone}pedido"
        self.redis.set(key, valor, ex=ttl)
        return f"✅ Pedido marcado como ativo para {telefone}. Expira em {ttl//60} minutos."
        
    def verificar_pedido_expirado(self, telefone: str) -> bool:
        """Verifica se pedido expirou"""
        key = f"{telefone}pedido"
        valor = self.redis.get(key)
        expirado = valor is None
        print(f"🔍 Verificando pedido para {telefone}: {'EXPIRADO' if expirado else 'ATIVO'}")
        return expirado
        
    def renovar_pedido_timeout(self, telefone: str, ttl: int = 3600) -> bool:
        """Renova timeout do pedido"""
        key = f"{telefone}pedido"
        renovado = self.redis.expire(key, ttl)
        if renovado:
            print(f"✅ Timeout renovado para {telefone} por mais {ttl//60} minutos")
        else:
            print(f"❌ Não foi possível renovar timeout para {telefone}")
        return renovado
        
    def confirme_pedido_ativo(self, telefone: str) -> str:
        """Confirma status do pedido"""
        key = f"{telefone}pedido"
        valor = self.redis.get(key)
        
        if valor is not None:
            return f"✅ Pedido ativo para {telefone}: {valor}"
        else:
            return f"ℹ️ Nenhum pedido ativo encontrado para {telefone}."

def demonstrar_sistema_timeout():
    """Demonstra o sistema de timeout com cenários reais"""
    print("🚀 Demonstração do Sistema de Timeout de Pedido (1 Hora)")
    print("=" * 70)
    
    sistema = SistemaTimeoutPedido()
    telefone = "5585999999999"
    
    print(f"📱 Cliente: {telefone}")
    print("⏰ Tempo de expiração: 1 hora (3600 segundos)")
    print()
    
    # Cenário 1: Cliente inicia pedido
    print("📋 CENÁRIO 1: Cliente inicia pedido")
    print("-" * 40)
    print("[10:00] Cliente envia: 'Oi, quero fazer um pedido'")
    
    resultado = sistema.set_pedido_ativo(telefone, "pedido_iniciado", ttl=3600)
    print(f"🤖 Sistema: {resultado}")
    print()
    
    # Cenário 2: Interação normal
    print("📋 CENÁRIO 2: Interação normal (dentro da hora)")
    print("-" * 40)
    print("[10:15] Cliente envia: 'Quero arroz e feijão'")
    
    if not sistema.verificar_pedido_expirado(telefone):
        print("✅ Pedido está ativo - processando normalmente...")
        sistema.renovar_pedido_timeout(telefone, ttl=3600)  # Renova após interação
        print("🔄 Timeout renovado para mais 1 hora!")
    else:
        print("❌ Pedido expirado - cliente precisa reiniciar")
    print()
    
    # Cenário 3: Cliente some por mais de 1 hora
    print("📋 CENÁRIO 3: Cliente some por mais de 1 hora")
    print("-" * 40)
    print("[11:30] Cliente volta após 1h30min e envia: 'Mais alguma coisa'")
    
    # Simular expiração (usar TTL curto para demonstração)
    sistema.set_pedido_ativo(telefone + "_expirado", "pedido_expirado", ttl=2)
    print("⏰ Aguardando 3 segundos para simular expiração...")
    time.sleep(3)
    
    if sistema.verificar_pedido_expirado(telefone + "_expirado"):
        print("⏰ Pedido expirado detectado!")
        print("🤖 Sistema responde:")
        print("   '⏰ Seu pedido anterior expirou após 1 hora de inatividade.'")
        print("   'Por favor, envie 'pedido' para iniciar um novo atendimento.'")
    else:
        print("❌ Erro: pedido deveria estar expirado")
    print()
    
    # Cenário 4: Cliente reinicia pedido
    print("📋 CENÁRIO 4: Cliente reinicia pedido")
    print("-" * 40)
    print("[11:32] Cliente envia: 'pedido'")
    
    resultado = sistema.set_pedido_ativo(telefone, "novo_pedido", ttl=3600)
    print(f"🤖 Sistema: {resultado}")
    print("✅ Novo pedido iniciado com sucesso!")
    print()
    
    # Status final
    print("📊 STATUS FINAL")
    print("=" * 70)
    status = sistema.confirme_pedido_ativo(telefone)
    print(f"📋 {status}")
    print()
    print("✅ Sistema de timeout de 1 hora funcionando perfeitamente!")
    print("💡 Benefícios:")
    print("   • Evita pedidos abandonados ocupando memória")
    print("   • Garante que clientes ativos mantêm sessão viva")
    print("   • Custa zero para pedidos expirados (economia de tokens)")
    print("   • Experiência limpa para o cliente")

def main():
    """Executa demonstração"""
    try:
        demonstrar_sistema_timeout()
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