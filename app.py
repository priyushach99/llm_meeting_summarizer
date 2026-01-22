import streamlit as st
from transcriber import transcribe_audio
from summarizer import summarize_meeting
#from rag_utils import chunk_text, embed_chunks, build_faiss_index, query_rag
from rag_llma import build_vector_db, query_rag
from utils import generate_pdf

st.set_page_config(page_title="LLM Meeting Summarizer",
    layout="wide"
)

#st.title("LLM-Powered Meeting Summarizer")
st.markdown(
        "<h1 style='text-align: center;'>LLM-Powered Meeting Summarizer</h1>",
        unsafe_allow_html=True
    )


uploaded_file = st.file_uploader("Upload meeting audio", type=["mp3", "wav", "m4a"])

if uploaded_file:
    
    with open("temp_audio.mp3", "wb") as f:
        f.write(uploaded_file.read())
        
    # Play the audio in the app ref
    st.audio("temp_audio.mp3", format="audio/mp3")
    
    # -----------------------
    # Left & Right Panels
    # -----------------------
    left_col, right_col = st.columns([3,2])

    with left_col:
        st.info("Transcribing audio...")
        transcript = transcribe_audio("temp_audio.mp3")

        st.subheader("Transcript")
        st.write(transcript)
        
        # --- RAG Setup ---
        #chunks = chunk_text(transcript)
        #embeddings = embed_chunks(chunks)
        #index = build_faiss_index(embeddings)
        
        # After transcription
        build_vector_db(transcript)

        #chunks = transcript.split("\n")
        #build_vector_db(chunks)

        # --- Summary ---
        info_col, button_col = st.columns([8, 2])
        
        with info_col:
            st.info("Summary...")
            
        with button_col:    
            if st.button("Clear Cache"):
                from cache_utils import clear_cache
                clear_cache()
                st.success("Cache cleared. Summaries will regenerate next time.")
            
        summary, used_cache = summarize_meeting(transcript)
        st.info("Summary loaded from cache" if used_cache else "Generated new summary")

        st.subheader("Meeting Summary")
        st.write(summary)
    
    with right_col:
        st.subheader("Download & Ask")
    
        # PDF download button
        if st.button("Extract"):
            pdf_file = generate_pdf(transcript, summary)
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="Click to download PDF",
                    data=f,
                    file_name=pdf_file,
                    mime="application/pdf"
                )
        query = st.text_input("Ask about the meeting")

        if query:
            answer = query_rag(query)
            st.subheader("Answer:")
            st.write(answer)
    
    # --- RAG Search UI ---
    #st.subheader("🔍 Ask a Question About the Meeting")
    #user_question = st.text_input("Ask something...")

    #if user_question:
    #    result = query_rag(user_question, chunks, index)

    #    if result:
    #        st.success("Answer based on meeting context:")
    #        st.write(result)
    #    else:
    #        st.warning("❗ This topic was not discussed in the meeting.")
