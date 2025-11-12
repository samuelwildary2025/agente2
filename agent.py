"""
Agente de IA para Atendimento de Supermercado
Utiliza LangChain para orquestração de ferramentas e memória de conversação
(v7 - Remove classe NonStreamingChatOpenAI e injeção de client)
"""
from typing import Dict, Any
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import httpx
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import AIMessageChunk, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentType
from langchain_core.tools import tool
from langchain_community.chat_message_histories import PostgresChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from pathlib import Path

from config.settings import settings
from config.logger import setup_logger
from tools.http_tools import estoque, pedidos, alterar, ean_lookup, estoque_preco
from tools.redis_tools import set_pedido_ativo, confirme_pedido_ativo
from tools.time_tool import get_current_time

logger = setup_logger(__name__)


# ============================================
# Definição das Ferramentas (Tools)
# ============================================

@tool
def estoque_tool(url: str) -> str:
    """
    Consultar estoque e preço atual dos produtos no sistema do supermercado.
    
    A URL completa para a consulta deve ser fornecida, por exemplo:
    'https://wildhub-wildhub-sistema-supermercado.5mos1l.easypanel.host/api/produtos/consulta?nome=arroz'
    
    Use esta ferramenta quando o cliente perguntar sobre disponibilidade ou preço de produtos.
    """
    return estoque(url)


@tool
def pedidos_tool(json_body: str) -> str:
    """
    Enviar o pedido finalizado para o painel dos funcionários (dashboard).
    
    O corpo da requisição deve ser um JSON (em formato string) com os detalhes do pedido.
    Exemplo: '{"cliente": "João Silva", "telefone": "5511999998888", "itens": [{"produto": "Arroz Integral 1kg", "quantidade": 2, "preco": 8.50}], "total": 17.00}'
    
    Use esta ferramenta SOMENTE quando o cliente confirmar que deseja finalizar o pedido.
    """
    return pedidos(json_body)


@tool
def alterar_tool(telefone: str, json_body: str) -> str:
    """
    Atualizar o pedido no painel dos funcionários (dashboard).
    
    O telefone do cliente deve ser fornecido para identificar o pedido.
    O corpo da requisição deve ser um JSON (em formato string) com os dados a serem atualizados.
    
    Exemplo: alterar_tool("5511987654321", '{"status": "cancelado", "motivo": "Cliente desistiu"}')
    
    Use esta ferramenta quando o cliente quiser modificar ou cancelar um pedido existente.
    """
    return alterar(telefone, json_body)


@tool
def set_tool(telefone: str, valor: str = "ativo", ttl: int = 600) -> str:
    """
    Define uma chave no Redis para indicar que um pedido está ativo.
    
    A chave é formada por: {telefone}pedido
    O TTL padrão é de 600 segundos (10 minutos).
    
    Use esta ferramenta APÓS finalizar um pedido com sucesso para marcar que o cliente tem um pedido ativo.
    """
    return set_pedido_ativo(telefone, valor, ttl)


@tool
def confirme_tool(telefone: str) -> str:
    """
    Verifica se um pedido está ativo no Redis.
    
    A chave é formada por: {telefone}pedido
    Retorna o valor da chave ou uma mensagem de que não foi encontrado.
    
    Use esta ferramenta para verificar se o cliente já tem um pedido em andamento antes de criar um novo.
    """
    return confirme_pedido_ativo(telefone)


@tool
def time_tool() -> str:
    """
    Retorna a data e hora atual no fuso horário de São Paulo (America/Sao_Paulo).
    
    Use esta ferramenta quando o cliente perguntar sobre horário de funcionamento,
    horário de entrega, ou qualquer informação relacionada ao tempo.
    """
    return get_current_time()


@tool
def ean_tool(query: str) -> str:
    """
    Buscar EAN/infos do produto via Supabase Functions (smart-responder).
    Envie o texto mencionado pelo cliente (nome/descrição) como 'query'.
    """
    return ean_lookup(query)

@tool("ean")
def ean_tool_alias(query: str) -> str:
    """
    Alias de ferramenta: `ean`
    Buscar EAN/infos do produto via smart-responder enviando o nome/descrição.
    """
    return ean_lookup(query)


