"""
Agente de IA para Atendimento de Supermercado
Utiliza LangChain para orquestração de ferramentas e memória de conversação
"""
from typing import Dict, Any
import os
import httpx  # Necessário para a correção do proxy
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_core.messages import AIMessageChunk
from langchain.agents import AgentExecutor, initialize_agent, AgentType
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
    """Consulta estoque e preço (Use URL completa)."""
    return estoque(url)

@tool
def pedidos_tool(json_body: str) -> str:
    """Envia pedido finalizado (JSON string)."""
    return pedidos(json_body)

@tool
def alterar_tool(telefone: str, json_body: str) -> str:
    """Atualiza pedido existente."""
    return alterar(telefone, json_body)

@tool
def set_tool(telefone: str, valor: str = "ativo", ttl: int = 600) -> str:
    """Marca pedido como ativo no Redis."""
    return set_pedido_ativo(telefone, valor, ttl)

@tool
def confirme_tool(telefone: str) -> str:
    """Verifica pedido ativo no Redis."""
    return confirme_pedido_ativo(telefone)

@tool
def time_tool() -> str:
    """Retorna data e hora atual."""
    return get_current_time()

@tool
def ean_tool(query: str) -> str:
    """Busca EAN/infos do produto via smart-responder."""
    return ean_lookup(query)

@tool("ean")
def ean_tool_alias(query: str) -> str:
    """Alias para ean_tool."""
    return ean_lookup(query)

@tool
def estoque_preco_tool(ean: str) -> str:
    """Consulta preço/disponibilidade por EAN (apenas dígitos)."""
    return estoque_preco(ean)

@tool("estoque")
def estoque_preco_alias(ean: str) -> str:
    """Alias para estoque_preco_tool."""
    return estoque_preco(ean)

TOOLS = [
    estoque_tool, pedidos_tool, alterar_tool, set_tool, confirme_tool,
    time_tool, ean_tool, ean_tool_alias, estoque_preco_tool, estoque_preco_alias
]

# ============================================
# Configuração do Agente
# ============================================

def _load_agent_prompt() -> str:
    default_prompt = (
        "Você é um atendente virtual de um supermercado. "
        "Base URL da API: {base_url}\nBase URL EAN: {ean_base}"
    )
    prompt_path = settings.agent_prompt_path
    if not prompt_path:
        base_dir = Path(__file__).resolve().parent
        prompt_path = str((base_dir / "prompts" / "agent_system.md"))

    try:
        return Path(prompt_path).read_text(encoding="utf-8")
    except Exception:
        return default_prompt

def create_agent() -> AgentExecutor:
    """Cria e retorna o AgentExecutor configurado com correção de Proxy."""
    
    # --- CORREÇÃO DE PROXY E VERSÃO ---
    logger.info("=== INICIANDO AGENTE: VERSÃO CORRIGIDA V3 ===")
    
    # 1. Limpar variáveis de ambiente que causam conflito
    for env_var in ["http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"]:
        if os.environ.pop(env_var, None):
            logger.info(f"Variável {env_var} removida do ambiente.")
            
    # 2. Criar cliente HTTP limpo (sem proxies)
    http_client = httpx.Client(proxies={})
    logger.info("Cliente HTTP (httpx) criado forçando sem proxies.")
    # ----------------------------------

    llm_kwargs = {
        "model": settings.llm_model,
        "openai_api_key": settings.openai_api_key,
        "http_client": http_client  # Injeta o cliente limpo
    }
    llm_kwargs["streaming"] = False
    
    if "gpt-5-mini" in str(settings.llm_model):
        llm_kwargs["temperature"] = 1.0
    else:
        llm_kwargs["temperature"] = settings.llm_temperature

    class NonStreamingChatOpenAI(ChatOpenAI):
        def stream(self, input, config=None, **kwargs):
            try:
                msg = self.invoke(input, config=config, **kwargs)
                yield AIMessageChunk(content=msg.content)
            except Exception as e:
                yield AIMessageChunk(content=f"Erro: {str(e)}")

    # Tentar instanciar LLM
    try:
        # Passa o http_client para o cliente OpenAI oficial também
        explicit_client = OpenAI(
            api_key=settings.openai_api_key,
            http_client=http_client
        )
        llm = NonStreamingChatOpenAI(**{**llm_kwargs, "client": explicit_client})
        logger.info("LLM criado com sucesso usando cliente explícito.")
    except Exception as e:
        logger.warning(f"Fallback LLM devido a erro: {e}")
        llm = NonStreamingChatOpenAI(**llm_kwargs)

    system_prompt_text = _load_agent_prompt()\
        .replace("{base_url}", settings.supermercado_base_url)\
        .replace("{ean_base}", settings.estoque_ean_base_url)\
        .replace("{", "{{").replace("}", "}}")

    agent_executor = initialize_agent(
        tools=TOOLS,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=settings.debug_mode,
        max_iterations=10,
        max_execution_time=60,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": {
                "type": "system",
                "content": system_prompt_text,
            }
        },
    )
    
    return agent_executor

# ============================================
# Memória e Execução
# ============================================

def get_session_history(session_id: str) -> PostgresChatMessageHistory:
    return PostgresChatMessageHistory(
        connection_string=settings.postgres_connection_string,
        session_id=session_id,
        table_name=settings.postgres_table_name
    )

_agent_with_history = None

def get_agent_with_history():
    global _agent_with_history
    if _agent_with_history is None:
        agent = create_agent()
        _agent_with_history = RunnableWithMessageHistory(
            agent,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
    return _agent_with_history

def run_agent(telefone: str, mensagem: str) -> Dict[str, Any]:
    logger.info(f"Executando agente V3 para: {telefone}")
    try:
        # (Lógica simplificada de pipeline proativo removida para focar na correção do erro principal)
        # Se precisar da lógica de EAN proativa de volta, basta descomentar ou manter a sua versão anterior,
        # mas certifique-se de manter a função create_agent corrigida acima.
        
        agent = get_agent_with_history()
        response = agent.invoke(
            {"input": mensagem},
            config={"configurable": {"session_id": telefone}},
        )
        return {"output": response.get("output", ""), "error": None}
    except Exception as e:
        logger.error(f"Erro fatal no agente: {e}", exc_info=True)
        return {"output": "Erro no sistema.", "error": str(e)}
