# ===============================================
# 🚀 Portfoli-AI – Streamlit + Groq Chatbot App
# Author: Robin Jimmichan Pooppally
# Version: v1.0 (Production)
# ===============================================

import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
import base64
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from PIL import Image
from robi_context import context

# -----------------------------------------------
# 🌍 Load Environment Variables (optional local)
# -----------------------------------------------
load_dotenv()

# -----------------------------------------------
# 🔐 API Setup (Groq)
# -----------------------------------------------
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ Missing GROQ_API_KEY. Please add it to Streamlit secrets or .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

# -----------------------------------------------
# 🎨 Streamlit Page Config
# -----------------------------------------------
st.set_page_config(
    page_title="Portfoli-AI | Robin Jimmichan Pooppally",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------
# 💎 Custom CSS – Neon Frosted Glass UI
# -----------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(145deg, #000000, #05081a);
    background-attachment: fixed;
    color: #e0e8ff;
}
.chat-box {
    background: rgba(10, 15, 25, 0.6);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(0, 255, 255, 0.25);
    box-shadow: 0 0 20px rgba(0, 200, 255, 0.2);
    border-radius: 18px;
    padding: 20px;
    margin-top: 10px;
}
.chat-bubble-user {
    background: rgba(0, 255, 255, 0.15);
    border: 1px solid rgba(0, 255, 255, 0.3);
    border-radius: 12px;
    padding: 10px 14px;
    color: #e0ffff;
    margin: 5px 0;
}
.chat-bubble-bot {
    background: rgba(0, 40, 60, 0.6);
    border: 1px solid rgba(0, 200, 255, 0.2);
    border-radius: 12px;
    padding: 10px 14px;
    color: #d8efff;
    margin: 5px 0;
}
h1, h2, h3 {
    color: #00e0ff !important;
}
button[kind="primary"] {
    background: linear-gradient(90deg, #00d0ff, #0066ff);
    border: none;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------
# 🎤 Text-to-Speech Function
# -----------------------------------------------
def speak_text(text):
    try:
        tts = gTTS(text)
        buf = BytesIO()
        tts.write_to_fp(buf)
        audio_bytes = buf.getvalue()
        st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.warning("TTS unavailable at the moment.")

# -----------------------------------------------
# 🧠 Chatbot Function
# -----------------------------------------------
def ask_portfoliai(prompt):
    """Send prompt to Groq LLM"""
    try:
        full_prompt = f"""
        You are {context['assistant_name']}, a professional portfolio assistant for {context['owner_name']}.
        Reference the provided context only:
        {json.dumps(context, indent=2)}

        User question: {prompt}
        """
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": full_prompt}],
            temperature=0.6,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"⚠️ API error: {e}")
        return None

# -----------------------------------------------
# 🚀 Main Streamlit UI
# -----------------------------------------------
st.title("🤖 Portfoli-AI – Robin Jimmichan’s Portfolio Assistant")

# Show greeting once
if "greeted" not in st.session_state:
    st.session_state.greeted = True
    st.markdown(f'<div class="chat-box"><div class="chat-bubble-bot">{context["greeting_message"]}</div></div>', unsafe_allow_html=True)

# User query input
user_query = st.chat_input("Ask about any of Robin’s projects...")

if user_query:
    st.markdown(f'<div class="chat-box"><div class="chat-bubble-user">👤 {user_query}</div></div>', unsafe_allow_html=True)
    bot_reply = ask_portfoliai(user_query)
    if bot_reply:
        st.markdown(f'<div class="chat-box"><div class="chat-bubble-bot">🤖 {bot_reply}</div></div>', unsafe_allow_html=True)
        with st.expander("🔊 Listen to this response"):
            speak_text(bot_reply)

# Sidebar — Quick Filters
st.sidebar.header("🎯 Filter by Project Type")
for category in context["projects"].keys():
    if st.sidebar.button(category):
        st.markdown(f"### 📂 {category} Projects")
        for proj_name, link in context["projects"][category].items():
            st.markdown(f"🔹 **[{proj_name}]({link})**")

# Footer
st.markdown("<br><center>💡 Built with ❤️ using Streamlit + Groq</center>", unsafe_allow_html=True)
