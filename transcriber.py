import streamlit as st
from groq import Groq
import os

def get_groq_client():
    try:
        return Groq(api_key=st.secrets["GROQ"]["API_KEY"])   # Streamlit Cloud
    except Exception:
        return Groq(api_key=os.getenv("GROQ_API_KEY"))       # Local dev

def transcribe_audio(audio_path):
    client = get_groq_client()   # <-- FIX: create client inside function
    print("transcriber.py client created at import:", "client" in globals())

    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3"
        )

    return transcription.text
