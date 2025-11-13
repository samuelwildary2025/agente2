#!/usr/bin/env python3
"""
Teste direto da API Smart Responder
"""

import os
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_smart_responder():
    """Testa a API Smart Responder diretamente"""
    
    url = os.getenv("SMART_RESPONDER_URL")
    token = os.getenv("SMART_RESPONDER_TOKEN")
    
    print(f"🌐 URL: {url}")
    print(f"🔑 Token: {token[:20]}...")
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "query": "coca cola 2L"
    }
    
    print(f"📤 Enviando payload: {payload}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
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
    print("🧪 Testando Smart Responder API...")
    print("=" * 50)
    test_smart_responder()