# app_fixed.py
"""
Robin's Portfoli-AI - polished Streamlit app (dark theme + neon accent)
- Uses robi_context.ROBIN_CONTEXT and PROJECTS_INDEX (embedded readmes)
- Groq LLM streaming wrapper with caching
- Google TTS for voice replies (cached)
- Dark + Neon Blue UI with animated avatar placeholder
- Quick README viewer & ask-about-project prefill
"""

import streamlit as st
from datetime import datetime
import io
import hashlib
from gtts import gTTS
from groq import Groq
import base64
import time

# import local context (must be present in same folder)
from robi_context import ROBIN_CONTEXT, PROJECTS_INDEX

# ----------------- Page config -----------------
st.set_page_config(
    page_title="Robin's Portfoli-AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------- Styling -----------------
ACCENT = "#00E5FF"  # neon blue accent (you asked neon blue)
DARK_BG = "#0B0F13"
CARD_BG = "#0f1418"
TEXT = "#E6EEF3"

st.markdown(f"""
<style>
/* App background */
body, .stApp, .main {{
  background: linear-gradient(180deg, {DARK_BG}, #071018);
  color: {TEXT};
  font-family: "Inter", "Segoe UI", system-ui, -apple-system, "Helvetica Neue", Arial;
}}
h1, h2, h3, h4 {{
  color: {ACCENT} !important;
  text-shadow: 0 0 12px rgba(0,229,255,0.12);
}}

/* Card */
.card {{
  background: linear-gradient(180deg, {CARD_BG}, #091014);
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  border: 1px solid rgba(0,229,255,0.06);
}}

/* Buttons */
.stButton>button {{
  background: transparent;
  color: {ACCENT};
  border: 1px solid rgba(0,229,255,0.18);
  padding: 6px 12px;
  border-radius: 8px;
}}
.stButton>button:hover {{
  background: {ACCENT};
  color: #001218;
  box-shadow: 0 0 24px rgba(0,229,255,0.12);
}}

/* Inputs */
input, textarea {{
  background: #071018 !important;
  color: {TEXT} !important;
  border: 1px solid rgba(0,229,255,0.08) !important;
  border-radius: 6px !important;
}}

/* Audio shadow */
audio {{
  filter: drop-shadow(0 0 8px {ACCENT});
}}

/* small muted */
.small-muted {{
  color: #9aa3b2;
  font-size: 12px;
}}

/* avatar */
.avatar {{
  width:96px; height:96px; border-radius:14px; object-fit:cover;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6); border: 1px solid rgba(0,229,255,0.08);
}}

/* footer */
footer {{visibility:hidden}}
</style>
""", unsafe_allow_html=True)

# ----------------- Helpers -----------------
@st.cache_resource
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY")
    if not api_key:
        st.error("GROQ_API_KEY missing in Streamlit secrets. Add it and redeploy.")
        st.stop()
    return Groq(api_key=api_key)

try:
    groq_client = init_groq()
except Exception as e:
    st.error(f"Groq init error: {e}")
    st.stop()

def _hash_text(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()

@st.cache_data(ttl=24*3600)
def tts_bytes(text: str):
    try:
        fp = io.BytesIO()
        tts = gTTS(text=text, lang="en", slow=False)
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception:
        return None

def groq_stream_response(messages):
    """Attempt streaming via Groq; fallback to single-response"""
    try:
        stream = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.6,
            max_tokens=1500,
            top_p=0.9,
            stream=True,
            timeout=45
        )
        text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                token = delta.content
                text += token
        return text, None
    except Exception as e:
        try:
            resp = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.6,
                max_tokens=1500,
                top_p=0.9,
                stream=False,
                timeout=45
            )
            return resp.choices[0].message.content, None
        except Exception as e2:
            return None, str(e2)

