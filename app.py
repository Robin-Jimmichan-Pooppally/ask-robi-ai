# app_fixed.py
"""
Robin's Portfoli-AI - Legendary UI (app_fixed.py)

Place this file next to your robi_context.py (Legendary Edition).
Features:
- Dark + Neon Blue theme
- Local offline assistant (answers from ROBIN_CONTEXT & PROJECTS_INDEX)
- Optional Groq LLM (if GROQ_API_KEY present in st.secrets)
- TTS via gTTS with caching
- Project cards, README display, repo links, avatar upload + animation
"""

import streamlit as st
from datetime import datetime
import io
import base64
import hashlib
import time
from gtts import gTTS
from typing import Optional

# Import your offline context file (must be in same folder)
from robi_context import ROBIN_CONTEXT, PROJECTS as PROJECTS_INDEX, PROJECT_SUMMARY as PROJECTS_SUMMARY_TABLE

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Robin's Portfoli-AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Styling (dark + neon blue) ----------------
NEON = "#00e6ff"
DARK_BG = "#0b0f14"
CARD_BG = "#0f1418"
TEXT = "#E6EEF6"

st.markdown(
    f"""
    <style>
    /* App */
    .stApp {{ background: linear-gradient(180deg, {DARK_BG} 0%, #071018 100%); color: {TEXT}; font-family: 'Inter', sans-serif; }}
    /* Header */
    .header-title {{ color: {NEON}; font-weight: 800; text-shadow: 0 0 12px rgba(0,230,255,0.15); }}
    .small-muted {{ color: #9aa3b2; font-size:12px; }}
    /* Cards */
    .card {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.12));
        border-radius:12px; padding:14px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    }}
    .card:hover {{ transform: translateY(-6px); transition: all 0.15s ease-in-out; box-shadow: 0 14px 40px rgba(0,0,0,0.7); }}
    .accent {{ color: {NEON}; font-weight:700; }}
    .badge {{ display:inline-block; padding:6px 10px; border-radius:8px; font-size:12px; background: rgba(0,230,255,0.06); color:{NEON}; margin-right:8px; }}
    /* Buttons */
    div.stButton > button {{
        background: transparent; color: {NEON}; border: 1px solid {NEON}; border-radius:8px; padding:6px 10px;
    }}
    div.stButton > button:hover {{ background: {NEON}; color: #001216; box-shadow: 0 0 20px rgba(0,230,255,0.14); }}
    /* Chat bubbles */
    .stChatMessage {{}}
    /* Avatar */
    .avatar {{ border-radius:12px; width:110px; height:110px; object-fit:cover; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }}
    .avatar.float {{ animation: floaty 4s ease-in-out infinite; }}
    @keyframes floaty {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-6px); }}
        100% {{ transform: translateY(0px); }}
    }}
    /* Hide footer */
    footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Utilities ----------------
def _hash_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

@st.cache_data(ttl=60*60*24)
def generate_tts_bytes(text: str) -> Optional[bytes]:
    """Generate and cache TTS audio bytes for a text using gTTS."""
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        # return None on failure (e.g., missing network)
        return None

# ---------------- Optional Groq client init (if user wants live LLM) ----------------
@st.cache_resource
def init_groq_client():
    try:
        from groq import Groq
        api_key = st.secrets.get("GROQ_API_KEY")
        if api_key:
            return Groq(api_key=api_key)
        return None
    except Exception:
        return None

groq_client = init_groq_client()

def call_groq_chat(messages):
    """Call Groq chat completions if client present. Returns (text, error_str)."""
    if not groq_client:
        return None, "Groq client not configured"
    try:
        # Try streaming if supported; otherwise fallback to single response
        stream = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6,
            max_tokens=1200,
            top_p=0.9,
            stream=False,
            timeout=45
        )
        # expected structure may vary; adapt
        content = stream.choices[0].message.content
        return content, None
    except Exception as e:
        return None, str(e)

# ---------------- Offline assistant (safe, no hallucination) ----------------
def local_assistant_answer(prompt: str) -> str:
    """
    Lightweight local assistant:
    - If user asks about a specific project name, return its embedded_readme.
    - Otherwise return a guided summary from ROBIN_CONTEXT and suggestions.
    """
    p = prompt.lower().strip()
    # check for exact project names or keywords
    for proj in PROJECTS_INDEX:
        name = proj["name"].lower()
        short = proj.get("short","").lower()
        if proj["name"].lower() in p or proj["id"].lower() in p or any(tok in p for tok in name.split()):
            # Return embedded_readme if present
            content = proj.get("embedded_readme") or proj.get("readme_text") or proj.get("short") or ""
            header = f"### {proj['name']} — Summary & Key Snippets\n\n"
            repo_line = f"Repository: {proj['repo']}\n\n"
            return header + repo_line + (content if content else "(No embedded README; open repo link above.)")
    # If prompt asks generally, return intro + instructions
    base = "🤖 Hi — I'm Robin's Portfoli-AI. I can explain any of Robin's 21 projects end-to-end, show code snippets (SQL, DAX, Python), or open READMEs.\n\n"
    base += "Quick suggestions:\n- Ask: `Show me the SQL used in Telco Churn Analysis`\n- Ask: `Show DAX measures for Retail Sales Dashboard`\n- Ask: `Explain the ARIMA forecasting steps in the Sales Forecasting project`\n\n"
    base += "Contact / Links:\n- GitHub: https://github.com/Robin-Jimmichan-Pooppally\n- LinkedIn: https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291\n- Email: rjimmichan@gmail.com\n\n"
    base += "If you'd like a live AI answer (LLM), add GROQ_API_KEY to Streamlit Secrets and the app will use Groq Llama 3.3."
    return base

# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown(f"<h3 class='header-title'>🤖 Robin's Portfoli-AI</h3>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Interactive portfolio assistant — ask for code, methodology, results.</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Avatar upload
    st.markdown("### 👤 Profile")
    uploaded = st.file_uploader("Upload avatar (PNG/JPG/GIF)", type=["png","jpg","jpeg","gif"])
    animate = st.checkbox("Animate avatar (float)", True)
    if uploaded:
        raw = uploaded.read()
        b64 = base64.b64encode(raw).decode()
        cls = "avatar float" if animate else "avatar"
        st.markdown(f"<img src='data:image;base64,{b64}' class='{cls}'/>", unsafe_allow_html=True)
        st.caption("Uploaded avatar preview.")
    else:
        # placeholder
        placeholder_avatar = f"""
        <div style='display:flex;gap:12px;align-items:center'>
          <div style='width:96px;height:96px;border-radius:12px;background:linear-gradient(135deg,#022430,#003a4a);display:flex;align-items:center;justify-content:center;color:{NEON};font-weight:700;font-size:22px'>RJ</div>
          <div>
            <div style='font-weight:700'>Robin Jimmichan P</div>
            <div class='small-muted'>Bengaluru · Business Analyst</div>
          </div>
        </div>
        """
        st.markdown(placeholder_avatar, unsafe_allow_html=True)

    st.markdown("---")
    # Links
    st.markdown("### 🔗 Quick Links")
    st.markdown(f"- GitHub: [Robin-Jimmichan-Pooppally](https://github.com/Robin-Jimmichan-Pooppally)")
    st.markdown(f"- LinkedIn: [Robin](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
    st.markdown(f"- Email: <a href='mailto:rjimmichan@gmail.com' style='color:{NEON}'>rjimmichan@gmail.com</a>", unsafe_allow_html=True)

    st.markdown("---")
    # TTS toggle
    if "tts_enabled" not in st.session_state:
        st.session_state.tts_enabled = True
    st.session_state.tts_enabled = st.checkbox("Enable voice replies (TTS)", value=st.session_state.tts_enabled)
    st.markdown("<div class='small-muted'>Voice replies are generated & cached with Google TTS. Audio generation may take a few seconds.</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📚 Projects")
    if st.button("Show all repo links"):
        for proj in PROJECTS_INDEX:
            st.markdown(f"- [{proj['name']}]({proj['repo']})  <span class='small-muted'>({proj['category']})</span>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Clear Chat"):
        st.session_state.pop("messages", None)
        st.experimental_rerun()

    st.caption("Built with ❤️ • Dark + Neon Blue • Portfoli-AI Legendary")

# ---------------- Main header ----------------
st.markdown(
    f"""
    <div style='display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:12px;'>
      <div>
        <h1 class='header-title' style='margin:0'>🤖 Welcome to Portfoli-AI — I’m Robin’s intelligent portfolio assistant 🚀</h1>
        <div class='small-muted'>Ask me about any of Robin's 21 projects, steps, or exact code snippets (SQL, DAX, Python, Excel).</div>
      </div>
      <div style='text-align:right'>
        <div class='small-muted'>{datetime.utcnow().strftime('%b %d, %Y • %H:%M UTC')}</div>
        <div style='font-size:12px;color:#9aa3b2'>Voice replies: {'ON' if st.session_state.tts_enabled else 'OFF'}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------- Chat history initialization ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": ROBIN_CONTEXT},
        {"role": "assistant", "content": "Hi — I am Robin's Portfoli-AI. Try: 'Show me the SQL used in Telco Churn Analysis' or 'Show DAX for Retail Sales Dashboard'."}
    ]

