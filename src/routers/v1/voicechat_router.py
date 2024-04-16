from fastapi import APIRouter, HTTPException, File, UploadFile
from src.services import voicechat_services

router = APIRouter()

@router.post("/message")
# async def transcribe_audio(file: UploadFile = File(...)):
async def transcribe_audio(file: UploadFile = File(...)):
    audio_content = await file.read()
    return voicechat_services.transcribe_audio(audio_content)