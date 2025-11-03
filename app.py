# app_fixed.py
"""
Robin's Portfoli-AI - improved Streamlit app (dark-only theme)
Features:
- Dark mode UI
- Legendary gold accent color
- Project cards with repo links and README reader
- Global TTS toggle (chat replies are voiced)
- Caching for generated audio and LLM responses
- Upload & animate profile image
- Uses robi_context.ROBIN_CONTEXT for system context
"""

import streamlit as st
from datetime import datetime
import io
import hashlib
from gtts import gTTS
from groq import Groq
import time
import base64
import textwrap

# Import expanded context (detailed project descriptions + code snippets)
from robi_context import ROBIN_CONTEXT, PROJECTS_INDEX

# ----------------- Page config -----------------
st.set_page_config(
    page_title="Robin's Portfoli-AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- Styling (dark theme + accent) -----------------
ACCENT_COLOR = "#FFD700"  # legendary gold
DARK_BG = "#0f1115"
CARD_BG = "#111215"
TEXT_COLOR = "#E6EDF3"

_custom_style = f"""
<style>
html, body, .reportview-container, .main {{
    background-color: {DARK_BG};
    color: {TEXT_COLOR};
}}
section.main .block-container {{
    padding-top: 1rem;
    padding-bottom: 2rem;
}}
.stButton>button {{
    border-radius: 8px;
}}
.card {{
    background: linear-gradient(180deg, {CARD_BG}, #0b0c0f);
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.6);
    transition: transform 0.12s ease-in-out;
}}
.card:hover {{ transform: translateY(-6px); }}
.accent {{
    color: {ACCENT_COLOR};
}}
.badge {{
    display:inline-block;
    padding:4px 8px;
    border-radius:6px;
    font-size:12px;
    background: rgba(255,215,0,0.12);
    color: {ACCENT_COLOR};
    margin-right:6px;
}}
.small-muted {{ color: #9aa3b2; font-size:12px; }}
.avatar {{
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    width:120px;
    height:120px;
    object-fit:cover;
    transition: transform 0.6s ease-in-out;
}}
.avatar.animate {{ transform: translateY(-6px) scale(1.03); }}
.speaker {{
    width:28px; height:28px; border-radius:50%;
    display:inline-flex; align-items:center; justify-content:center;
    background: linear-gradient(90deg, rgba(255,215,0,0.18), rgba(255,215,0,0.08));
    color: {ACCENT_COLOR};
}}
.footer-note {{ color:#9aa3b2; font-size:12px; margin-top:10px; }}
</style>
"""
st.markdown(_custom_style, unsafe_allow_html=True)

# ----------------- Helpers -----------------
@st.cache_resource
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY missing in Streamlit secrets. Add it and redeploy.")
        st.stop()
    return Groq(api_key=api_key)

# init client
try:
    groq_client = init_groq()
except Exception as e:
    st.error(f"Unable to init Groq client: {e}")
    st.stop()

# Simple hash util for caching audio / responses
def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# TTS caching (response_text -> bytes)
@st.cache_data(ttl=60 * 60 * 24)  # cache 24h
def generate_tts_bytes(text: str) -> bytes:
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        # propagate as None for caller
        return None

# LLM streaming wrapper (non-blocking mimic)
def generate_llm_response(messages_for_api):
    """
    Use Groq client to send messages and return the assistant text.
    We try streaming; fallback to single response if streaming not available.
    """
    try:
        stream = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages_for_api,
            temperature=0.6,
            max_tokens=1500,
            top_p=0.9,
            stream=True,
            timeout=45
        )
        # collect
        full = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                token = delta.content
                full += token
        return full, None
    except Exception as e:
        # fallback single-call (non-stream)
        try:
            resp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.6,
                max_tokens=1500,
                top_p=0.9,
                stream=False,
                timeout=45
            )
            choice = resp.choices[0].message.content
            return choice, None
        except Exception as e2:
            return None, str(e2)

