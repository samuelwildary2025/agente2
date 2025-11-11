"""
Script de teste para o agente de supermercado
Execute este script para testar o agente localmente sem precisar do servidor web
"""
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

from agent import run_agent
from config.logger import setup_logger

logger = setup_logger(__name__)


def test_conversation():
    """
    Testa uma conversa completa com o agente
    """
    # Telefone de teste
    telefone_teste = "5511999998888"
    
    print("=" * 60)
    print("🤖 TESTE DO AGENTE DE SUPERMERCADO")
    print("=" * 60)
    print(f"Telefone de teste: {telefone_teste}")
    print("Digite 'sair' para encerrar o teste")
    print("=" * 60)
    
    # Conversas de exemplo (descomente para testar automaticamente)
    conversas_exemplo = [
        # "Olá! Quais são os horários de funcionamento?",
        # "Vocês têm arroz integral em estoque?",
        # "Qual o preço do feijão preto?",
        # "Quero fazer um pedido de 2kg de arroz e 1kg de feijão",
        # "Confirma o pedido",
    ]
    
    # Modo interativo
    while True:
        print("\n" + "-" * 60)
        mensagem = input("Você: ").strip()
        
        if not mensagem:
            continue
        
        if mensagem.lower() in ["sair", "exit", "quit"]:
            print("\n👋 Encerrando teste...")
            break
        
        print("\n🤖 Agente está processando...\n")
        
        # Executar agente
        result = run_agent(telefone_teste, mensagem)
        
        if result["error"]:
            print(f"❌ ERRO: {result['error']}\n")
        
        print(f"Agente: {result['output']}")
    
    print("\n" + "=" * 60)
    print("✅ Teste concluído!")
    print("=" * 60)


def test_tools():
    """
    Testa cada ferramenta individualmente
    """
    print("=" * 60)
    print("🔧 TESTE DAS FERRAMENTAS")
    print("=" * 60)
    
    # Teste 1: Ferramenta de tempo
    print("\n1️⃣ Testando ferramenta de tempo...")
    from tools.time_tool import get_current_time
    print(get_current_time())
    
    # Teste 2: Ferramenta Redis (se configurado)
    print("\n2️⃣ Testando ferramentas Redis...")
    from tools.redis_tools import set_pedido_ativo, confirme_pedido_ativo
    
    telefone_teste = "5511999998888"
    print(f"Definindo pedido ativo para {telefone_teste}...")
    print(set_pedido_ativo(telefone_teste, "teste", 60))
    
    print(f"Verificando pedido ativo...")
    print(confirme_pedido_ativo(telefone_teste))
    
    # Teste 3: Base de conhecimento (se configurado)
    print("\n3️⃣ Testando base de conhecimento...")
    try:
        from tools.kb_tools import ean_retrieve
        print(ean_retrieve("política de devolução"))
    except Exception as e:
        print(f"⚠️ Base de conhecimento não configurada: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Teste de ferramentas concluído!")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--tools":
        # Testar ferramentas individualmente
        test_tools()
    else:
        # Testar conversação completa
        test_conversation()
