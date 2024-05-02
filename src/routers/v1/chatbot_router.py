from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from src.services import chatbot_services
from vertexai.generative_models import GenerativeModel, ChatSession
from typing import List
from src.services import voicechat_services
import json
from src.services import voicechat_services
import base64
from src.schemas.chatbot_schemas import ChatRequest
from src.utils.chatbot_utils import markdown_to_text

router = APIRouter()

@router.post("/message")
async def send_message(request: ChatRequest):
    try:
        return chatbot_services.chat(request, stream=False)
    except Exception as e:
        print("Error: ", str(e))
        raise HTTPException(status_code=500, detail=str(e))

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
