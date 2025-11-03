"""
Robi.AI - Fixed Streamlit App (app_fixed.py)
Dark mode only • Neon cyan accent • TTS for all responses • Robin's Portfoli-AI

This file replaces the original app.py. It imports ROBIN_CONTEXT from robi_context.py (created separately) and provides a polished Streamlit UI with:
- Dark theme CSS
- Neon-cyan accent
- Streaming responses via Groq client (same client usage as before)
- Built-in TTS for all assistant replies using gTTS (server-side) and browser audio playback
- Project browser: view README text and code snippets loaded from ROBIN_CONTEXT
- Speaker toggle and mute/unmute

NOTE: put this file, robi_context.py and requirements.txt in the same folder and set the secret GROQ_API_KEY in Streamlit Cloud.
"""

import streamlit as st
from groq import Groq
import time
from datetime import datetime
from gtts import gTTS
import io
import base64
import re

# Import ROBIN_CONTEXT which contains full project READMEs, code snippets, and metadata
from robi_context import ROBIN_CONTEXT

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Robin's Portfoli-AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DARK THEME CSS + ACCENT ====================
ACCENT = "#00FFFF"  # Neon Cyan
st.markdown(f"""
<style>
/* Base dark background */
body {{ background-color: #0b0f14; color: #e6eef8; }}
section.main {{ background-color: transparent; }}
/* Chat bubbles */
[data-testid='stChatMessage'] .stMarkdown {{ color: #e6eef8; }}
/* Accent color for buttons and links */
a, .stButton>button, .stDownloadButton>button {{
  background: linear-gradient(90deg, rgba(0,255,255,0.06), rgba(0,255,255,0.02));
  border: 1px solid {ACCENT};
  color: #e6eef8 !important;
}}
.stButton>button:hover {{ box-shadow: 0 0 12px {ACCENT}; }}
/* Header card */
.header-card {{ background: linear-gradient(135deg, rgba(102,126,234,0.12), rgba(118,75,162,0.12)); padding:18px; border-radius:12px; }}
/* Speaker icon style */
.speaker {{ font-size: 20px; color: {ACCENT}; cursor: pointer; }}
/* Make sidebar dark */
[data-testid='stSidebar'] {{ background-color: #071018; color: #dfefff; }}
</style>
""", unsafe_allow_html=True)

# ==================== SAMPLE QUESTIONS ====================
SAMPLE_QUESTIONS = [
    "How did Robin achieve 92% forecasting accuracy?",
    "Tell me about the Loan Default Risk project",
    "What are the key findings in the Loan Default Risk analysis?",
    "Explain the E-commerce Funnel Analysis",
    "Show me all SQL projects",
    "What Python projects has Robin done?",
    "Compare Excel vs Power BI projects",
    "What's the biggest business impact achieved?",
    "Explain the RFM segmentation approach",
    "Tell me about healthcare analytics work"
]

# ==================== SESSION STATE ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking_active" not in st.session_state:
    st.session_state.thinking_active = False

if "api_error_count" not in st.session_state:
    st.session_state.api_error_count = 0

if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True  # by default TTS on for all responses

if "muted" not in st.session_state:
    st.session_state.muted = False

# ==================== GROQ CLIENT ====================
@st.cache_resource
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            st.error("❌ GROQ_API_KEY is empty in Streamlit Cloud Secrets!")
            st.stop()
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Groq Connection Error: {str(e)}")
        st.info("Make sure your GROQ_API_KEY is correct in Streamlit Cloud Secrets")
        st.stop()

try:
    client = init_groq()
except Exception as e:
    st.error(f"Failed to initialize: {str(e)}")
    st.stop()

# ==================== TTS FUNCTION ====================
def speak_response(text: str) -> io.BytesIO:
    """Convert text to speech using gTTS and return BytesIO containing mp3"""
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        return audio_fp
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")
        return None

# Helper to play audio in streamlit
def st_audio_bytes(audio_bytes: io.BytesIO):
    st.audio(audio_bytes, format='audio/mp3')

# ==================== STREAMING RESPONSE ====================
def stream_llm_response(prompt: str, placeholder) -> tuple:
    """Stream LLM response with error handling"""
    st.session_state.thinking_active = True
    try:
        with st.spinner("🚀 Connecting to AI..."):
            time.sleep(0.2)

        messages_for_api = [
            {"role": "system", "content": ROBIN_CONTEXT},
            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] in ("user","assistant")]
        ]

        full_response = ""
        response_placeholder = placeholder.empty()

        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=1500,
                top_p=0.9,
                stream=True,
                timeout=45
            )

            for chunk in stream:
                # defensive access
                delta = getattr(chunk.choices[0], 'delta', None)
                if delta and getattr(delta, 'content', None):
                    token = delta.content
                    full_response += token
                    with response_placeholder.container():
                        st.markdown(full_response + "▌")

            with response_placeholder.container():
                st.markdown(full_response)

            st.session_state.thinking_active = False
            st.session_state.api_error_count = 0
            return full_response, None

        except Exception as stream_error:
            st.session_state.thinking_active = False
            error_msg = f"Stream Error: {str(stream_error)}"
            with response_placeholder.container():
                st.error(f"🚨 Connection interrupted. Please try again.")
            st.session_state.api_error_count += 1
            return None, error_msg

    except Exception as e:
        st.session_state.thinking_active = False
        error_msg = f"Connection Error: {str(e)}"
        with placeholder.container():
            st.error(f"🚨 Oops! I seem to have lost my connection. Please try again in a moment.")
        st.session_state.api_error_count += 1
        return None, error_msg

