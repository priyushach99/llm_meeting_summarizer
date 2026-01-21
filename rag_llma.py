from sentence_transformers import SentenceTransformer
import streamlit as st
import faiss
import numpy as np
from groq import Groq
import os

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_groq_client():
    try:
        return Groq(api_key=st.secrets["GROQ"]["API_KEY"])   # Streamlit Cloud
    except Exception:
        return Groq(api_key=os.getenv("GROQ_API_KEY"))       # Local dev


documents = []
index = None

def build_vector_db(chunks):
    global index, documents
    documents = chunks
    embeddings = embedder.encode(chunks).astype("float32")
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

def query_rag(question, top_k=5, threshold=0.40):
    global index, documents
    
    client = get_groq_client()   # <— FIX: create client inside function

    # Step 1: Embed question
    q_emb = embedder.encode([question]).astype("float32")
    faiss.normalize_L2(q_emb)

    # Step 2: Retrieve top-k chunks
    scores, indices = index.search(q_emb, k=top_k)

    # Filter by threshold val
    pairs = [(i, s) for i, s in zip(indices[0], scores[0]) if s >= threshold]
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    if not pairs:
        return "This was not discussed in the meeting."

    valid_chunks = [documents[i] for i, s in pairs]
    context = "\n".join(valid_chunks)

    # Step 3: Guard check — ask LLM if answer exists
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

    guard = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": guard_prompt}]
    ).choices[0].message.content.strip()
    #)["message"]["content"].strip()

    if guard == "NO":
        return "This was not discussed in the meeting."

    # Step 4: Now answer using the same context
    answer_prompt = f"""
You are a meeting assistant.
Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": answer_prompt}]
    )

    return response.choices[0].message.content