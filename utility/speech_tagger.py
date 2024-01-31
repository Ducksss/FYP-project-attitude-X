import whisper_timestamped as whisper
import math
import streamlit as st

# f = st.file_uploader("Upload file")
# tfile = tempfile.NamedTemporaryFile(delete=False)
# tfile.write(f.read())
model = whisper.load_model("base")


def transcribeFile(file):
    audio = whisper.load_audio(file)
    result = whisper.transcribe(model, audio, language="en",vad="auditok")
    transcript = ''
    for i, segment in enumerate(result['segments']):
        start, end = segment['start'], segment['end']
        transcript += f'{segment["text"].strip()} ({math.floor(start)} -> {math.floor(end)} seconds)\n'
    return transcript