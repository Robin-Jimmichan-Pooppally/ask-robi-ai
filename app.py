"""
Robi.AI - Production Chatbot (patched)
- Fixes: message assembly bug, st.toggle -> st.checkbox
- Adds: defensive streaming parsing, retry/backoff, TTS caching
- Keep your existing robi_context.py in the same folder (ROBIN_CONTEXT variable)
"""

import os
import io
import time
import logging
from datetime import datetime
from typing import Optional, Tuple

import streamlit as st
from groq import Groq
from gtts import gTTS

# Import ROBIN_CONTEXT from separate file you provided
from robi_context import ROBIN_CONTEXT

# -----------------------
# Basic logging
# -----------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("robi_ai")

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Ask Robi.AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    "Tell me about healthcare analytics work",
]

# ==================== SESSION STATE ====================
if "messages" not in st.session_state:
    # initialize with an optional assistant greeting (or leave empty)
    st.session_state.messages = []

if "thinking_active" not in st.session_state:
    st.session_state.thinking_active = False

if "api_error_count" not in st.session_state:
    st.session_state.api_error_count = 0

if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = False

# ==================== GROQ CLIENT INITIALIZATION ====================
@st.cache_resource
def init_groq_client() -> Groq:
    """
    Initialize Groq client. Expects GROQ_API_KEY to be in Streamlit secrets
    or environment variables. If missing, raise a clear error (Streamlit UI will show it).
    """
    api_key = None

    # prefer Streamlit secrets (on Streamlit Cloud)
    try:
        api_key = st.secrets.get("GROQ_API_KEY")  # may return None
    except Exception:
        api_key = None

    # fallback to environment variable
    if not api_key:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        # Instead of st.stop(), raise an informative exception so the app shows it clearly
        raise RuntimeError(
            "GROQ_API_KEY not found. Please set GROQ_API_KEY in Streamlit Secrets or environment variables."
        )

    # create client
    try:
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq client: {e}")


# initialize client (wrapped to show a friendly error in UI)
try:
    client = init_groq_client()
except Exception as e:
    # show friendly UI and stop further execution on this session
    st.error(str(e))
    st.info("Add the key to Streamlit Secrets (Streamlit Cloud) or set env var GROQ_API_KEY locally.")
    st.stop()

# ==================== TTS CACHING ====================
@st.cache_data(max_entries=128, ttl=60 * 60)  # cache audio for 1 hour
def tts_bytes(text: str) -> Optional[bytes]:
    """Generate and cache TTS bytes for a given text."""
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buf = io.BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        logger.exception("TTS generation failed")
        return None


# ==================== HELPER: SAFE STREAM CHUNK PARSING ====================
def safe_get_token_from_chunk(chunk) -> Optional[str]:
    """
    Safely extract streaming token from a Groq stream chunk.
    Returns token string if found, else None.
    Defensive against shape changes.
    """
    try:
        # chunk.choices is typically a list
        choices = getattr(chunk, "choices", None)
        if not choices:
            return None
        first_choice = choices[0]
        delta = getattr(first_choice, "delta", None)
        if not delta:
            return None
        token = getattr(delta, "content", None)
        return token
    except Exception:
        # any unexpected shape: ignore this chunk
        return None