# Render existing messages
for m in st.session_state.messages[1:]:
    role = m["role"]
    avatar = "🤖" if role == "assistant" else "👤"
    with st.chat_message(role, avatar=avatar):
        st.markdown(m["content"])

# ---------------- Projects grid ----------------
st.markdown("## 📂 Projects — browse & ask")
cols = st.columns(4)
for i, proj in enumerate(PROJECTS_INDEX[:12]):  # show first 12 for speed; rest available via sidebar
    col = cols[i % 4]
    with col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div><span class='badge'>{proj['category']}</span> <span class='accent'>{proj['name']}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted' style='margin-top:8px'>{proj.get('short','—')}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("🔗 Open Repo", key=f"open_{proj['id']}"):
                st.experimental_set_query_params(repo=proj['repo'])
                st.write(f"[Open repository]({proj['repo']})")
        with c2:
            if st.button("📖 Show README", key=f"read_{proj['id']}"):
                st.markdown("---")
                readme_text = proj.get("embedded_readme") or proj.get("short") or f"Open repo: {proj['repo']}"
                st.markdown(f"### README — {proj['name']}")
                st.markdown(readme_text)
                if st.session_state.tts_enabled:
                    audio = generate_tts_bytes(readme_text)
                    if audio:
                        st.audio(audio, format="audio/mp3")
        with c3:
            if st.button("💬 Ask about this project", key=f"ask_{proj['id']}"):
                # Prefill a user question and rerun to trigger chat flow
                prompt = f"Explain the '{proj['name']}' project end-to-end. Include dataset, steps, key queries/code, and business impact. Repo: {proj['repo']}"
                st.session_state.messages.append({"role":"user","content":prompt})
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

