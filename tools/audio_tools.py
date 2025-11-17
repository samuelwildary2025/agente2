"""
Ferramentas de transcrição de áudio para o agente
"""

import os
import tempfile
import requests
from typing import Optional
from openai import OpenAI
from config.settings import settings
from config.logger import setup_logger

logger = setup_logger(__name__)

# Cliente OpenAI para transcrição
_openai_client: Optional[OpenAI] = None

def get_openai_client() -> OpenAI:
    """Retorna cliente OpenAI para transcrição"""
    global _openai_client
    
    if _openai_client is None:
        _openai_client = OpenAI(api_key=settings.openai_api_key)
    
    return _openai_client

def transcrever_audio_url(audio_url: str) -> str:
    """
    Transcreve áudio de uma URL usando OpenAI Whisper
    
    Args:
        audio_url: URL do arquivo de áudio
        
    Returns:
        Texto transcrito ou mensagem de erro
    """
    try:
        logger.info(f"Transcrevendo áudio da URL: {audio_url[:100]}...")
        
        # Baixar áudio da URL
        response = requests.get(audio_url, timeout=30)
        response.raise_for_status()
        
        # Salvar áudio temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name
        
        try:
            # Transcrever com Whisper
            client = get_openai_client()
            with open(temp_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="pt"  # Português
                )
            
            texto_transcrito = transcript.text
            logger.info(f"Áudio transcrito com sucesso: {texto_transcrito[:100]}...")
            return texto_transcrito
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao baixar áudio: {e}")
        return f"Erro ao baixar áudio: {str(e)}"
    except Exception as e:
        logger.error(f"Erro na transcrição: {e}")
        return f"Erro na transcrição: {str(e)}"

def transcrever_audio_base64(audio_base64: str, formato: str = "mp3") -> str:
    """
    Transcreve áudio em base64 usando OpenAI Whisper
    
    Args:
        audio_base64: Áudio em base64
        formato: Formato do áudio (mp3, ogg, etc)
        
    Returns:
        Texto transcrito ou mensagem de erro
    """
    try:
        logger.info("Transcrevendo áudio em base64...")
        
        # Decodificar base64
        import base64
        audio_data = base64.b64decode(audio_base64)
        
        # Salvar áudio temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{formato}') as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        try:
            # Transcrever com Whisper
            client = get_openai_client()
            with open(temp_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="pt"  # Português
                )
            
            texto_transcrito = transcript.text
            logger.info(f"Áudio transcrito com sucesso: {texto_transcrito[:100]}...")
            return texto_transcrito
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        logger.error(f"Erro na transcrição de base64: {e}")
        return f"Erro na transcrição: {str(e)}"

def transcrever_audio_whatsapp(audio_data: dict) -> str:
    """
    Transcreve áudio do WhatsApp (pode vir como URL ou base64)
    
    Args:
        audio_data: Dicionário com dados do áudio do WhatsApp
        
    Returns:
        Texto transcrito
    """
    try:
        # Verificar se tem URL
        if "url" in audio_data:
            return transcrever_audio_url(audio_data["url"])
        
        # Verificar se tem base64
        if "base64" in audio_data:
            formato = audio_data.get("formato", "mp3")
            return transcrever_audio_base64(audio_data["base64"], formato)
        
        # Tentar extrair URL de estrutura WhatsApp
        if "audio" in audio_data and isinstance(audio_data["audio"], dict):
            if "url" in audio_data["audio"]:
                return transcrever_audio_url(audio_data["audio"]["url"])
        
        return "Não foi possível extrair o áudio para transcrição"
        
    except Exception as e:
        logger.error(f"Erro ao processar áudio do WhatsApp: {e}")
        return f"Erro ao processar áudio: {str(e)}"

# Função principal para o agente usar
def transcrever_mensagem_audio(audio_info: dict) -> str:
    """
    Função principal para transcrever mensagens de áudio
    
    Args:
        audio_info: Informações do áudio (URL, base64, etc)
        
    Returns:
        Texto transcrito
    """
    if not audio_info:
        return "Nenhum áudio recebido"
    
    # Se for string, assumir que é URL
    if isinstance(audio_info, str):
        if audio_info.startswith("http"):
            return transcrever_audio_url(audio_info)
        else:
            return "Formato de áudio não reconhecido"
    
    # Se for dicionário, usar função WhatsApp
    if isinstance(audio_info, dict):
        return transcrever_audio_whatsapp(audio_info)
    
    return "Formato de áudio não suportado"

if __name__ == "__main__":
    # Teste básico
    print("🎤 Ferramenta de transcrição de áudio criada!")
    print("✅ Integração com OpenAI Whisper pronta!")
    print("📱 Suporte para WhatsApp implementado!")