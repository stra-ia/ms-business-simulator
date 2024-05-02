import subprocess
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.v1 import chatbot_router, voicechat_router, prediction_router, feedback_router



def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    from google.cloud import speech
except ImportError:
    install("google-cloud-speech")
    from google.cloud import speech

try:
    from google.cloud import texttospeech
except ImportError:
    install("google-cloud-texttospeech")
    from google.cloud import texttospeech

try:
    import vertexai
except ImportError:
    install("google-cloud-aiplatform")
    import vertexai

try:
    import multipart
except ImportError:
    install("python-multipart")
    import multipart

try:
    import markdown
except ImportError:
    install("markdown")
    import markdown
try:
    from bs4 import BeautifulSoup
except ImportError:
    install("beautifulsoup4")
    from google.cloud import speech


import vertexai


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Especifica dominios específicos en lugar de '*' para producción
    allow_credentials=True,
    allow_methods=["*"],  # O puedes listar solo los métodos que necesitas: ['GET', 'POST']
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    vertexai.init(project="proyectos-internos-lapzo", location="us-central1")

app.include_router(chatbot_router.router, prefix="/chatbot", tags=["chatbot"])
app.include_router(voicechat_router.router, prefix="/voicechat", tags=["voicechat"])
app.include_router(prediction_router.router, prefix="/prediction", tags=["prediction"])
app.include_router(feedback_router.router, prefix="/feedback", tags=["feedback_router"])