# ---------------- Chat input handling ----------------
user_input = st.chat_input("Ask about Robin's projects, code (SQL/DAX/Python), or steps...")
if user_input:
    # append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Build assistant reply: prefer Groq if configured, else local assistant
    # Build minimal messages (system + last few)
    try:
        # Attempt Groq if available
        if groq_client:
            # Create messages list for Groq
            msgs = [{"role":"system","content":ROBIN_CONTEXT}]
            # include last 6 messages from history
            for m in st.session_state.messages[-6:]:
                msgs.append({"role": m["role"], "content": m["content"]})
            # call groq
            assistant_text, err = call_groq_chat(msgs)
            if err or not assistant_text:
                # fallback to local
                assistant_text = local_assistant_answer(user_input)
            # display response
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(assistant_text)
            st.session_state.messages.append({"role":"assistant","content":assistant_text})
            # TTS
            if st.session_state.tts_enabled:
                audio_bytes = generate_tts_bytes(assistant_text)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
        else:
            # no groq => local assistant
            assistant_text = local_assistant_answer(user_input)
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(assistant_text)
            st.session_state.messages.append({"role":"assistant","content":assistant_text})
            if st.session_state.tts_enabled:
                audio_bytes = generate_tts_bytes(assistant_text)
                if audio_bytes:
                    st.audio(audio_bytes, format="audio/mp3")
    except Exception as e:
        st.error("Assistant error: " + str(e))

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("<div class='small-muted'>Tip: For exact SQL/DAX snippets, ask: 'Show me the SQL used in <project name>' or 'Show DAX measures for <Power BI project name>'.</div>", unsafe_allow_html=True)
st.markdown("<div class='small-muted'>This app works offline using the embedded `robi_context.py`. Add GROQ_API_KEY in Streamlit Secrets to enable live LLM responses.</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-top:8px;color:#9aa3b2;font-size:12px'>Built with ❤️ by Robin • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
