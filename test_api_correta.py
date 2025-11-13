#!/usr/bin/env python3
"""
Testar a nova API do LangChain v1.0 com parâmetros corretos
"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool

# Testar ferramenta simples
@tool
def test_tool(query: str) -> str:
    """Ferramenta de teste"""
    return f"Resultado para: {query}"

# Criar LLM simples (vai falhar mas queremos ver a estrutura)
try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        openai_api_key="sk-test-key",  
        temperature=0
    )
    
    # Testar diferentes formas de chamar create_agent
    print("Testando create_agent com parâmetros posicionais...")
    
    try:
        agent = create_agent(llm, [test_tool])
        print("✅ create_agent(llm, tools) funcionou!")
    except Exception as e:
        print(f"❌ create_agent(llm, tools) falhou: {e}")
    
    try:
        agent = create_agent(llm, [test_tool], system_prompt="Você é um assistente")
        print("✅ create_agent(llm, tools, system_prompt) funcionou!")
    except Exception as e:
        print(f"❌ create_agent(llm, tools, system_prompt) falhou: {e}")
        
except Exception as e:
    print(f"❌ Erro ao criar LLM: {e}")