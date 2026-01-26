Built an end-to-end LLM-powered meeting intelligence system using Whisper, LLaMA-3, FAISS, and Streamlit to transcribe audio, generate structured summaries, extract action items, and enable semantic Q&amp;A.

# LLM-Powered Meeting Summarizer 
A full-stack AI-powered meeting intelligence system that transcribes meetings, summarizes discussions, extracts action items, and enables intelligent Q&A using RAG (Retrieval-Augmented Generation) — all running locally and free using LLaMA 3 + FAISS.

✨ Features

- Upload meeting audio (MP3 / WAV / M4A)
- Automatic transcription using Whisper
- Structured meeting summary
- Action item extraction (Owner, Task, Deadline)
- Ask questions using RAG
- Semantic search using FAISS
- LLaMA 3 (no OpenAI cost)
- PDF report generation
- Streamlit interactive UI

### Architecture
Audio File
↓
Whisper Transcription
↓
Text Chunking
↓
Embeddings (SentenceTransformers)
↓
FAISS Vector Store
↓
LLaMA 3
↓
Summary + Action Items + Q&A

### 🔹 Programming Language
![Python](https://img.shields.io/badge/Python-FF6F61?style=for-the-badge)
### 🔹 Models & Libraries
![LLaMa3](https://img.shields.io/badge/LLaMa3-FF6F61?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-0F52BA?style=for-the-badge)
![OpenAI Whisper (Speech-to-Text)](https://img.shields.io/badge/Whisper-8A2BE2?style=for-the-badge)
![Sentence-Transformers](https://img.shields.io/badge/Sentence-Transformers-FF4500?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-0078D7?style=for-the-badge)
### 🛠️ Libraries & Utilities
![PyDub](https://img.shields.io/badge/PyDub-FF6347?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge)
![ReportLab](https://img.shields.io/badge/ReportLab-2E8B57?style=for-the-badge)
![FPDF](https://img.shields.io/badge/FPDF-4682B4?style=for-the-badge)

🔹 AI / ML : Retrieval-Augmented Generation (RAG), Semantic search, Embeddings-based similarity search, Prompt engineering

🔹 Others : PDF generation (ReportLab), Caching for deterministic outputs

## 📂 Project Structure

```text
llm-meeting-summarizer/
│
├── app.py              # Streamlit UI
├── summarizer.py       # LLM summarization logic
├── rag_llama.py        # RAG + FAISS logic
├── transcriber.py      # Whisper transcription
├── utils.py            # PDF generation
├── cache_utils.py      # Summary caching
├── requirements.txt
├── README.md
└── .gitignore
```

## Demo
<p>
<img width="1877" height="978" alt="LLM_1" src="https://github.com/user-attachments/assets/8f49a9e5-c0f5-4a95-9c99-b16f076f2063" />
<img width="1857" height="932" alt="LLM_2" src="https://github.com/user-attachments/assets/aa8e31cf-f599-4f21-ad23-932a92f462f7" />
</p>
