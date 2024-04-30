from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from src.services import chatbot_services
from vertexai.generative_models import GenerativeModel, ChatSession
from pydantic import BaseModel
from typing import List
from src.services import voicechat_services
import json
from src.services import voicechat_services
import base64
import markdown
from bs4 import BeautifulSoup


router = APIRouter()

class SalesObject(BaseModel):
    type: str
    isField: bool
    title: str
    description: str

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
    try:
        # print(message)
        return chatbot_services.chat(request, stream=False)
    except Exception as e:
        # return {"error": str(e)}
        print("Error: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    # chat_response_generator = chatbot_services.chat(request, stream=True)

    # print(chat_response_generator)

    # Función generadora que adapta las respuestas del chat para streaming
    # def generate_responses(chat_response_generator):
    #     try:
    #         for response in chat_response_generator:
    #             # Suponemos que 'response' tiene un atributo 'candidates' que contiene los datos necesarios
    #             if response.candidates and response.candidates[0].content:
    #                 # Extraemos el texto de la primera parte del contenido del primer candidato
    #                 text = response.candidates[0].content.parts[0].text
    #                 yield json.dumps({"message": text}) + "\n"
    #             else:
    #                 yield json.dumps({"message": "No response"}) + "\n"
    #     except Exception as e:
    #         yield json.dumps({"error": str(e)}) + "\n"

    # # StreamingResponse maneja el envío de los datos generados continuamente
    # return StreamingResponse(generate_responses(chat_response_generator), media_type="application/json")

@router.post("/voice")
async def send_message_voice(file: UploadFile = File(...), history: str = Form(...)):
    try: 
        # print(message)
        # Transcribe the audio message
        audio_content = await file.read()
        voice_message = voicechat_services.transcribe_audio(audio_content)

        # Send the message to the chatbot
        history_obj = json.loads(history)
        request: ChatRequest = ChatRequest(message=voice_message['transcription'], history=history_obj)

        chatbot = chatbot_services.chat(request)['message']

        # Convert the message to voice
        message_to_voice = markdown_to_text(chatbot.message)
        voice = voicechat_services.text_to_speech(message_to_voice)
        # Codifica el audio en base64
        audio_base64 = base64.b64encode(voice).decode('utf-8')

        return {
            "message": chatbot.message,
            "clientBrief": chatbot.clientBrief,
            "voice_message": voice_message['transcription'],
            "voice": audio_base64
        }
        # raise Exception("This is a new error.")
    except Exception as e:
        return {"error": str(e)}
