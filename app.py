"""
Portfoli-AI — Streamlit app (Groq + neon frosted UI + GitHub README preview + gTTS)
"""

import streamlit as st
from groq import Groq
from gtts import gTTS
from io import BytesIO
import requests
import json
import os
import textwrap
from urllib.parse import urlparse

# Import verified context
from robi_context import context

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# -----------------------
# Initialize session state
# -----------------------
for key in ["messages", "chat_history", "history", "selected_project", "readme_full", "readme_preview", "show_more"]:
    if key not in st.session_state:
        st.session_state[key] = [] if "history" in key or "messages" in key or "chat" in key else None
st.session_state.show_more = False

# -----------------------
# Handle clear chat (from URL param)
# -----------------------
if "clear" in st.query_params:
    for k in ["messages", "chat_history", "history"]:
        st.session_state[k] = []
    st.experimental_rerun()

# --- Sticky Header ---
st.markdown("""
    <style>
        .sticky-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #000000;
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
            top: 8px;
            right: 20px;
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
        <div class="header-title">🤖 Portfoli-AI — Robin Jimmichan’s Portfolio Assistant</div>
        <div class="clear-btn-container">
            <form action="" method="get">
                <button class="clear-btn" name="clear" type="submit">🧹 Clear Chat</button>
            </form>
        </div>
    </div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)

# -----------------------
# Greeting message
# -----------------------
if "greeted" not in st.session_state:
    st.session_state.greeted = False

if not st.session_state.greeted:
    st.markdown("""
    <div style='border-radius: 15px; padding: 18px; background: rgba(0, 191, 255, 0.08);
                border: 1px solid rgba(0,191,255,0.3); box-shadow: 0 0 15px rgba(0,191,255,0.4);
                font-family: "Inter", sans-serif; margin-bottom: 20px;'>
        <h4 style='color:#00bfff;'>👋 Hey!</h4>
        <p style='color:white;'>
        I'm <b style='color:#00bfff;'>Portfoli-AI 🤖</b>, your portfolio assistant.<br><br>
        Ask me about your <b>projects</b>, <b>skills</b>, or <b>business analytics insights</b>.<br>
        Try saying: <i>"Explain my Telco Churn Dashboard project."</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# -----------------------
# Neon CSS
# -----------------------
st.markdown("""
<style>
body { background: #000000; color: #e8f7ff; }
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
# Sidebar + rest (unchanged)
# -----------------------
# everything below remains the same as your original

# -----------------------
# Fix user input handling safely
# -----------------------
tts_toggle = st.checkbox("🔊 Play responses (TTS)", value=False)

user_input = st.text_input("Type your message and press Enter...", key="chat_input", placeholder="Ask me anything...")

# If user pressed Enter (non-empty message)
if user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_input = ""  # safely clear

    # Build prompt and call Groq
    system_prompt = f"Use Robin's verified context: {context.get('persona','')}"
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        with st.spinner("Thinking..."):
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.history[-8:],
                ],
                temperature=0.25,
                max_tokens=800,
            )
            bot_text = completion.choices[0].message.content.strip()
    except Exception as e:
        bot_text = f"⚠️ Groq API error: {e}"

    st.session_state.history.append({"role": "assistant", "content": bot_text})
    if tts_toggle:
        try:
            tts = gTTS(bot_text)
            buf = BytesIO()
            tts.write_to_fp(buf)
            buf.seek(0)
            st.audio(buf.read(), format="audio/mp3")
        except Exception:
            st.warning("TTS failed.")

# -----------------------
# Display chat bubbles
# -----------------------
for m in st.session_state.history:
    if m["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {m['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>Portfoli-AI:</b> {m['content']}</div>", unsafe_allow_html=True)

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