@tool
def estoque_preco_tool(ean: str) -> str:
    """
    Consultar preço e disponibilidade pelo EAN.
    Informe apenas os dígitos do código EAN.

    Observações:
    - Retorna somente itens com disponibilidade/estoque positivo.
    - Remove campos de quantidade de estoque da saída.
    - Normaliza o preço no campo "preco" quando possível.
    Use esta ferramenta para montar opções (nome + variação + preço)
    e perguntar tamanho/gramagem quando o pedido for genérico.
    """
    return estoque_preco(ean)

@tool("estoque")
def estoque_preco_alias(ean: str) -> str:
    """
    Alias de ferramenta: `estoque`
    Consulta preço e disponibilidade pelo EAN (apenas dígitos).
    Filtra apenas itens com estoque e normaliza o preço em `preco`.
    """
    return estoque_preco(ean)



# Lista de todas as ferramentas
TOOLS = [
    estoque_tool,
    pedidos_tool,
    alterar_tool,
    set_tool,
    confirme_tool,
    time_tool,
    ean_tool,
    ean_tool_alias,
    estoque_preco_tool,
    estoque_preco_alias,
    
]


# ============================================
# Configuração do Agente
# ============================================

def _load_agent_prompt() -> str:
    """Carrega o prompt do agente de um arquivo externo obrigatório."""
    
    base_dir = Path(__file__).resolve().parent
    prompt_path = str((base_dir / "prompts" / "agent_system.md"))

    try:
        text = Path(prompt_path).read_text(encoding="utf-8")
        logger.info(f"Carregado prompt único em: {prompt_path}")
        return text
    except Exception as e:
        logger.error(f"FALHA CRÍTICA: Não foi possível carregar o prompt em {prompt_path}. Erro: {e}")
        raise

def create_agent() -> AgentExecutor:
    """
    Cria e retorna o AgentExecutor configurado (MODO MODERNO - LCEL)
    """
    logger.info("Criando agente de IA (VERSÃO CORRIGIDA v7 - LCEL)...")

    # --- CORREÇÃO v4: (Manter) ---
    os.environ.pop("http_proxy", None)
    os.environ.pop("https://_proxy", None)
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)
    logger.info("Variáveis de ambiente de proxy (se existiam) foram removidas.")
    
    # ==================================================================
    # INÍCIO DA CORREÇÃO (v7 - Simplificação do LLM)
    # ==================================================================
    
    # Removemos a classe 'NonStreamingChatOpenAI' e a injeção do 'httpx.Client'
    # Deixamos o ChatOpenAI padrão criar seu próprio cliente.
    
    llm_kwargs = {
        "model": settings.llm_model,
        "openai_api_key": settings.openai_api_key,
        "streaming": False, # Garantir que não use streaming
    }
    
    if "gpt-5-mini" in str(settings.llm_model):
        llm_kwargs["temperature"] = 1.0
    else:
        llm_kwargs["temperature"] = settings.llm_temperature

    # Remover import do cliente OpenAI
    // ... existing code ...
    # Remover qualquer instância de OpenAI
    llm_kwargs = {
        "model": settings.llm_model,
        "openai_api_key": settings.openai_api_key,
        "streaming": False,
        "temperature": settings.llm_temperature,
    }
    llm = ChatOpenAI(**llm_kwargs)
    logger.info(f"LLM configurado: {settings.llm_model}")
    
    # ==================================================================
    # FIM DA CORREÇÃO (v7)
    # ==================================================================
    
    # 1. Carregar o texto do prompt do sistema
    system_prompt_raw = _load_agent_prompt()
    system_prompt_text = (
        system_prompt_raw
        .replace("{base_url}", settings.supermercado_base_url)
        .replace("{ean_base}", settings.estoque_ean_base_url)
    )
    
    # 2. Criar o template do prompt (moderno)
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=system_prompt_text),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessage(content="{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"), # Essencial para o agente
    ])
    
    # 3. Criar o agente (moderno)
    agent = create_openai_functions_agent(llm, TOOLS, prompt)
    
    # 4. Criar o Executor (moderno)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=TOOLS,
        verbose=settings.debug_mode,
        max_iterations=10,
        max_execution_time=60,
        handle_parsing_errors=True, # Importante para robustez
    )
    
    logger.info("✅ Agente (LCEL) criado com sucesso")
    return agent_executor


# ============================================
# Função de Memória
# ============================================