# ==================== PROJECTS PARSER (from ROBIN_CONTEXT) ====================
# ROBIN_CONTEXT is a large string. We'll parse project headings and READMEs from it.
PROJECTS = {}

def parse_projects_from_context(context_text: str):
    # Heuristic: projects are listed under headers like '=== EXCEL PROJECTS (6) ===' or '=== POWER BI PROJECTS (5) ==='
    # We parse blocks starting with project numbering like '1. **Project Name**'
    projects = {}
    lines = context_text.splitlines()
    current = None
    buffer = []
    for line in lines:
        m = re.match(r"^\d+\. \*\*(.+)\*\*", line.strip())
        if m:
            # store previous
            if current:
                projects[current] = "\n".join(buffer).strip()
            current = m.group(1).strip()
            buffer = []
            # add the project title line also
            buffer.append(line.strip())
        else:
            if current:
                buffer.append(line)
    # final flush
    if current:
        projects[current] = "\n".join(buffer).strip()
    return projects

PROJECTS = parse_projects_from_context(ROBIN_CONTEXT)

# ==================== MAIN UI ====================
st.markdown(f"""
<div class='header-card'>
  <h1 style='color: {ACCENT}; margin:0;'>🤖 Robin's Portfoli-AI</h1>
  <p style='color: #cfefff; margin:0.2rem 0 0;'>Ask about Robin's 21 Business Analytics Projects — Excel, SQL, Power BI, Python</p>
</div>
""", unsafe_allow_html=True)

st.write(" ")
col1, col2 = st.columns([3,1])
with col2:
    # Controls: mute toggle and TTS toggle
    st.markdown("### Controls")
    if st.button("🔊 Toggle TTS"):
        st.session_state.tts_enabled = not st.session_state.tts_enabled
    if st.button("🔇 Mute/Unmute"):
        st.session_state.muted = not st.session_state.muted
    st.write(f"TTS: {'On' if st.session_state.tts_enabled else 'Off'} — Muted: {'Yes' if st.session_state.muted else 'No'}")
    st.markdown("---")
    st.markdown("### Quick Links")
    if st.button("Show Project List"):
        with st.expander("All Projects (extracted from ROBIN_CONTEXT)"):
            for i, k in enumerate(PROJECTS.keys(), start=1):
                st.markdown(f"**{i}. {k}**")

with col1:
    st.write("👋 Hi! I'm Robin's AI assistant. Ask me about his **21 projects** across **Excel, SQL, Power BI, and Python**!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Robin's projects..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    response_placeholder = st.empty()
    with st.chat_message("assistant", avatar="🤖"):
        response_text, error = stream_llm_response(prompt, response_placeholder)
        if response_text:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })
            st.success("✅ Response complete!")
            # TTS playback if enabled and not muted
            if st.session_state.tts_enabled and not st.session_state.muted:
                with st.spinner("🔊 Generating audio..."):
                    audio = speak_response(response_text)
                    if audio:
                        st_audio_bytes(audio)
        else:
            if st.session_state.api_error_count > 2:
                st.warning("💡 Multiple errors detected. Please refresh and try again.")
            else:
                st.info("Feel free to try asking again!")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.checkbox("Enable Text-to-Speech for responses", value=st.session_state.tts_enabled, key="_tts_checkbox")
    st.markdown("---")
    st.markdown("### 📚 About")
    st.write("Robin's Business Analytics portfolio with **21 real projects** across 10+ industries.")
    st.markdown("### 📊 Project Breakdown")
    col1s, col2s = st.columns(2)
    with col1s:
        st.metric("Excel", "6")
        st.metric("Power BI", "5")
    with col2s:
        st.metric("SQL", "6")
        st.metric("Python", "4")
    st.markdown("---")
    st.markdown("### 🔗 Quick Navigation")
    # allow user to pick a project to view README
    project_names = list(PROJECTS.keys())
    selected = st.selectbox("Open project README", ["— select —"] + project_names)
    if selected and selected != "— select —":
        st.markdown(f"### {selected}")
        st.code(PROJECTS[selected][:4000])  # show first chunk; README is large
        if st.button("Show full README and code (open in new panel)"):
            with st.expander(f"Full README — {selected}"):
                st.markdown(PROJECTS[selected])
                st.download_button("Download README as .md", PROJECTS[selected], file_name=f"{selected}.md")
    st.markdown("---")
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()
    st.markdown("---")
    st.caption("Built with ❤️ by Robin | Robin's Portfoli-AI")

# Footer note
st.markdown("---")
st.write("Tip: Ask for specific project sections like 'DAX measures' or 'SQL queries' to see exact code snippets available in the README.")

# End of app_fixed.py
