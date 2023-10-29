import base64
import tempfile
from io import BytesIO

import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment


def base64_to_binary(base64_audio: str) -> BytesIO:
    return base64.b64decode(base64_audio)


def convert_webm_to_wav(input_file, output_file):
    # Load the WebM audio file
    audio = AudioSegment.from_file(input_file, format="webm")

    # Convert the audio to WAV format
    audio.export(output_file, format="wav")


def speech_to_text(audio_data_in_base64: str) -> str:
    binary_data = base64_to_binary(audio_data_in_base64)
    print(binary_data)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_filename = temp_wav.name

    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_webm:
        temp_webm_filename = temp_webm.name

    with open(temp_webm_filename, "wb") as audio_file:
        audio_file.write(binary_data)

    convert_webm_to_wav(temp_webm_filename, temp_wav_filename)

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
