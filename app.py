import streamlit as st
from groq import Groq
from gtts import gTTS
import os, base64
import pandas as pd
from dotenv import load_dotenv
from io import BytesIO

# ---------------------- ENV + API ----------------------
load_dotenv()
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------- CONFIG ----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="💡", layout="wide")

# ---------------------- STYLING ----------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #000010, #020b1a 70%);
    color: white;
}
div[data-testid="stAppViewContainer"] {
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 2rem;
}
.chat-message {
    border: 1px solid rgba(0, 255, 255, 0.25);
    border-radius: 10px;
    padding: 0.9rem;
    margin-bottom: 0.8rem;
    box-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
}
.stButton>button {
    background-color: #001f33;
    border: 1px solid #00ffff;
    color: #00ffff;
    border-radius: 8px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #00ffff;
    color: #000;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR ----------------------
st.sidebar.markdown("### 👋 Welcome to Portfoli-AI")
st.sidebar.markdown("Your AI-powered portfolio companion")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📬 Connect with me:")
st.sidebar.write("**📧 Email:** [rjimmichan@gmail.com](mailto:rjimmichan@gmail.com)")
st.sidebar.write("**💻 GitHub:** [Robin-Jimmichan-Pooppally](https://github.com/Robin-Jimmichan-Pooppally)")
st.sidebar.write("**🔗 LinkedIn:** [Robin Jimmichan Pooppally](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")

st.sidebar.markdown("---")
repo_list = [
    "Telco-Customer-Churn-Analysis",
    "Financial-Performance-Dashboard-PowerBI-Project",
    "Airbnb-NYC-Price-Analysis",
    "HR-Analytics-Employee-Attrition",
    "Sales-Performance-Excel-Dashboard"
]
selected_repo = st.sidebar.selectbox("📁 Choose a Project Repo", repo_list)
st.sidebar.markdown(f"[🔍 View on GitHub](https://github.com/Robin-Jimmichan-Pooppally/{selected_repo})")

# ---------------------- MAIN ----------------------
st.markdown("<h1 style='text-align:center; color:#00ffff;'>💬 Portfoli-AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your neon-lit AI portfolio assistant</p>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("💡 Ask me about my projects, skills, or insights:", key="input_text")
col1, col2 = st.columns([1, 0.2])
with col1:
    send = st.button("🚀 Send")
with col2:
    tts_enabled = st.toggle("🔊 TTS", value=False)

# ---------------------- CHAT ----------------------
if send and user_input:
    with st.spinner("Thinking..."):
        try:
            completion = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "You are Portfoli-AI, Robin Jimmichan's intelligent portfolio assistant."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = completion.choices[0].message.content
            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("bot", answer))

            if tts_enabled:
                tts = gTTS(answer)
                tts.save("response.mp3")
                audio_bytes = open("response.mp3", "rb").read()
                b64 = base64.b64encode(audio_bytes).decode()
                st.markdown(
                    f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}"></audio>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"⚠️ Groq API error: {e}")

# ---------------------- DISPLAY ----------------------
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"<div class='chat-message'><b>🧑 You:</b> {msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-message'><b>🤖 Portfoli-AI:</b> {msg}</div>", unsafe_allow_html=True)
