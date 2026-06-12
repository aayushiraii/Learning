import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit_mic_recorder import mic_recorder

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

st.set_page_config(
    page_title="Voice Agent",
    layout="centered"
)

st.title("Voice Agent")

audio = mic_recorder(
    start_prompt="Start Recording",
    stop_prompt="Stop Recording",
    just_once=True
)

if audio:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
        temp.write(audio["bytes"])
        temp_path = temp.name

    with st.spinner("Transcribing audio..."):
        with open(temp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )

    user_text = transcript.text

    st.subheader("Transcription")
    st.write(user_text)

    with st.spinner("Generating response..."):
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=user_text
        )

    answer = response.output_text

    st.subheader("Agent Response")
    st.write(answer)

    speech_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    speech_path = speech_file.name
    speech_file.close()

    with st.spinner("Generating voice response..."):
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=answer
        ) as speech_response:
            speech_response.stream_to_file(speech_path)

    st.subheader("Voice Response")
    st.audio(speech_path, format="audio/mp3")