from fastapi import APIRouter, HTTPException, Form, File, UploadFile
from src.services import chatbot_services
from vertexai.generative_models import GenerativeModel, ChatSession
from pydantic import BaseModel
from typing import List, Dict
from src.services import voicechat_services
import json
from src.services import voicechat_services
import base64
import markdown
from bs4 import BeautifulSoup


router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]

class VoiceRequest(BaseModel):
    file: UploadFile
    history: List[ChatMessage]

# transcribe_audio(file: UploadFile = File(...)):
#     audio_content = await file.read()

def markdown_to_text(markdown_text):
    # Convertir Markdown a HTML
    html = markdown.markdown(markdown_text)
    
    # Parsear HTML para obtener texto plano
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    
    # Opcionalmente, puedes eliminar espacios adicionales
    text = ' '.join(text.split())
    
    return text

@router.post("/message")
async def send_message(request: ChatRequest):
    # print(message)
    return chatbot_services.chat(request)

@router.post("/voice")
async def send_message_voice(file: UploadFile = File(...), history: str = Form(...)):
    # print(message)
    # Transcribe the audio message
    audio_content = await file.read()
    voice_message = voicechat_services.transcribe_audio(audio_content)

    # Send the message to the chatbot
    history_obj = json.loads(history)
    request: ChatRequest = ChatRequest(message=voice_message['transcription'], history=history_obj)

    message = chatbot_services.chat(request)['message']

    # Convert the message to voice
    message_to_voice = markdown_to_text(message)
    voice = voicechat_services.text_to_speech(message_to_voice)
    # Codifica el audio en base64
    audio_base64 = base64.b64encode(voice).decode('utf-8')

    return {
        "message": message,
        "voice_message": voice_message['transcription'],
        "voice": audio_base64
    }
    # raise Exception("This is a new error.")
