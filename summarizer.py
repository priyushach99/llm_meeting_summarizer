#from openai import OpenAI
#import os
import streamlit as st
from groq import Groq
import os
from cache_utils import get_hash, load_cache, save_cache

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_groq_client():
    try:
        return Groq(api_key=st.secrets["GROQ"]["API_KEY"])
    except Exception:
        return Groq(api_key=os.getenv("GROQ_API_KEY"))


def summarize_meeting(transcript):
    
    client = get_groq_client()   # <— FIXED: client created here
    
    cache = load_cache()
    transcript_hash = get_hash(transcript)

    # Return cached results
    if transcript_hash in cache:
        print(" Loaded summary from cache")
        return cache[transcript_hash], True
    prompt = f"""
You are an AI assistant summarizing a meeting transcript.

STRICT RULES:
- Use ONLY information explicitly stated in the transcript.
- Do NOT infer intent, meaning, or next steps.
- Do NOT add assumptions or missing details.
- If something is unclear or missing, write "Not specified".
- Follow the output format exactly.
- Each field must be on its own line.

FORMAT:

Meeting Summary

Key Discussion Points:
- <bullet points>

Decisions Made:
- <bullet points>

Action Items:
- Owner: <name or Not specified>
  Task: <task or Not specified>
  Deadline: <date or Not specified>

Transcript:
{transcript}
"""
    try: 
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=0.8,
            frequency_penalty=0.2,
            presence_penalty=0.0
        )

        #summary = response["message"]["content"]
        summary = response.choices[0].message.content
        
        # Save to cache
        cache[transcript_hash] = summary
        save_cache(cache)
        
        return summary, False
    
    except Exception as e:
        import traceback
        st.error("Groq API Error:")
        st.error(str(e))
        st.code(traceback.format_exc())
        return "Summary could not be generated due to API error.", False
     

    #response = client.chat.completions.create(
    #    model="gpt-4o-mini",
    #    messages=[{"role": "user", "content": prompt}],
    #    temperature=0.3
    #)

    #return response.choices[0].message.content
