# llm_meeting_summarizer
Built an end-to-end LLM-powered meeting intelligence system using Whisper, LLaMA-2, FAISS, and Streamlit to transcribe audio, generate structured summaries, extract action items, and enable semantic Q&amp;A.

# LLM-Powered Meeting Summarizer 
A full-stack AI-powered meeting intelligence system that transcribes meetings, summarizes discussions, extracts action items, and enables intelligent Q&A using RAG (Retrieval-Augmented Generation) — all running locally and free using LLaMA 2 + FAISS.

✨ Features

- Upload meeting audio (MP3 / WAV / M4A)

- Automatic transcription using Whisper

- Structured meeting summary

- Action item extraction (Owner, Task, Deadline)

- Ask questions using RAG

- Semantic search using FAISS

- LLaMA 2 inference via Ollama (no OpenAI cost)

- PDF report generation

- Streamlit interactive UI

- Works completely offline

## 📍 Local Deployment

### 🧠 Architecture
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

LLaMA 2 (Ollama)

↓

Summary + Action Items + Q&A

🧠 Tech Stack

🔹 Core Technologies

Python

LLaMA 2 (via Ollama)

Sentence Transformers

FAISS (Vector Database)

OpenAI Whisper (Speech-to-Text)

Streamlit

🔹 AI / ML

Retrieval-Augmented Generation (RAG)

Semantic search

Embeddings-based similarity search

Prompt engineering

🔹 Others

PDF generation (ReportLab)

Caching for deterministic outputs



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

---
title: llm-meeting-summarizer
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.32.0"
python_version: "3.10"
app_file: app.py
pinned: false
---