import base64
import tempfile
from io import BytesIO

import speech_recognition as sr
from googletrans import Translator


def base64_to_binary(base64_audio: str) -> BytesIO:
    binary_audio_data: bytes = base64.b64decode(base64_audio)
    audio_file_object: BytesIO = BytesIO(binary_audio_data)

    return audio_file_object


def speech_to_text(audio_data_in_base64: str) -> str:
    binary_data = base64_to_binary(audio_data_in_base64).getvalue()

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_filename = temp_wav.name

    with open(temp_wav_filename, "wb") as audio_file:
        audio_file.write(binary_data)

    recognizer = sr.Recognizer()

    with open(temp_wav_filename, "rb") as audio_file:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            audio_text = recognizer.recognize_google(audio)

    return audio_text


def translateMessage(message: str, to="en"):
    tr = Translator()
    convert = tr.translate(message, src="auto", dest=to)
    return convert.text, convert.src
