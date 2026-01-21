import streamlit as st
from groq import Groq
import os

try:
    client = Groq(api_key=st.secrets["GROQ"]["API_KEY"]) # Streamlit Cloud
except Exception:
    client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Local .env

def transcribe_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3"
        )

    return transcription.text
