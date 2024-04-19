from fastapi import APIRouter, HTTPException, File, UploadFile
from src.services import voicechat_services
from pydantic import BaseModel

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/message")
# async def transcribe_audio(file: UploadFile = File(...)):
async def transcribe_audio(file: UploadFile = File(...)):
    audio_content = await file.read()
    return voicechat_services.transcribe_audio(audio_content)


@router.post("/synthesize")
async def text_to_speech(request: TextRequest):
    return voicechat_services.text_to_speech(request.text)