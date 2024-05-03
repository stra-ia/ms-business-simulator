from pydantic import BaseModel
from typing import List
from fastapi import UploadFile
import enum

class SalesObject(BaseModel):
    id: int
    type: str
    isField: bool
    title: str
    description: str

class ChatMessage(BaseModel):
    role: str
    content: str
class SimulationType(enum.Enum):
    SALES = "sales"
    MARKETING = "marketing"

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]
    type: SimulationType

class VoiceRequest(BaseModel):
    file: UploadFile
    history: List[ChatMessage]
