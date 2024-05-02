from pydantic import BaseModel
from typing import List
from fastapi import UploadFile

class SalesObject(BaseModel):
    id: int
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