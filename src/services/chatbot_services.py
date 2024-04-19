from vertexai.generative_models import GenerativeModel, ChatSession, Content, Part
from pydantic import BaseModel
from typing import List, Dict

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]

def convert_history(history):
    content_list = []
    for message in history:
        part = Part.from_text(text = message.content)
        content = Content(parts=[part], role=message.role)
        content_list.append(content)
    return content_list


def chat(request: ChatRequest):

    history = convert_history(request.history)

    prompt = f"The response will be short and concise. {request.message}"

    model = GenerativeModel("gemini-1.0-pro", generation_config={"max_output_tokens": 100})
    chat = model.start_chat(history=history, response_validation=False)
    responses = chat.send_message(prompt, stream=False)

    messages = {"message": responses.candidates[0].content.parts[0].text}
    # messages = {"message": "esta es una prueba"}
    return messages
    # return {
    #     "message": "Transcription failed",
    # }