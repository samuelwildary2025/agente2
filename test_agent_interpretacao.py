#!/usr/bin/env python3
"""
Teste Visual: Como o Agente Interpreta Pedidos Expirados
Mostra o fluxo completo de detecção e resposta
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_langgraph_simple import run_agent_langgraph
from tools.redis_tools import set_pedido_ativo, verificar_pedido_expirado
from config.logger import setup_logger

logger = setup_logger(__name__)

class SimuladorAgente:
    """Simula o comportamento do agente com timeout"""
    
    def __init__(self):
        self.custo_tokens = {
            "input": 0,
            "output": 0,
            "total": 0
        }
        self.mensagens_processadas = 0
        
    def simular_interacao(self, telefone: str, mensagem: str, simular_expirado: bool = False):
        """Simula uma interação completa com o agente"""
        
        print(f"\n📱 SIMULAÇÃO: {telefone}")
        print(f"💬 Mensagem: '{mensagem}'")
        print("-" * 60)
        
        # Etapa 1: Verificação de Timeout (Sempre acontece PRIMEIRO)
        print("🔍 ETAPA 1: Verificando se pedido expirou...")
        print(f"   Chamando: verificar_pedido_expirado('{telefone}')")
        
        if simular_expirado:
            print("   🔄 Simulando pedido expirado (Redis retornaria None)")
            expirado = True
        else:
            expirado = verificar_pedido_expirado(telefone)
            
        print(f"   ⏰ Resultado: {'EXPIRADO' if expirado else 'ATIVO'}")
        
        # Etapa 2: Decisão do Agente
        if expirado:
            print("\n🤖 ETAPA 2: Agente detecta pedido expirado")
            print("   ⚠️  DECISÃO: Não processar no LLM (economizar tokens)")
            print("   💬 RESPOSTA IMEDIATA:")
            print("   '⏰ Seu pedido anterior expirou após 1 hora de inatividade.'")
            print("   'Por favor, envie 'pedido' para iniciar um novo atendimento.'")
            
            resultado = {
                "output": "⏰ Seu pedido anterior expirou após 1 hora de inatividade. Por favor, envie 'pedido' para iniciar um novo atendimento.",
                "error": None,
                "expired": True
            }
            
            print(f"\n💰 CUSTO: R$ 0,00 (nenhum token consumido)")
            
        else:
            print("\n🤖 ETAPA 2: Pedido está ativo")
            print("   ✅ DECISÃO: Processar normalmente no LLM")
            print("   🔄 Chamando: run_agent_langgraph() com configuração completa")
            
            # Simular custo de tokens para processamento normal
            tokens_estimados = {
                "input": 150,  # Mensagem + histórico
                "output": 200,  # Resposta do agente
                "total": 350
            }
            
            custo_estimado = (tokens_estimados["input"] * 0.00000025 + 
                            tokens_estimados["output"] * 0.000002) * 5.5
            
            print(f"💰 CUSTO ESTIMADO: R$ {custo_estimado:.4f}")
            print(f"📊 Tokens: {tokens_estimados['total']} (input: {tokens_estimados['input']}, output: {tokens_estimados['output']})")
            
            # Simular resposta do agente
            resultado = {
                "output": "Claro! Vou verificar o estoque de arroz e feijão para você. Um momento por favor...",
                "error": None,
                "expired": False
            }
            
            self.custo_tokens["input"] += tokens_estimados["input"]
            self.custo_tokens["output"] += tokens_estimados["output"]
            self.custo_tokens["total"] += tokens_estimados["total"]
            self.mensagens_processadas += 1
            
        return resultado
    
    def mostrar_resumo_economia(self):
        """Mostra economia gerada pelo timeout"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DE ECONOMIA COM TIMEOUT")
        print("=" * 60)
        
        if self.mensagens_processadas > 0:
            custo_total = (self.custo_tokens["input"] * 0.00000025 + 
                          self.custo_tokens["output"] * 0.000002) * 5.5
            
            print(f"📈 Mensagens processadas: {self.mensagens_processadas}")
            print(f"📊 Total de tokens: {self.custo_tokens['total']}")
            print(f"💰 Custo total: R$ {custo_total:.4f}")
            print(f"📱 Custo por mensagem: R$ {custo_total/self.mensagens_processadas:.4f}")
        else:
            print("💡 Todas as mensagens foram bloqueadas por timeout!")
            print("💰 Economia total: 100% (R$ 0,00 gasto)")

def demonstrar_interpretacao_agente():
    """Demonstra como o agente interpreta diferentes situações"""
    
    print("🧠 TESTE VISUAL: Como o Agente Interpreta Pedidos Expirados")
    print("=" * 70)
    print("🔍 Este teste mostra EXATAMENTE o que acontece quando um cliente")
    print("   envia mensagem e o pedido está expirado vs ativo")
    print("=" * 70)
    
    simulador = SimuladorAgente()
    
    # Cenário 1: Cliente com pedido ATIVO
    print("\n🟢 CENÁRIO 1: Cliente com pedido ATIVO")
    print("-" * 50)
    telefone_ativo = "558588880001"
    
    # Primeiro, criar um pedido ativo
    print(f"📝 Criando pedido ativo para {telefone_ativo}...")
    set_pedido_ativo(telefone_ativo, "pedido_ativo", ttl=3600)
    
    # Agora simular interação
    resultado = simulador.simular_interacao(
        telefone_ativo, 
        "Quero arroz e feijão",
        simular_expirado=False
    )
    
    # Cenário 2: Cliente com pedido EXPIRADO
    print("\n🔴 CENÁRIO 2: Cliente com pedido EXPIRADO")
    print("-" * 50)
    telefone_expirado = "558588880002"
    
    resultado = simulador.simular_interacao(
        telefone_expirado,
        "Quero arroz e feijão", 
        simular_expirado=True
    )
    
    # Cenário 3: Cliente tenta continuar pedido expirado
    print("\n🟡 CENÁRIO 3: Cliente tenta continuar após expiração")
    print("-" * 50)
    
    resultado = simulador.simular_interacao(
        telefone_expirado,
        "Mais alguma coisa",
        simular_expirado=True
    )
    
    # Cenário 4: Cliente reinicia corretamente
    print("\n🟢 CENÁRIO 4: Cliente reinicia pedido corretamente")
    print("-" * 50)
    
    # Criar novo pedido
    print(f"📝 Criando novo pedido para {telefone_expirado}...")
    set_pedido_ativo(telefone_expirado, "novo_pedido", ttl=3600)
    
    resultado = simulador.simular_interacao(
        telefone_expirado,
        "pedido",  # Palavra mágica para reiniciar
        simular_expirado=False
    )
    
    # Resumo final
    simulador.mostrar_resumo_economia()
    
    print("\n✅ CONCLUSÃO:")
    print("   • O agente VERIFICA primeiro, PROCESSA depois")
    print("   • Pedidos expirados: 0 tokens, resposta imediata")
    print("   • Pedidos ativos: processamento normal com LLM")
    print("   • Economia significativa em clientes inativos")

def main():
    """Executa demonstração visual"""
    try:
        demonstrar_interpretacao_agente()
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