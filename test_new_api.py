#!/usr/bin/env python3
"""
Testar a nova API do LangChain v1.0 para criar agentes
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

# Testar ferramenta simples
@tool
def test_tool(query: str) -> str:
    """Ferramenta de teste"""
    return f"Resultado para: {query}"

# Criar LLM simples
llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key="sk-test-key",  # Vai falhar mas queremos ver a estrutura
    temperature=0
)

# Criar prompt
try:
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="Você é um assistente de teste"),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessage(content="{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    print("✅ Prompt criado com sucesso")
except Exception as e:
    print(f"❌ Erro ao criar prompt: {e}")

# Criar agente
try:
    agent = create_agent(
        llm,
        [test_tool],
        prompt,
        verbose=True
    )
    print("✅ Agente criado com sucesso")
    print(f"Tipo do agente: {type(agent)}")
except Exception as e:
    print(f"❌ Erro ao criar agente: {e}")
    print("Vamos tentar sem o prompt...")
    
    try:
        agent = create_agent(
            llm,
            [test_tool],
            verbose=True
        )
        print("✅ Agente criado sem prompt")
        print(f"Tipo do agente: {type(agent)}")
    except Exception as e2:
        print(f"❌ Erro ao criar agente sem prompt: {e2}")