# Cached LLM wrapper keyed by messages hash
@st.cache_data(ttl=60 * 60)  # cache 1 hour
def cached_llm_response(system_context: str, history: tuple):
    """
    history: tuple of (role, content) items
    """
    messages = [{"role": "system", "content": system_context}]
    for r, c in history:
        messages.append({"role": r, "content": c})
    resp, err = generate_llm_response(messages)
    if err:
        raise RuntimeError(err)
    return resp

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown(f"<h3 style='color:{ACCENT_COLOR}; margin-bottom:4px;'>🤖 Robin's Portfoli-AI</h3>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Your interactive guide to Robin's 21 projects — ask any project, technique, or code snippet.</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Profile upload and animation
    st.markdown("### 👤 Profile")
    uploaded = st.file_uploader("Upload avatar (PNG/GIF) — the app will animate it", type=["png","jpg","jpeg","gif"])
    animate_avatar = st.checkbox("Animate avatar (subtle float)", True)
    if uploaded:
        raw = uploaded.read()
        b64 = base64.b64encode(raw).decode()
        img_html = f"<img src='data:image/jpeg;base64,{b64}' class='avatar {'animate' if animate_avatar else ''}'/>"
        st.markdown(img_html, unsafe_allow_html=True)
        st.caption("Uploaded avatar is previewed above. For best animation use a PNG with transparent background or a short GIF.")
    else:
        # default placeholder avatar (simple colored box)
        placeholder_svg = f"""
        <div style='display:flex;align-items:center;gap:12px'>
            <div style='width:80px;height:80px;border-radius:12px;background:linear-gradient(135deg,#242526,#151516);display:flex;align-items:center;justify-content:center;color:{ACCENT_COLOR};font-weight:600'>
                RJ
            </div>
            <div style='line-height:1'>
                <div style='font-weight:700'>Robin Jimmichan P</div>
                <div class='small-muted'>Bengaluru · Business Analyst</div>
            </div>
        </div>
        """
        st.markdown(placeholder_svg, unsafe_allow_html=True)

    st.markdown("---")
    # Links & contact
    st.markdown("### 🔗 Quick Links")
    st.markdown(f"- GitHub: [Robin-Jimmichan-Pooppally](https://github.com/Robin-Jimmichan-Pooppally)")
    st.markdown(f"- LinkedIn: [Robin](https://{st.session_state.get('linkedin', 'www.linkedin.com/in/robin-jimmichan-pooppally-676061291')})")
    st.markdown(f"- Email: <a href='mailto:rjimmichan@gmail.com' style='color:{ACCENT_COLOR}'>rjimmichan@gmail.com</a>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    # TTS toggle
    if "tts_enabled" not in st.session_state:
        st.session_state.tts_enabled = True  # default on for chat replies
    st.session_state.tts_enabled = st.checkbox("Enable voice replies (TTS)", value=st.session_state.tts_enabled)
    st.markdown("<div class='small-muted'>Voice replies will be generated using Google TTS (cached).</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📚 Projects")
    if st.button("Show all repo links"):
        for p in PROJECTS_INDEX:
            st.markdown(f"- [{p['name']}]({p['repo']})  <span class='small-muted'>({p['category']})</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Built with ❤️ • Dark-only theme • Legendary accent")

# ----------------- Main header -----------------
st.markdown(f"""
<div style='display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px;'>
  <div>
    <h1 style='margin:0;color:{ACCENT_COLOR};'>🤖 Robin's Portfoli-AI</h1>
    <div class='small-muted'>Interactive guide to Robin's 21 end-to-end projects • Ask any project for code, steps, or results</div>
  </div>
  <div style='text-align:right'>
    <div style='font-size:13px;color:#9aa3b2'>Welcome — {datetime.utcnow().strftime("%b %d, %Y • %H:%M UTC")}</div>
    <div style='font-size:12px;color:#9aa3b2'>Voice replies: {'ON' if st.session_state.tts_enabled else 'OFF'}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ----------------- Global chat history state -----------------
if "messages" not in st.session_state:
    # default welcome messages
    st.session_state.messages = [
        {"role": "system", "content": ROBIN_CONTEXT},
        {"role": "assistant", "content": "Hi — I am Robin's Portfoli-AI. Ask me anything about his 21 projects, steps, code, or results. Try: 'Show me the SQL queries used in the Telco Churn project'."}
    ]

# render chat history
for msg in st.session_state.messages[1:]:
    role = msg["role"]
    avatar = "🤖" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

# ----------------- Show Projects Section -----------------
st.markdown("## 📂 Projects — browse and ask")
cols = st.columns([1,1,1,1])

# display project cards grouped by index
def _render_project_card(proj, col):
    with col:
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'>"
                    f"<div><span class='badge'>{proj['category']}</span> <strong class='accent'>{proj['name']}</strong></div>"
                    f"<div><span class='small-muted'>Updated: {proj.get('updated','2025')}</span></div>"
                    f"</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted' style='margin-top:8px'>{proj.get('short','—')}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        # action buttons
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button("🔗 Open Repo", key=f"repo_{proj['id']}"):
                st.experimental_set_query_params(open_repo=proj['repo'])
                st.write(f"[Open repo]({proj['repo']})")
        with col2:
            if st.button("📖 Show README", key=f"readme_{proj['id']}"):
                # If full readme text is in context, display; else show repo link
                content = proj.get("readme_text")
                if content:
                    st.markdown("---")
                    st.markdown(f"### README — {proj['name']}")
                    st.markdown(content)
                    if st.session_state.tts_enabled:
                        audio_bytes = generate_tts_bytes(content)
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.markdown(f"Open repo for README: [link]({proj['repo']})")
        with col3:
            if st.button("💬 Ask about this project", key=f"ask_{proj['id']}"):
                # Pre-fill chat input with project-based question
                prompt = f"Explain the '{proj['name']}' project end-to-end. Include dataset, steps, key queries/code, and business impact. Repo: {proj['repo']}"
                st.session_state.messages.append({"role":"user","content":prompt})
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# render first 8 projects in grid
for i, proj in enumerate(PROJECTS_INDEX[:8]):
    _render_project_card(proj, cols[i % 4])

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ----------------- Chat input -----------------
user_input = st.chat_input("Ask about Robin's projects, code, DAX, SQL or steps...")
if user_input:
    # add to history and show
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)
    # Build minimal history for LLM (we include system context + last 6 messages)
    recent = tuple((m["role"], m["content"]) for m in st.session_state.messages[-6:])
    try:
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            placeholder.markdown("Thinking...")
            # call cached LLM
            assistant_text = cached_llm_response(ROBIN_CONTEXT, recent)
            placeholder.markdown(assistant_text)
            st.session_state.messages.append({"role":"assistant","content":assistant_text})
            # TTS playback
            if st.session_state.tts_enabled:
                audio_bytes = generate_tts_bytes(assistant_text)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("AI request failed: " + str(e))

# ----------------- Footer / complete project list -----------------
st.markdown("---")
st.markdown("<div class='small-muted'>All project READMEs are sourced from Robin's verified GitHub repositories. The assistant uses the full project context to answer code & methodology questions.</div>", unsafe_allow_html=True)
st.markdown("<div class='footer-note'>Tip: For exact SQL/DAX snippets, ask: 'Show me the SQL used in <project name>' or 'Show DAX measures for <Power BI project name>'.</div>", unsafe_allow_html=True)

# ----------------- End -----------------
