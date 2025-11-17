#!/usr/bin/env python3
"""
Teste de integração do reconhecimento de áudio
"""
import asyncio
import os
from tools.audio_tools import transcrever_audio_url, transcrever_audio_base64
from server import _extract_incoming

def test_audio_transcription():
    """Testa a transcrição de áudio com dados simulados"""
    print("🎧 Testando reconhecimento de áudio...")
    
    # Teste 1: Simulação de mensagem de áudio com URL
    print("\n1. Testando mensagem de áudio com URL:")
    payload_url = {
        "message": {
            "type": "audio",
            "audio": {
                "url": "https://example.com/audio.mp3",
                "caption": "Teste de áudio"
            }
        },
        "from": "5511999999999"
    }
    
    result = _extract_incoming(payload_url)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Mensagem: {result['mensagem_texto']}")
    
    # Teste 2: Simulação de mensagem de áudio com base64
    print("\n2. Testando mensagem de áudio com base64:")
    payload_base64 = {
        "message": {
            "type": "audioMessage",
            "audio": {
                "base64": "data:audio/ogg;base64,dummy_audio_data",
                "mimeType": "audio/ogg"
            }
        },
        "from": "5511888888888"
    }
    
    result = _extract_incoming(payload_base64)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Mensagem: {result['mensagem_texto']}")
    
    # Teste 3: Simulação de mensagem de áudio sem dados
    print("\n3. Testando mensagem de áudio sem dados:")
    payload_no_data = {
        "message": {
            "type": "audio",
            "audio": {}
        },
        "from": "5511777777777"
    }
    
    result = _extract_incoming(payload_no_data)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Mensagem: {result['mensagem_texto']}")
    
    # Teste 4: Mensagem de texto normal (não deve ser afetada)
    print("\n4. Testando mensagem de texto normal:")
    payload_text = {
        "message": {
            "type": "text",
            "text": {"body": "Olá, quero comprar arroz"}
        },
        "from": "5511666666666"
    }
    
    result = _extract_incoming(payload_text)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Mensagem: {result['mensagem_texto']}")

def test_direct_audio_tools():
    """Testa as ferramentas de áudio diretamente"""
    print("\n🔧 Testando ferramentas de áudio diretamente...")
    
    # Teste com URL inválida (deve falhar graciosamente)
    print("\n1. Testando transcrição com URL inválida:")
    try:
        result = transcrever_audio_url("https://invalid-url.com/audio.mp3")
        print(f"   Resultado: {result}")
    except Exception as e:
        print(f"   Erro esperado: {e}")
    
    # Teste com base64 inválido (deve falhar graciosamente)
    print("\n2. Testando transcrição com base64 inválido:")
    try:
        result = transcrever_audio_base64("invalid_base64_data")
        print(f"   Resultado: {result}")
    except Exception as e:
        print(f"   Erro esperado: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Iniciando testes de reconhecimento de áudio")
    print("=" * 60)
    
    # Testar integração com o servidor
    test_audio_transcription()
    
    # Testar ferramentas diretamente
    test_direct_audio_tools()
    
    print("\n" + "=" * 60)
    print("✅ Testes de reconhecimento de áudio concluídos")
    print("=" * 60)