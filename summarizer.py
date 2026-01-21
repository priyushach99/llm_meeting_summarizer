#from openai import OpenAI
#import os
from groq import Groq
import os
from cache_utils import get_hash, load_cache, save_cache

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_meeting(transcript):
    cache = load_cache()
    transcript_hash = get_hash(transcript)

    # Return cached results
    if transcript_hash in cache:
        print(" Loaded summary from cache")
        return cache[transcript_hash], True
    prompt = f"""
You are an AI meeting assistant.

Rules:
1. Only include information present in the transcript.
2. Do NOT assume, infer, or add anything that is not explicitly stated.
3. Do NOT invent names, or deadlines.
4. If something is missing, write "Not specified".
5. Use the exact format below:

Summarize the meeting clearly and extract action items.
Requirements:
- Key discussion points
- Decisions made
- Action items in bullet format like:
    - Owner: Name
    - Task: What needs to be done
    - Deadline: When it is due (if mentioned)

Transcript:
{transcript}
"""
    try: 
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            top_p=0.8,
            repeat_penalty=1.1
        )

        #summary = response["message"]["content"]
        summary = response.choices[0].message.content
    
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        summary = "Summary could not be generated due to API error."
    
    # Save to cache
    cache[transcript_hash] = summary
    save_cache(cache)

    return summary, False 

    #response = client.chat.completions.create(
    #    model="gpt-4o-mini",
    #    messages=[{"role": "user", "content": prompt}],
    #    temperature=0.3
    #)

    #return response.choices[0].message.content
