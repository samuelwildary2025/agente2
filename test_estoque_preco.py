#!/usr/bin/env python3
"""
Teste direto da API de estoque/preço
"""

import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_estoque_preco():
    """Testa a API de estoque/preço diretamente"""
    
    base_url = os.getenv("ESTOQUE_EAN_BASE_URL")
    ean = "7894900011516"  # Coca-Cola 2L
    
    url = f"{base_url}?ean={ean}"
    
    print(f"🌐 URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📨 Response: {response.text[:500]}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso: {data}")
            return True
        else:
            print(f"❌ Erro: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testando API de Estoque/Preço...")
    print("=" * 50)
    test_estoque_preco()