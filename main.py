import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    # subprocess.check_call([sys.executable,"gcloud", "config","set","project","784708256427"])
    from google.cloud import speech
except ImportError:
    install("google-cloud-speech")
    from google.cloud import speech


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.v1 import chatbot_router, voicechat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Especifica dominios específicos en lugar de '*' para producción
    allow_credentials=True,
    allow_methods=["*"],  # O puedes listar solo los métodos que necesitas: ['GET', 'POST']
    allow_headers=["*"],
)


app.include_router(chatbot_router.router, prefix="/chatbot", tags=["chatbot"])
app.include_router(voicechat_router.router, prefix="/voicechat", tags=["voicechat"])
