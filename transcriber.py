import whisper

def transcribe_audio(audio_path):
    model = whisper.load_model("base")

    result = model.transcribe(audio_path, fp16=False)
    return result["text"]
