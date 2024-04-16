from fastapi import FastAPI
from src.routers.v1 import chatbot_router

app = FastAPI()

app.include_router(chatbot_router.router, prefix="/chatbot", tags=["chatbot"])
