# rag_llama.py

import os
import faiss
import numpy as np
import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer

# ---- Embedding model ----
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---- In-memory vector store ----
documents = []
index = None


def get_groq_client():
    """Create Groq client safely for Streamlit + local."""
    try:
        return Groq(api_key=st.secrets["GROQ"]["API_KEY"])
    except Exception:
        return Groq(api_key=os.getenv("GROQ_API_KEY"))


# ---------- Chunking ----------
def chunk_text(text, max_chars=400):
    """Split transcript into semantic-ish chunks."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks, current = [], ""

    for sent in sentences:
        if not sent:
            continue
        if len(current) + len(sent) + 1 <= max_chars:
            current = (current + " " + sent).strip()
        else:
            chunks.append(current)
            current = sent
    if current:
        chunks.append(current)

    return chunks


# ---------- Build Vector DB ----------
def build_vector_db(transcript):
    """Build FAISS index from transcript."""
    global index, documents

    documents = chunk_text(transcript)
    if not documents:
        index = None
        return

    embeddings = embedder.encode(documents).astype("float32")
    faiss.normalize_L2(embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)


# ---------- Query RAG ----------
def query_rag(question, top_k=5, threshold=0.20):
    """Answer questions grounded in the transcript."""
    global index, documents

    if index is None or not documents:
        return "I don't have any meeting context loaded yet."

    client = get_groq_client()

    # 1. Embed question
    q_emb = embedder.encode([question]).astype("float32")
    faiss.normalize_L2(q_emb)

    # 2. Retrieve top-k chunks
    scores, indices = index.search(q_emb, k=top_k)

    # 3. Filter by similarity threshold
    pairs = [(i, s) for i, s in zip(indices[0], scores[0]) if s >= threshold]
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    if not pairs:
        return "This was not discussed in the meeting."

    # Use top 2–3 chunks max
    top_pairs = pairs[:3]
    valid_chunks = [documents[i] for i, s in top_pairs]
    context = "\n".join(valid_chunks)
    context = context[:800]  # keep prompt compact

    # ---------- Guard check ----------
    guard_prompt = f"""
You are a meeting assistant.
Determine whether the answer to the question is explicitly present in the context.

Context:
{context}

Question:
{question}

If the answer is NOT explicitly in the context, reply exactly:
NO

If the answer IS explicitly in the context, reply exactly:
YES
"""

    guard_resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": guard_prompt}],
        temperature=0.0,
    ).choices[0].message.content.strip().lower()

    if "no" in guard_resp:
        return "This was not discussed in the meeting."

    # ---------- Final answer ----------
    answer_prompt = f"""
You are a meeting assistant.
Answer ONLY using the context below.
If the answer is not clearly stated, say:
"This was not discussed in the meeting."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": answer_prompt}],
        temperature=0.0,
    )

    return response.choices[0].message.content.strip()