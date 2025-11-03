"""
Portfoli-AI — Streamlit app (Groq + neon frosted UI + GitHub README preview + gTTS)
Place robi_context.py (your finalized context) in the same folder.
Add your Groq API key to Streamlit secrets: GROQ_API_KEY = "gsk_..."
"""

import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
import requests
import os
from urllib.parse import urlparse
from robi_context import context

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# -----------------------
# Session state init
# -----------------------
for key in ["messages", "chat_history", "history"]:
    if key not in st.session_state:
        st.session_state[key] = []

# -----------------------
# Sticky Header with broom clear button
# -----------------------
st.markdown("""
    <style>
        .sticky-header {
            position: fixed;
            top: 0; left: 0; width: 100%;
            background-color: #000;
            z-index: 9999;
            padding: 0.6rem 0;
            border-bottom: 1px solid #00bfff33;
        }
        .header-title {
            text-align: center;
            font-size: 22px;
            font-weight: 600;
            color: #00bfff;
            text-shadow: 0 0 12px #00bfff;
        }
        .clear-btn-container {
            position: absolute;
            top: 8px; right: 20px;
        }
        .clear-btn {
            background-color:#1e88e5;
            border:none;
            color:white;
            padding:5px 10px;
            border-radius:8px;
            cursor:pointer;
            font-weight:500;
        }
        .spacer { height: 65px; }
    </style>
    <div class="sticky-header">
        <div class="header-title">🤖 Portfoli-AI — Portfolio Assistant</div>
        <div class="clear-btn-container">
            <form action="" method="post">
                <button class="clear-btn" name="clear" type="submit">🧹 Clear Chat</button>
            </form>
        </div>
    </div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)

# -----------------------
# Clear chat functionality
# -----------------------
if "clear" in st.session_state:
    st.session_state.history = []
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.clear = False
if st.button("🧹 Clear Chat (Alt)", key="clear_top"):
    st.session_state.history = []
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.rerun()

# -----------------------
# Greeting message
# -----------------------
if "greeted" not in st.session_state or not st.session_state.greeted:
    st.markdown("""
    <div style='
        border-radius: 15px;
        padding: 18px;
        background: rgba(0, 191, 255, 0.08);
        border: 1px solid rgba(0,191,255,0.3);
        box-shadow: 0 0 15px rgba(0,191,255,0.4);
        font-family: "Inter", sans-serif;
        margin-bottom: 20px;
    '>
        <h4 style='color:#00bfff;'>👋 Hi!</h4>
        <p style='color:white;'>
        I'm <b style='color:#00bfff;'>Portfoli-AI 🤖</b>, your portfolio assistant.<br><br>
        Ask me about your <b>projects</b>, <b>skills</b>, or <b>business analytics insights</b>.<br>
        Try saying: <i>"Explain my Telco Churn Dashboard project."</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# -----------------------
# CSS
# -----------------------
st.markdown("""
<style>
body { background: #000; color: #e8f7ff; }
h1,h2,h3 { color: #00bfff; text-shadow: 0 0 12px #00bfff; }
.section-card {
  background: rgba(10,12,18,0.6);
  border-radius: 14px;
  padding: 14px;
  border: 1px solid rgba(0,191,255,0.18);
  box-shadow: 0 6px 26px rgba(0,191,255,0.06);
}
.chat-bubble-user {
  background: rgba(0,191,255,0.12);
  border: 1px solid rgba(0,191,255,0.25);
  color: #cffcff;
  padding: 10px 14px;
  border-radius: 12px;
  margin: 8px 0;
}
.chat-bubble-bot {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(0,191,255,0.12);
  color: #e8f7ff;
  padding: 10px 14px;
  border-radius: 12px;
  margin: 8px 0;
}
.small-muted { color: #98cfe6; font-size:12px; }
button.stButton>button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# Sidebar (unchanged)
# -----------------------
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown(f"### 👋 {context['owner_name']}")
st.sidebar.markdown(f"**{context['owner_role']}**")
st.sidebar.markdown("---")
st.sidebar.markdown("📬 **Contact**")
st.sidebar.markdown(f"- Email: <a href='mailto:rjimmichan@gmail.com'>rjimmichan@gmail.com</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- LinkedIn: <a href='https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291'>Profile</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- GitHub: <a href='https://github.com/Robin-Jimmichan-Pooppally'>Robin-Jimmichan-Pooppally</a>", unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Chat display
# -----------------------
for m in st.session_state.history:
    role = m.get("role")
    text = m.get("content")
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>Portfoli-AI:</b> {text}</div>", unsafe_allow_html=True)

# -----------------------
# Chat input (Enter to send)
# -----------------------
tts_toggle = st.checkbox("🔊 Play responses (TTS)", value=False)
user_input = st.text_input("Type your message...", key="chat_input", placeholder="Ask me anything and press Enter...")

# -----------------------
# Groq client
# -----------------------
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    if not api_key:
        st.error("Missing Groq API key.")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq()

# -----------------------
# gTTS helper
# -----------------------
def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        st.audio(buf.read(), format="audio/mp3")
    except Exception:
        st.warning("TTS unavailable.")

# -----------------------
# Chat response logic
# -----------------------
if user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": "You are Portfoli-AI, a portfolio chatbot."}]
    for h in st.session_state.history[-6:]:
        messages.append({"role": h["role"], "content": h["content"]})
    with st.spinner("Thinking..."):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.25,
                max_tokens=800,
            )
            reply = completion.choices[0].message.content.strip()
        except Exception as e:
            reply = f"⚠️ Groq API error: {e}"
    st.session_state.history.append({"role": "assistant", "content": reply})
    if tts_toggle:
        speak_text(reply)

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
