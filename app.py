import streamlit as st
import time
from gtts import gTTS
import os
from io import BytesIO
from groq import Groq
from robi_context import PROJECT_CONTEXT

# --- Page Config ---
st.set_page_config(
    page_title="Robin's Portfoli-AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Neon CSS + UI Effects ---
st.markdown("""
    <style>
    body {
        background-color: #0d1117;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
    }
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: #00bfff;
        border: 1px solid #00bfff;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 0 10px rgba(0,191,255,0.3);
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background: rgba(0,191,255,0.1);
        border-left: 3px solid #00bfff;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background: rgba(255,255,255,0.05);
        border-left: 3px solid #00bfff;
    }
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    @keyframes blink {
        50% { border-color: transparent }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .typing {
        color: #00bfff;
        font-size: 1.5rem;
        border-right: 3px solid #00bfff;
        white-space: nowrap;
        overflow: hidden;
        width: 0;
        animation: typing 3.5s steps(50, end), blink .75s step-end infinite;
        text-shadow: 0 0 10px #00bfff, 0 0 30px #00bfff;
    }
    .subtitle {
        color: #bdbdbd;
        font-size: 1rem;
        margin-top: 10px;
        opacity: 0;
        animation: fadeIn 1s ease-in forwards;
        animation-delay: 3.8s;
    }
    .fade-wrapper {
        text-align: center;
        margin-top: 50px;
    }
    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #8b949e;
        margin-top: 60px;
        border-top: 1px solid rgba(0,191,255,0.2);
        padding-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Animated Neon Greeting ---
st.markdown("""
    <div class='fade-wrapper'>
        <div class='typing'>👋 Hey there! I’m Robin’s Portfoli-AI — your interactive portfolio assistant 🚀</div>
        <div class='subtitle'>Built with Streamlit, Groq & a dash of neon energy ⚡</div>
    </div>
""", unsafe_allow_html=True)

time.sleep(4)  # cinematic delay before chatbot loads
st.write("")  # spacer

# --- Initialize Groq Client ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Chat State ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey Robin 👋! I’m your Portfoli-AI — ask me about any of your 21 projects, tools used, or how you built them."}
    ]

# --- Chat UI ---
st.title("💬 Robin’s Portfoli-AI Chatbot")
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- User Input ---
prompt = st.chat_input("Ask me anything about Robin’s projects...")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- AI Context Integration ---
    context_prompt = f"""
    You are Robin’s Portfolio AI. Use this project context to answer:
    {PROJECT_CONTEXT}
    The user asked: {prompt}
    Be specific, accurate, and do not hallucinate.
    """

    # --- Groq Response ---
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": context_prompt}]
    )

    answer = response.choices[0].message.content
    st.chat_message("assistant").write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

    # --- Optional Voice Response (TTS) ---
    tts = gTTS(answer, lang="en")
    tts_path = "response.mp3"
    tts.save(tts_path)
    st.audio(tts_path, format="audio/mp3")

# --- Footer ---
st.markdown("""
<div class="footer">
    <p>📧 <a href="mailto:rjimmichan@gmail.com" target="_blank" style="color:#00bfff;">rjimmichan@gmail.com</a> |
    💼 <a href="https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291" target="_blank" style="color:#00bfff;">LinkedIn</a> |
    🧠 <a href="https://github.com/Robin-Jimmichan-Pooppally" target="_blank" style="color:#00bfff;">GitHub</a></p>
    <p>© 2025 Robin’s Portfoli-AI. All rights reserved ⚡</p>
</div>
""", unsafe_allow_html=True)