@st.cache_data(ttl=60*60)
def cached_ai(system_context: str, history_tuple):
    messages = [{"role":"system","content": system_context}]
    for r,c in history_tuple:
        messages.append({"role": r, "content": c})
    resp, err = groq_stream_response(messages)
    if err:
        raise RuntimeError(err)
    return resp

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown(f"<h3 style='color:{ACCENT}; margin-bottom:6px;'>🤖 Robin's Portfoli-AI</h3>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Interactive guide to Robin's 21 projects — ask for code, steps, or business impact.</div>", unsafe_allow_html=True)
    st.markdown("---")

    # Avatar
    uploaded = st.file_uploader("Upload avatar (optional, PNG/JPG/GIF)", type=["png","jpg","jpeg","gif"])
    if uploaded:
        raw = uploaded.read()
        b64 = base64.b64encode(raw).decode()
        st.markdown(f"<img src='data:image;base64,{b64}' class='avatar'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display:flex;align-items:center;gap:12px'><div style='width:72px;height:72px;border-radius:12px;background:{ACCENT};display:flex;align-items:center;justify-content:center;font-weight:700;color:#001218'>RJ</div><div><strong>Robin Jimmichan P</strong><div class='small-muted'>Bengaluru · Business Analyst</div></div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔗 Quick Links")
    st.markdown("- GitHub: [Robin-Jimmichan-Pooppally](https://github.com/Robin-Jimmichan-Pooppally)")
    st.markdown("- LinkedIn: [Robin](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
    st.markdown("- Email: <a href='mailto:rjimmichan@gmail.com' style='color:inherit'>rjimmichan@gmail.com</a>", unsafe_allow_html=True)
    st.markdown("---")

    if "tts_enabled" not in st.session_state:
        st.session_state.tts_enabled = True
    st.session_state.tts_enabled = st.checkbox("🔊 Enable voice replies", value=st.session_state.tts_enabled)
    st.markdown("<div class='small-muted'>Voice replies are generated and cached (Google TTS).</div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📚 Projects")
    if st.button("Show all repos (open in new tab)"):
        for p in PROJECTS_INDEX:
            st.markdown(f"- [{p['name']}]({p['repo']})  <span class='small-muted'>({p['category']})</span>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Clear chat"):
        st.session_state.messages = None
        st.experimental_rerun()

# ----------------- Main #################
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;">
  <div>
    <h1 style="margin:0;color:{ACCENT};">🤖 Robin's Portfoli-AI</h1>
    <div class="small-muted">“👋 Hey there! I’m Robin’s Portfoli-AI — your interactive portfolio assistant 🚀”</div>
  </div>
  <div style="text-align:right">
    <div class='small-muted'>UTC: {datetime.utcnow().strftime('%b %d, %Y • %H:%M')}</div>
    <div class='small-muted'>Voice replies: {'ON' if st.session_state.tts_enabled else 'OFF'}</div>
  </div>
</div>
<hr style="opacity:0.08"/>
""", unsafe_allow_html=True)

# initialize chat history
if "messages" not in st.session_state or st.session_state.messages is None:
    st.session_state.messages = [
        {"role":"system","content": ROBIN_CONTEXT},
        {"role":"assistant","content":"Hi — I am Robin's Portfoli-AI. Ask me about any project, code snippet, DAX, SQL, or project steps. Try: 'Show me the SQL used in Telco Churn Analysis.'"}
    ]

# render chat messages
for m in st.session_state.messages[1:]:
    with st.chat_message(m["role"], avatar="🤖" if m["role"]=="assistant" else "👤"):
        st.markdown(m["content"])

# Projects grid (first 8)
st.markdown("## 📂 Projects — Browse & read")
cols = st.columns(4)
def render_card(p, col):
    with col:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'><div><strong style='color:{ACCENT}'>{p['name']}</strong> <span class='small-muted'>({p['category']})</span></div><div class='small-muted'>{p.get('updated','2025')}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted' style='margin-top:8px'>{p.get('short','—')}</div>", unsafe_allow_html=True)
        if st.button("📖 Show README", key=f"read_{p['id']}"):
            # show embedded readme if present
            readme = p.get("embedded_readme") or p.get("readme_text") or None
            if readme:
                st.markdown("---")
                st.markdown(readme)
                if st.session_state.tts_enabled:
                    audio = tts_bytes(readme)
                    if audio:
                        st.audio(audio, format="audio/mp3")
            else:
                st.markdown(f"Open the repository for README: [link]({p['repo']})")
        if st.button("💬 Ask about project", key=f"ask_{p['id']}"):
            prompt = f"Explain the '{p['name']}' project end-to-end. Include dataset, steps, key queries/code, and business impact. Repo: {p['repo']}"
            st.session_state.messages.append({"role":"user","content":prompt})
            st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

for i,p in enumerate(PROJECTS_INDEX[:8]):
    render_card(p, cols[i%4])

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# chat input
user_input = st.chat_input("Ask about Robin's projects, code, DAX or steps...")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    recent = tuple((m["role"], m["content"]) for m in st.session_state.messages[-6:])
    try:
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("Thinking...")
            assistant_text = cached_ai(ROBIN_CONTEXT, recent)
            placeholder.markdown(assistant_text)
            st.session_state.messages.append({"role":"assistant","content":assistant_text})
            if st.session_state.tts_enabled:
                audio = tts_bytes(assistant_text)
                if audio:
                    st.audio(audio, format="audio/mp3")
    except Exception as e:
        st.error(f"AI error: {e}")

st.markdown("---")
st.markdown("<div class='small-muted'>Tip: ask for exact SQL/DAX by name — the assistant uses embedded README content (offline) for accuracy.</div>", unsafe_allow_html=True)
