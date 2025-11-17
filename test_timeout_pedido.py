#!/usr/bin/env python3
"""
Teste de timeout de pedido - Valida sistema de expiração de 1 hora
"""

import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.redis_tools import (
    set_pedido_ativo, 
    verificar_pedido_expirado, 
    renovar_pedido_timeout,
    confirme_pedido_ativo,
    get_redis_client
)
from config.logger import setup_logger

logger = setup_logger(__name__)

def test_timeout_pedido():
    """Testa o sistema de timeout de pedido com 1 hora"""
    print("🧪 Testando Sistema de Timeout de Pedido (1 hora)")
    print("=" * 60)
    
    telefone = "5585999999999"
    
    # Test 1: Criar pedido
    print(f"📱 Telefone de teste: {telefone}")
    print("\n1️⃣ Criando pedido ativo...")
    
    resultado = set_pedido_ativo(telefone, "ativo", ttl=5)  # 5 segundos para teste rápido
    print(f"✅ {resultado}")
    
    # Test 2: Verificar se está ativo
    print("\n2️⃣ Verificando se pedido está ativo...")
    status = confirme_pedido_ativo(telefone)
    print(f"📊 {status}")
    
    # Test 3: Verificar se não expirou
    print("\n3️⃣ Verificando se pedido NÃO expirou (imediatamente)...")
    expirado = verificar_pedido_expirado(telefone)
    print(f"⏰ Pedido expirado? {'❌ SIM' if expirado else '✅ NÃO'}")
    
    if expirado:
        print("❌ ERRO: Pedido não deveria estar expirado agora!")
        return False
    
    # Test 4: Aguardar expiração
    print(f"\n4️⃣ Aguardando 6 segundos para expiração...")
    time.sleep(6)
    
    # Test 5: Verificar se expirou
    print("\n5️⃣ Verificando se pedido expirou (após timeout)...")
    expirado = verificar_pedido_expirado(telefone)
    print(f"⏰ Pedido expirado? {'✅ SIM' if expirado else '❌ NÃO'}")
    
    if not expirado:
        print("❌ ERRO: Pedido deveria estar expirado agora!")
        return False
    
    # Test 6: Tentar renovar pedido expirado
    print("\n6️⃣ Tentando renovar pedido expirado...")
    renovado = renovar_pedido_timeout(telefone, ttl=5)
    print(f"🔄 Pedido renovado? {'✅ SIM' if renovado else '❌ NÃO'}")
    
    if renovado:
        print("❌ ERRO: Pedido expirado não deveria poder ser renovado!")
        return False
    
    # Test 7: Criar novo pedido
    print("\n7️⃣ Criando novo pedido...")
    resultado = set_pedido_ativo(telefone, "novo_pedido", ttl=5)
    print(f"✅ {resultado}")
    
    # Test 8: Renovar pedido ativo
    print("\n8️⃣ Renovando pedido ativo...")
    renovado = renovar_pedido_timeout(telefone, ttl=5)
    print(f"🔄 Pedido renovado? {'✅ SIM' if renovado else '❌ NÃO'}")
    
    if not renovado:
        print("❌ ERRO: Pedido ativo deveria poder ser renovado!")
        return False
    
    # Test 9: Simular comportamento do agente com pedido expirado
    print("\n9️⃣ Simulando comportamento do agente com pedido expirado...")
    time.sleep(6)  # Aguardar nova expiração
    
    if verificar_pedido_expirado(telefone):
        print("✅ Pedido expirado detectado corretamente!")
        print("🤖 Agente responde: '⏰ Seu pedido anterior expirou após 1 hora de inatividade...'")
    else:
        print("❌ ERRO: Pedido deveria estar expirado!")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Todos os testes de timeout foram executados com sucesso!")
    print("📊 Sistema de timeout de 1 hora está funcionando corretamente")
    return True

def test_timeout_scenarios_praticos():
    """Testa cenários práticos de timeout"""
    print("\n🎯 Testando Cenários Práticos de Timeout")
    print("=" * 60)
    
    # Cenário 1: Cliente faz pedido e some por 2 horas
    print("📋 Cenário 1: Cliente some por mais de 1 hora")
    telefone1 = "558588880001"
    
    print(f"  📱 Cliente {telefone1} faz pedido...")
    set_pedido_ativo(telefone1, "pedido_iniciado", ttl=3)  # 3 segundos para teste
    print(f"  ⏰ Aguardando 4 segundos (simulando 1+ hora)...")
    time.sleep(4)
    
    if verificar_pedido_expirado(telefone1):
        print("  ✅ Pedido expirado corretamente - cliente deve reiniciar")
    else:
        print("  ❌ ERRO: Pedido deveria estar expirado")
        return False
    
    # Cenário 2: Cliente ativo mantém pedido vivo
    print("\n📋 Cenário 2: Cliente ativo (renovação automática)")
    telefone2 = "558588880002"
    
    print(f"  📱 Cliente {telefone2} faz pedido...")
    set_pedido_ativo(telefone2, "pedido_ativo", ttl=3)
    
    print(f"  💬 Simulando interação do cliente (renova timeout)...")
    renovar_pedido_timeout(telefone2, ttl=3)
    time.sleep(2)
    
    if not verificar_pedido_expirado(telefone2):
        print("  ✅ Pedido mantido ativo por renovação")
    else:
        print("  ❌ ERRO: Pedido não deveria estar expirado")
        return False
    
    print("\n✅ Cenários práticos validados com sucesso!")
    return True

def main():
    """Executa todos os testes de timeout"""
    print("🚀 Iniciando Testes de Timeout de Pedido")
    print("⚠️  Certifique-se de que o Redis está em execução")
    
    # Verificar conexão com Redis
    client = get_redis_client()
    if client is None:
        print("❌ ERRO: Redis não está disponível. Inicie o Redis primeiro.")
        print("💡 Dica: Execute 'redis-server' ou use Docker: docker run -d -p 6379:6379 redis")
        return False
    
    try:
        # Executar testes
        sucesso1 = test_timeout_pedido()
        sucesso2 = test_timeout_scenarios_praticos()
        
        if sucesso1 and sucesso2:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Sistema de timeout de 1 hora está pronto para produção")
            return True
        else:
            print("\n❌ ALGUNS TESTES FALHARAM!")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️ Teste interrompido pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)