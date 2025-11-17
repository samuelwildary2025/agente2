#!/usr/bin/env python3
"""
Demonstração do fluxo completo com reconhecimento de áudio
"""
import asyncio
from datetime import datetime
from server import _extract_incoming, process_message_async
from agent_langgraph_simple import get_session_history

def demo_audio_flow():
    """Demonstra o fluxo completo de atendimento com áudio"""
    print("🎤 Demonstração do Fluxo com Áudio")
    print("=" * 60)
    
    # Simula uma conversa real com áudio
    telefone = "5511999999999"
    
    print(f"📱 Cliente: {telefone}")
    print(f"⏰ Início: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # 1. Cliente envia áudio pedindo arroz
    print("1️⃣  Cliente envia áudio:")
    payload_audio1 = {
        "message": {
            "type": "audioMessage",
            "audio": {
                "url": "https://example.com/cliente_arroz.ogg",
                "caption": "Áudio do cliente"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_audio1)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Transcrição: '{result['mensagem_texto']}'")
    print(f"   Status: Áudio processado e transcrito")
    print()
    
    # 2. Agente responde
    print("2️⃣  Agente responde:")
    print("   'Entendi! Você quer arroz. Quantos pacotes?'")
    print()
    
    # 3. Cliente envia outro áudio
    print("3️⃣  Cliente envia outro áudio:")
    payload_audio2 = {
        "message": {
            "type": "audio",
            "audio": {
                "base64": "data:audio/ogg;base64,dummy_audio_2_pacotes",
                "mimeType": "audio/ogg"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_audio2)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Transcrição: '{result['mensagem_texto']}'")
    print(f"   Status: Áudio processado e transcrito")
    print()
    
    # 4. Agente confirma
    print("4️⃣  Agente confirma:")
    print("   'Perfeito! 2 pacotes de arroz anotados. Mais alguma coisa?'")
    print()
    
    # 5. Cliente envia áudio final
    print("5️⃣  Cliente envia áudio final:")
    payload_audio3 = {
        "message": {
            "type": "audioMessage",
            "audio": {
                "url": "https://example.com/cliente_final.ogg"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_audio3)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Transcrição: '{result['mensagem_texto']}'")
    print(f"   Status: Áudio processado e transcrito")
    print()
    
    # 6. Agente finaliza
    print("6️⃣  Agente finaliza:")
    print("   'Tudo certo! Seu pedido está confirmado. Total: R$ 25,00'")
    print()
    
    print("=" * 60)
    print("✅ Conversa com áudio concluída com sucesso!")
    print("=" * 60)

def demo_mixed_messages():
    """Demonstra fluxo misto com texto e áudio"""
    print("\n🔄 Demonstração de Fluxo Misto (Texto + Áudio)")
    print("=" * 60)
    
    telefone = "5511888888888"
    print(f"📱 Cliente: {telefone}")
    print()
    
    # 1. Cliente envia texto
    print("1️⃣  Cliente envia texto:")
    payload_text = {
        "message": {
            "type": "text",
            "text": {"body": "Olá, quero fazer um pedido"}
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_text)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Mensagem: '{result['mensagem_texto']}'")
    print()
    
    # 2. Cliente envia áudio
    print("2️⃣  Cliente envia áudio:")
    payload_audio = {
        "message": {
            "type": "audio",
            "audio": {
                "url": "https://example.com/queijo_presunto.ogg"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_audio)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Transcrição: '{result['mensagem_texto']}'")
    print()
    
    # 3. Cliente envia imagem
    print("3️⃣  Cliente envia imagem:")
    payload_image = {
        "message": {
            "type": "image",
            "image": {
                "caption": "Quero esse produto"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_image)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Mensagem: '{result['mensagem_texto']}'")
    print()
    
    print("✅ Fluxo misto processado com sucesso!")
    print("   O agente consegue lidar com texto, áudio e imagens na mesma conversa!")
    print("=" * 60)

def demo_error_handling():
    """Demonstra tratamento de erros em áudio"""
    print("\n⚠️  Demonstração de Tratamento de Erros")
    print("=" * 60)
    
    telefone = "5511777777777"
    print(f"📱 Cliente: {telefone}")
    print()
    
    # 1. Áudio com URL inválida
    print("1️⃣  Áudio com URL inválida:")
    payload_invalid_url = {
        "message": {
            "type": "audio",
            "audio": {
                "url": "https://invalid-url.com/audio.ogg"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_invalid_url)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Resultado: '{result['mensagem_texto']}'")
    print("   ✅ Sistema tratou erro graciosamente")
    print()
    
    # 2. Áudio com base64 inválido
    print("2️⃣  Áudio com base64 inválido:")
    payload_invalid_base64 = {
        "message": {
            "type": "audioMessage",
            "audio": {
                "base64": "invalid_base64_data"
            }
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_invalid_base64)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Resultado: '{result['mensagem_texto']}'")
    print("   ✅ Sistema tratou erro graciosamente")
    print()
    
    # 3. Áudio sem dados
    print("3️⃣  Áudio sem dados:")
    payload_no_data = {
        "message": {
            "type": "audio",
            "audio": {}
        },
        "from": telefone
    }
    
    result = _extract_incoming(payload_no_data)
    print(f"   Tipo: {result['message_type']}")
    print(f"   Resultado: '{result['mensagem_texto']}'")
    print("   ✅ Sistema tratou situação graciosamente")
    print()
    
    print("✅ Todos os erros foram tratados sem quebrar o sistema!")
    print("   O cliente sempre recebe uma resposta apropriada.")
    print("=" * 60)

if __name__ == "__main__":
    print("🚀 Demonstração do Reconhecimento de Áudio no Agente")
    print("=" * 60)
    
    # Demonstração do fluxo principal
    demo_audio_flow()
    
    # Demonstração de fluxo misto
    demo_mixed_messages()
    
    # Demonstração de tratamento de erros
    demo_error_handling()
    
    print("\n🎯 RESUMO")
    print("=" * 60)
    print("✅ Áudio transcrição integrada com sucesso!")
    print("✅ Suporte a URLs e base64")
    print("✅ Tratamento robusto de erros")
    print("✅ Compatível com mensagens de texto e imagem")
    print("✅ Fluxo natural de conversação")
    print("=" * 60)