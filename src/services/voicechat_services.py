# Import the Speech-to-Text client library
from google.cloud import speech
from google.oauth2 import service_account
import os



def transcribe_audio(audio_content):

    credentials = service_account.Credentials.from_service_account_file(f'{os.getcwd()}/google-config.json')

    config = speech.RecognitionConfig(
        language_code="es",
    )

    audio = speech.RecognitionAudio(
        content=audio_content,
    )

    client = speech.SpeechClient(credentials=credentials)

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))
        return {
            "transcription": result.alternatives[0].transcript,
        }

    # return {
    #     "message": "Transcription failed",
    # }