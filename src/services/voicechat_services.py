# Import the Speech-to-Text client library
from google.cloud import speech, texttospeech
from google.cloud import texttospeech_v1beta1
from google.oauth2 import service_account
import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
from fastapi.responses import StreamingResponse
import io

def transcribe_audio(audio_content):
    # return transcribe_audio_speech(audio_content)
    return transcribe_audio_gemini(audio_content)


def transcribe_audio_speech(audio_content):

    credentials = service_account.Credentials.from_service_account_file(f'{os.getcwd()}/google-config.json')

    config = speech.RecognitionConfig(
        language_code="en",
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

def transcribe_audio_gemini(audio_uri):
    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    # audio_part = Part(mime_type="audio/mpeg", uri=audio_uri)
    audio_part = Part.from_data(data=audio_uri, mime_type="audio/mpeg")
   
    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0.5,
        "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    responses = model.generate_content(
        [audio_part, "Generate transcription from the audio in spanish, only extract speech, only want the transcript and ignore background audio"],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=False,
    )

    for response in responses.candidates[0].content.parts:
        print(response.text, end="")
        return {"transcription": response.text}

def text_to_speech(text: str):
    return text_to_speech_bad(text)
    # return synthesize_text(text)

def synthesize_text(text:str):
    credentials = service_account.Credentials.from_service_account_file(f'{os.getcwd()}/google-config.json')
    client = texttospeech_v1beta1.TextToSpeechClient(credentials=credentials)

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech_v1beta1.VoiceSelectionParams(
        language_code='es-EN',
        ssml_gender=texttospeech_v1beta1.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech_v1beta1.AudioConfig(
        audio_encoding=texttospeech_v1beta1.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": input_text,
            "voice": voice,
            "audio_config": audio_config
        }
    )

    # El audio es en formato binario.
    return StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/mpeg")


def text_to_speech_bad(text: str):
    credentials = service_account.Credentials.from_service_account_file(f'{os.getcwd()}/google-config.json')
    client = texttospeech.TextToSpeechClient(credentials=credentials)

    synthesis_input = texttospeech.SynthesisInput(text=text)
    # ssml = "<speak><p><s>This is sentence one.</s><s>This is sentence two.</s></p></speak>"
    # synthesis_input = texttospeech.SynthesisInput(ssml=ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        # ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        name= "en-US-Studio-O"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        effects_profile_id=["medium-bluetooth-speaker-class-device"],
    )

    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    # return StreamingResponse(io.BytesIO(response.audio_content), media_type="audio/mpeg")
    return response.audio_content

# # Llama a la función con tu texto
# text_to_speech("Hello, this is a test of Google Cloud Text-to-Speech in Python.")
