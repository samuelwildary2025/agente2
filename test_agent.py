"""
Script de teste para o agente de supermercado
Execute este script para testar o agente localmente sem precisar do servidor web
"""
import os

# Carregar variáveis de ambiente com fallback quando python-dotenv não estiver instalado
def _fallback_load_env(path: str = ".env"):
    try:
        if not os.path.exists(path):
            return
        with open(path, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except Exception:
        pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    _fallback_load_env()

from config.logger import setup_logger

logger = setup_logger(__name__)


def test_conversation():
    """
    Testa uma conversa completa com o agente
    """
    # Importar o agente apenas quando necessário (evitar dependências pesadas no modo --ean)
    from agent import run_agent
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
    
    def _extract_eans(text: str):
        """Extrai pares (EAN, nome) de um texto/JSON retornado pelo smart-responder."""
        import re, json
        pairs = []
        if not isinstance(text, str):
            try:
                text = json.dumps(text)
            except Exception:
                text = str(text)

        # Caso 1: sumário já formatado
        if "EANS_ENCONTRADOS:" in text:
            for line in text.splitlines():
                m = re.search(r"^\s*\d+\)\s*([0-9]{8,14})(?:\s*-\s*(.+))?$", line)
                if m:
                    pairs.append((m.group(1).strip(), (m.group(2) or "").strip()))
            if pairs:
                return pairs

        # Caso 2: tentar JSON estruturado
        try:
            data = json.loads(text)
        except Exception:
            data = None

        def walk(payload):
            if isinstance(payload, dict):
                e = None
                n = None
                for k in ["ean", "ean_code", "codigo_ean", "barcode", "gtin"]:
                    v = payload.get(k)
                    if isinstance(v, (str, int)) and str(v).strip():
                        e = str(v).strip()
                        break
                for k in ["produto", "product", "name", "nome", "title", "descricao", "description"]:
                    v = payload.get(k)
                    if isinstance(v, str) and v.strip():
                        n = v.strip()
                        break
                if e or n:
                    pairs.append((e, n))
                for _, val in payload.items():
                    walk(val)
            elif isinstance(payload, list):
                for it in payload:
                    walk(it)

        if data is not None:
            walk(data)
            if pairs:
                return pairs

        # Caso 3: regex básica no texto bruto
        import re as _re
        eans = _re.findall(r'"codigo_ean"\s*:\s*([0-9]{8,14})', text)
        names = _re.findall(r'"produto"\s*:\s*"([^"]+)"', text)
        for e, n in zip(eans, names):
            pairs.append((e.strip(), n.strip()))
        return pairs

    def test_ean_prompt(query: str | None = None):
        """Teste dedicado para consultar o smart-responder e listar EANs."""
        from tools.http_tools import ean_lookup
        import json
        print("=" * 60)
        print("🧪 TESTE DO SMART-RESPONDER (EAN)")
        print("=" * 60)
        if not query:
            query = input("Consulta de produto (ex.: 'Coca 2L'): ").strip()
        print(f"\nConsulta: {query}")
        resp = ean_lookup(query)
        preview = resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)
        if isinstance(preview, str) and len(preview) > 2000:
            preview = preview[:2000] + "\n... (truncado)"
        print("\nRetorno bruto do smart-responder:\n")
        print(preview)

        pairs = _extract_eans(resp)
        if pairs:
            print("\nEANS encontrados:")
            for i, (e, n) in enumerate(pairs[:10], 1):
                print(f"{i}) {e} - {n or '(sem nome)'}")
            print("\n✅ Comunicação com Supabase OK")
        else:
            print("\n⚠️ Nenhum EAN encontrado.")
            print("Verifique SMART_RESPONDER_URL/SMART_RESPONDER_AUTH/SMART_RESPONDER_APIKEY no .env")

        print("\n" + "=" * 60)
        print("✅ Teste concluído!")
        print("=" * 60)

    if len(sys.argv) > 1:
        if sys.argv[1] == "--tools":
            # Testar ferramentas individualmente
            test_tools()
        elif sys.argv[1] == "--ean":
            # Teste direto do smart-responder
            query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else None
            test_ean_prompt(query)
        else:
            # Testar conversação completa
            test_conversation()
    else:
        # Padrão: conversação completa
        test_conversation()