def get_session_history(session_id: str) -> PostgresChatMessageHistory:
    """
    Carrega o histórico de mensagens do Postgres.
    O session_id é o telefone do cliente.
    """
    return PostgresChatMessageHistory(
        connection_string=settings.postgres_connection_string,
        session_id=session_id,
        table_name=settings.postgres_table_name
    )


# ============================================
# Agente com Memória
# ============================================

# Criar agente global
_agent_executor = None
_agent_with_history = None


def get_agent_with_history():
    """
    Retorna o agente com histórico de mensagens (singleton)
    """
    global _agent_executor, _agent_with_history
    
    if _agent_with_history is None:
        _agent_executor = create_agent()
        
        # Esta parte já estava correta e pronta para LCEL
        _agent_with_history = RunnableWithMessageHistory(
            _agent_executor,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        logger.info("✅ Agente com histórico de mensagens configurado")
    
    return _agent_with_history


# ============================================
# Função Principal de Execução
# ============================================

def run_agent(telefone: str, mensagem: str) -> Dict[str, Any]:
    """
    Executa o agente com uma mensagem e um ID de sessão (telefone).
    
    O LLM decide e invoca ferramentas; não há fallback de pipeline.
    
    Args:
        telefone: Telefone do cliente (usado como session_id)
        mensagem: Mensagem do cliente
    
    Returns:
        Dict com 'output' (resposta do agente) e 'error' (se houver)
    """
    logger.info(f"Executando agente para telefone: {telefone}")
    logger.debug(f"Mensagem recebida: {mensagem}")

    # 1) Tentar primeiro o LLM com ferramentas e memória
    try:
        agent = get_agent_with_history()
        response = agent.invoke(
            {"input": mensagem},
            config={"configurable": {"session_id": telefone}},
        )
        output = response.get("output", "Desculpe, não consegui processar sua mensagem.")
        logger.info("✅ Agente executado com sucesso (LLM primeiro)")
        logger.debug(f"Resposta: {output}")
        return {"output": output, "error": None}
    except Exception as e:
        # Log detalhado do erro
        logger.error(f"Falha ao executar LLM: {e}", exc_info=True)
        error_msg = f"Erro ao executar o agente: {e}"
        return {
            "output": "Desculpe, não consegui processar sua mensagem agora.",
            "error": error_msg,
        }

    # 2) Pipeline proativo: Produto → EAN → Estoque/Preço
    # (Este pipeline de fallback não será executado se o try acima falhar)
    try:
        import re, json

        def _extrair_pares(texto: str) -> list[tuple[str, str]]:
            pares: list[tuple[str, str]] = []
            if not texto:
                return pares
            if "EANS_ENCONTRADOS:" in texto:
                for linha in texto.splitlines():
                    m = re.search(r"^\s*\d+\)\s*([0-9]{8,14})\s*-\s*(.+)$", linha)
                    if m:
                        pares.append((m.group(1).strip(), m.group(2).strip()))
            if not pares:
                eans = re.findall(r'"codigo_ean"\s*:\s*([0-9]{8,14})', texto)
                nomes = re.findall(r'"produto"\s*:\s*"([^"]+)"', texto)
                for e, n in zip(eans, nomes):
                    pares.append((e.strip(), n.strip()))
            return pares

        def _extrair_variacao(nome: str) -> str | None:
            m = re.search(r"\b(\d+[\.,]?\d*\s*(?:l|L|ml|g|kg))\b", nome)
            if m:
                return m.group(1).replace("L", "L").replace("l", "L").replace("ML", "ml")
            return None

        def _format_item(op: dict) -> str | None:
            nome = op.get("produto") or op.get("nome") or op.get("descricao")
            preco = op.get("preco")
            if not nome:
                return None
            if preco is not None:
                try:
                    valor = float(str(preco).replace(",", "."))
                    preco_fmt = f"R${valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                except Exception:
                    preco_fmt = f"R${preco}"
            else:
                preco_fmt = "preço indisponível"
            return f"{nome} — {preco_fmt}"

        # Tentativa de resolução automática via EAN
        ean_resp = ean_lookup(mensagem)
        pares = _extrair_pares(ean_resp)

        if pares:
            todas_opcoes: list[dict] = []
            for ean, nome in pares[:5]:
                try:
                    estoque_str = estoque_preco(ean)
                    itens = json.loads(estoque_str)
                    if isinstance(itens, list):
                        for it in itens:
                            todas_opcoes.append(it)
                except Exception:
                    continue

            # Filtra somente itens com nome e preço
            opcoes_formatadas = []
            for it in todas_opcoes:
                linha = _format_item(it)
                if linha:
                    opcoes_formatadas.append((linha, _extrair_variacao(linha or "")))

            # Se não achou opções válidas, cai para LLM
            if opcoes_formatadas:
                # Detectar se é genérico (múltiplas variações)
                variacoes = {v for _, v in opcoes_formatadas if v}
                texto_listagem = "\n".join([f"- {linha}" for linha, _ in opcoes_formatadas[:5]])
                if len(variacoes) >= 2:
                    pergunta = "Qual você prefere? Tenho " + ", ".join(sorted(variacoes)) + "."
                else:
                    pergunta = "Posso adicionar ao seu pedido?"

                resposta_natural = (
                    "Encontrei algumas opções disponíveis em estoque:\n"
                    f"{texto_listagem}\n"
                    f"{pergunta}"
                )
                logger.info("✅ Resposta gerada pelo pipeline proativo")
                return {"output": resposta_natural, "error": None}

        # Fallback: consulta por nome direto na API principal quando não houver EAN
        try:
            from urllib.parse import quote
            url = f"{settings.supermercado_base_url}/produtos/consulta?nome={quote(mensagem.strip())}"
            estoque_json = estoque(url)
            itens = json.loads(estoque_json)
            if isinstance(itens, list) and itens:
                # Reaproveitar heurísticas simples de preço/variação
                def _tem_estoque(d: dict) -> bool:
                    for k in ("estoque", "qtd", "qtde", "qtd_estoque", "quantidade", "quantidade_disponivel"):
                        if k in d:
                            try:
                                if float(str(d.get(k)).replace(',', '.')) > 0:
                                    return True
                            except Exception:
                                pass
                    # Alguns endpoints usam booleanos
                    for k in ("disponibilidade", "disponivel", "in_stock"):
                        v = d.get(k)
                        if isinstance(v, bool) and v:
                            return True
                        if isinstance(v, str) and v.strip().lower() in {"true", "sim", "yes"}:
                            return True
                    return False

                def _preco(d: dict) -> float | None:
                    for k in ("vl_produto", "vl_produto_normal", "preco", "preco_venda", "valor", "valor_unitario"):
                        if k in d:
                            try:
                                return float(str(d.get(k)).replace('.', '').replace(',', '.'))
                            except Exception:
                                pass
                    return None

                candidatos = []
                for it in itens:
                    if not isinstance(it, dict):
                        continue
                    if not _tem_estoque(it):
                        continue
                    nome = it.get("produto") or it.get("nome") or it.get("descricao")
                    preco = _preco(it)
                    if nome:
                        if preco is not None:
                            pf = f"R${preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                        else:
                            pf = "preço indisponível"
                        candidatos.append((f"{nome} — {pf}", _extrair_variacao(nome)))

                if candidatos:
                    variacoes = {v for _, v in candidatos if v}
                    texto_listagem = "\n".join([f"- {linha}" for linha, _ in candidatos[:5]])
                    if len(variacoes) >= 2:
                        pergunta = "Qual você prefere? Tenho " + ", ".join(sorted(variacoes)) + "."
                    else:
                        pergunta = "Posso adicionar ao seu pedido?"
                    resposta_natural = (
                        "Achei opções com estoque pelo nome informado:\n"
                        f"{texto_listagem}\n"
                        f"{pergunta}"
                    )
                    logger.info("✅ Resposta gerada pelo fallback de nome")
                    return {"output": resposta_natural, "error": None}
        except Exception as _e:
            logger.warning(f"Falha no fallback de nome: {_e}")

        # Caso específico: smart-responder não configurado → pedir clarificação
        if isinstance(ean_resp, str) and "SMART_RESPONDER_URL" in ean_resp:
            pergunta = (
                "Para confirmar direitinho: prefere Coca-Cola de 2L, 1L ou lata? "
                "Assim eu já te trago o preço certinho do que estiver disponível."
            )
            logger.info("✅ Retorno de clarificação por falta de smart-responder (pipeline)")
            return {"output": pergunta, "error": None}
    except Exception as e:
        logger.warning(f"Pipeline falhou: {e}")

    # 3) Último recurso
    error_msg = "Erro ao executar agente/pipeline"
    logger.error(error_msg)
    return {
        "output": "Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente.",
        "error": error_msg,
    }
