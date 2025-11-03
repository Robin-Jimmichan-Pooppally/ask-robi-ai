"""
Portfoli-AI — Streamlit app (Groq + neon frosted UI + GitHub README preview + gTTS)
Requirements: see requirements.txt provided below
Place robi_context.py (the context you finalized) in same folder.
Add your Groq API key to Streamlit secrets: GROQ_API_KEY = "gsk_..."
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
from robi_context import context

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# -----------------------
# Initialize session state
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "history" not in st.session_state:
    st.session_state.history = []

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
        .spacer {
            height: 65px;
        }
    </style>
    <div class="sticky-header">
        <div class="header-title">🤖 Portfoli-AI — Portfolio Assistant</div>
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
# CSS (neon blue frosted glass)
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
# Sidebar + project list etc. (unchanged)
# -----------------------
# keep everything below identical to your original

# Portfolio overview, category filters, Groq, chat logic, TTS, etc. stay unchanged

# -----------------------
# Chat UI
# -----------------------
for m in st.session_state.history:
    role = m.get("role")
    text = m.get("content")
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>{context.get('assistant_name','Portfoli-AI')}:</b> {text}</div>", unsafe_allow_html=True)

tts_toggle = st.checkbox("🔊 Play responses (TTS)", value=False)

# --- Input row: only erase button ---
col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.text_input("Type your message...", key="chat_input", placeholder="Ask me anything...")

with col2:
    erase = st.button("🧹")

if erase:
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.history = []
    st.rerun()

# --- Auto-send on Enter ---
if user_input.strip():
    st.session_state.history.append({"role": "user", "content": user_input})
    system_prompt = build_system_prompt(st.session_state.chat_mode, st.session_state.get("selected_project"))
    messages = [{"role": "system", "content": system_prompt}]
    for h in st.session_state.history[-8:]:
        role_map = "user" if h["role"] == "user" else "assistant"
        messages.append({"role": role_map, "content": h["content"]})
    with st.spinner("Thinking..."):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.25,
                max_tokens=800,
            )
            bot_text = completion.choices[0].message.content.strip()
        except Exception as e:
            bot_text = f"⚠️ Groq API error: {e}"
    st.session_state.history.append({"role": "assistant", "content": bot_text})
    if tts_toggle:
        try:
            speak_text(bot_text)
        except Exception:
            st.warning("TTS failed for this response.")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)