# ==================== STREAMING RESPONSE HANDLING (with retries) ====================
def stream_llm_response(prompt: str, placeholder) -> Tuple[Optional[str], Optional[str]]:
    """
    Streams LLM response into the provided placeholder.
    Returns (full_response, error_message). On success error_message is None.
    """
    st.session_state.thinking_active = True
    response_placeholder = placeholder.empty()
    # friendly spinner
    try:
        with st.spinner("🚀 Connecting to AI..."):
            time.sleep(0.15)
    except Exception:
        pass

    # Build messages_for_api: include the system context + ALL prior messages
    messages_for_api = [
        {"role": "system", "content": ROBIN_CONTEXT},
        *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
    ]

    max_retries = 2
    attempt = 0
    backoff_base = 1.0  # seconds

    while attempt <= max_retries:
        attempt += 1
        try:
            # Request streaming completions
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=1500,
                top_p=0.9,
                stream=True,
                timeout=45,
            )

            full_response = ""
            partial_shown = False

            # Stream tokens as they come
            for chunk in stream:
                token = safe_get_token_from_chunk(chunk)
                if token:
                    full_response += token
                    # update placeholder with a caret to indicate streaming
                    with response_placeholder.container():
                        st.markdown(full_response + "▌")
                    partial_shown = True

            # streaming finished normally
            with response_placeholder.container():
                # write final response (no caret)
                st.markdown(full_response)

            # reset thinking / errors and return
            st.session_state.thinking_active = False
            st.session_state.api_error_count = 0
            return full_response, None

        except Exception as e:
            # increment error counter and decide whether to retry
            st.session_state.api_error_count += 1
            logger.exception("Streaming attempt failed")
            # show a brief retry message
            with response_placeholder.container():
                st.warning(
                    f"⚠️ Connection interrupted (attempt {attempt}/{max_retries}). Retrying..."
                )
            # if we've exhausted retries, show final error
            if attempt > max_retries:
                st.session_state.thinking_active = False
                err_msg = f"Stream Error: {str(e)}"
                with response_placeholder.container():
                    st.error("🚨 Connection interrupted. Please try again later.")
                return None, err_msg
            # exponential backoff sleep before retrying
            time.sleep(backoff_base * attempt)

    # Fallback if loop ends unexpectedly
    st.session_state.thinking_active = False
    return None, "Unknown streaming error"


# ==================== APP UI ====================

# Header
st.markdown(
    """
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🤖 Ask Robi.AI</h1>
        <p style="color: #f0f0f0; margin-top: 0.5rem;">Your Interactive Guide to Robin's 21 Business Analytics Projects</p>
        <p style="color: #e0e0e0; margin-top: 1rem; font-size: 0.9rem;">Powered by Groq Llama 3.3 • Streaming ⚡ • TTS 🔊</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("👋 Hi! I'm Robin's AI assistant. Ask me about his **21 projects** across **Excel, SQL, Power BI, and Python**!")

# Display chat history
for message in st.session_state.messages:
    # use st.chat_message to keep the chat UI consistent (if available)
    role = message.get("role", "user")
    avatar = "🤖" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.get("content", ""))

# Chat input block
if prompt := st.chat_input("Ask about Robin's projects..."):
    # append user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # placeholder for streaming assistant response
    response_placeholder = st.empty()

    # call the streaming function
    response_text, error = stream_llm_response(prompt, response_placeholder)

    # only append assistant message if there's a successful full response
    if response_text:
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response_text)

        st.success("✅ Response complete!")

        # If TTS enabled, play audio (use cached bytes)
        if st.session_state.tts_enabled:
            with st.spinner("🔊 Generating audio..."):
                audio_bytes = tts_bytes(response_text)
                if audio_bytes:
                    st.audio(io.BytesIO(audio_bytes), format="audio/mp3")
                else:
                    st.info("TTS currently unavailable for this response.")
    else:
        # streaming failed; show helpful hint
        if st.session_state.api_error_count > 2:
            st.warning("💡 Multiple errors detected. Please refresh and try again.")
        else:
            st.info("⚠️ Response could not be generated. Try rephrasing your question or try again.")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    # Replace st.toggle with st.checkbox (valid Streamlit API)
    st.session_state.tts_enabled = st.checkbox(
        "🔊 Enable Text-to-Speech",
        value=st.session_state.tts_enabled,
        help="Convert AI responses to audio",
    )

    st.markdown("---")
    st.markdown("### 📚 About")
    st.write("Robin's Business Analytics portfolio with **21 real projects** across 10+ industries.")

    st.markdown("### 📊 Project Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Excel", "6")
        st.metric("Power BI", "5")
    with col2:
        st.metric("SQL", "6")
        st.metric("Python", "4")

    st.markdown("### 🎖️ Key Achievements")
    st.success("✅ 92% Forecasting")
    st.success("✅ 60% VIP Revenue")
    st.success("✅ 28% Risk ID")
    st.success("✅ 10-15% Default Reduction")

    st.markdown("### 🔗 Links")
    st.markdown("[🐙 GitHub](https://github.com/Robi8995)")
    st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")

    st.markdown("### 💡 Sample Questions")
    if st.button("📌 Show Examples"):
        with st.expander("Questions"):
            for q in SAMPLE_QUESTIONS[:5]:
                st.write(f"• {q}")

    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.experimental_rerun()

    st.markdown("---")
    st.caption("Built with ❤️ by Robin | Powered by Groq ⚡")
