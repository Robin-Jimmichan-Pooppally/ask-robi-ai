# app_fixed.py
"""
Robin's Portfoli-AI (app_fixed.py)
Dark + Neon Blue themed Streamlit chatbot for Robin Jimmichan P's 21 projects.
Features:
- Chat UI powered by Groq (optional - requires GROQ_API_KEY in Streamlit secrets)
- TTS (Google gTTS) with caching
- Dark theme + neon accent, animated avatar support
- Project cards linking to GitHub repos and runtime README fetching (raw URLs)
- Safe behavior: displays README & code fetched from GitHub raw URLs (no hallucinated code)
"""
import streamlit as st
from datetime import datetime
import io, hashlib, base64, requests, time
from gtts import gTTS
from pathlib import Path
from typing import Optional

# Import the context and project index
from robi_context import ROBIN_CONTEXT, PROJECTS_INDEX

# ---------- Page config ----------
st.set_page_config(page_title="Robin's Portfoli-AI",
                   page_icon="🤖",
                   layout="wide",
                   initial_sidebar_state="expanded")

# ---------- Styling ----------
ACCENT = "#00D0FF"  # Neon blue accent
DARK_BG = "#0b0f14"
CARD_BG = "#0f1317"
TEXT = "#e6eef3"

st.markdown(f"""
<style>
/* App background */
.reportview-container, .main {{
  background-color: {DARK_BG};
  color: {TEXT};
}}
section.main .block-container {{
  max-width: 1200px;
  padding-top: 16px;
  padding-bottom: 40px;
}}
h1,h2,h3,h4,h5 {{ color: {ACCENT}; text-shadow: 0 0 10px rgba(0,208,255,0.12); }}
.card {{
  background: linear-gradient(180deg, {CARD_BG}, #07090b);
  border-radius: 12px;
  padding: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  transition: transform .12s ease-in-out, box-shadow .12s ease-in-out;
}}
.card:hover {{ transform: translateY(-6px); box-shadow: 0 14px 40px rgba(0,208,255,0.06); }}
.badge {{
  display:inline-block;
  padding:4px 8px;
  border-radius:6px;
  font-size:12px;
  background: rgba(0,208,255,0.06);
  color: {ACCENT};
  margin-right:6px;
}}
.small-muted {{ color: #93a1aa; font-size:13px; }}
.avatar {{
  border-radius:12px;
  width:120px;height:120px;object-fit:cover;
  box-shadow: 0 8px 24px rgba(0,0,0,0.6);
}}
.audio-btn {{
  background: rgba(0,208,255,0.06);
  border-radius: 8px; padding:6px 8px; color:{ACCENT};
}}
footer {{visibility:hidden;}} /* hide streamlit footer */
</style>
""", unsafe_allow_html=True)

# ---------- Helpers ----------
def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

@st.cache_data(ttl=60*60*24)
def generate_tts_bytes(text: str) -> Optional[bytes]:
    """Generate TTS audio bytes for text and cache them."""
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        st.error(f"TTS generation failed: {e}")
        return None

def fetch_raw_url(url: str, timeout=10) -> Optional[str]:
    """Fetch raw text from a URL (GitHub raw README or code). Returns str or None."""
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return r.text
        else:
            return None
    except Exception:
        return None

# Minimal Groq client initializer (lazy - optional usage)
def get_groq_client():
    try:
        from groq import Groq
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None

groq_client = get_groq_client()

def call_groq_chat(system_prompt: str, messages: list):
    """Call Groq chat completions - streaming or non-streaming.
       Returns (response_text, error_str_or_None)."""
    if groq_client is None:
        return None, "GROQ client not configured (set GROQ_API_KEY in Streamlit secrets)."
    try:
        # Build messages
        msgs = [{"role":"system","content":system_prompt}]
        for m in messages:
            msgs.append({"role":m["role"], "content":m["content"]})
        # try streaming
        stream = groq_client.chat.completions.create(model="llama-3.3-70b-versatile",
                                                    messages=msgs, temperature=0.6, max_tokens=1500,
                                                    top_p=0.9, stream=True, timeout=60)
        text = ""
        for chunk in stream:
            delta = chunk.choices[0].delta
            if getattr(delta, "content", None):
                text += delta.content
        return text, None
    except Exception as e:
        # fallback single call
        try:
            resp = groq_client.chat.completions.create(model="llama-3.3-70b-versatile",
                                                       messages=msgs, temperature=0.6, max_tokens=1500,
                                                       top_p=0.9, stream=False, timeout=60)
            return resp.choices[0].message.content, None
        except Exception as e2:
            return None, str(e2)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(f"<h3 style='color:{ACCENT};margin-bottom:4px;'>🤖 Robin's Portfoli-AI</h3>", unsafe_allow_html=True)
    st.markdown("<div class='small-muted'>Interactive guide to Robin's 21 projects — exact READMEs and code pulled from your GitHub.</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👤 Profile")
    uploaded = st.file_uploader("Upload avatar (PNG/GIF) — will preview here", type=["png","jpg","jpeg","gif"])
    if uploaded:
        raw = uploaded.read()
        b64 = base64.b64encode(raw).decode()
        st.markdown(f"<img src='data:image/png;base64,{b64}' class='avatar'/>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='display:flex;gap:10px;align-items:center'><div style='width:72px;height:72px;border-radius:12px;background:linear-gradient(135deg,#081018,#0d1216);display:flex;align-items:center;justify-content:center;color:{ACCENT};font-weight:700'>RJ</div><div><strong>Robin Jimmichan P</strong><div class='small-muted'>Bengaluru · Business Analyst</div></div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔗 Links")
    st.markdown(f"- GitHub: [Robin-Jimmichan-Pooppally](https://github.com/Robin-Jimmichan-Pooppally)")
    st.markdown(f"- LinkedIn: [Robin](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
    st.markdown(f"- Email: <a href='mailto:rjimmichan@gmail.com' style='color:{ACCENT}'>{'rjimmichan@gmail.com'}</a>", unsafe_allow_html=True)
    st.markdown("---")
    # TTS toggle
    if "tts_enabled" not in st.session_state:
        st.session_state.tts_enabled = True
    st.session_state.tts_enabled = st.checkbox("Enable voice replies (TTS)", value=st.session_state.tts_enabled)
    st.markdown("<div class='small-muted'>Voice replies use Google TTS and are cached locally.</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📚 Projects")
    if st.button("Show all repo links"):
        for p in PROJECTS_INDEX:
            st.markdown(f"- [{p['name']}]({p['repo']})  <span class='small-muted'>({p['category']})</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Built with ❤️ — Dark + Neon Blue theme")

# ---------- Header ----------
st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;">
  <div>
    <h1 style="margin:0;color:{ACCENT}">🤖 Robin's Portfoli-AI</h1>
    <div class='small-muted'>Ask about projects, steps, SQL, DAX, Excel formulas, or view exact README files from GitHub.</div>
  </div>
  <div style="text-align:right">
    <div class='small-muted'>UTC {datetime.utcnow().strftime('%b %d, %Y • %H:%M')}</div>
    <div class='small-muted'>Voice replies: {'ON' if st.session_state.tts_enabled else 'OFF'}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ---------- Initialize chat state ----------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role":"system", "content": ROBIN_CONTEXT},
        {"role":"assistant", "content":"Hi — I'm Robin's Portfoli-AI. Ask me about any project, show me SQL/DAX/exact README, or ask for step-by-step methodology."}
    ]

# Show history
for m in st.session_state.messages[1:]:
    with st.chat_message(m["role"], avatar="🤖" if m["role"]=="assistant" else "👤"):
        st.markdown(m["content"])

# ---------- Projects grid ----------
st.markdown("## 📂 Projects")
cols = st.columns(4)
def render_proj_card(proj, column):
    with column:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div style='display:flex;justify-content:space-between;align-items:center'><div><span class='badge'>{proj['category']}</span> <strong style='color:{ACCENT}'>{proj['name']}</strong></div><div class='small-muted'>{proj.get('updated','2025')}</div></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='small-muted' style='margin-top:8px'>{proj.get('short','—')}</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,1])
        with c1:
            if st.button("🔗 Open Repo", key=f"repo_{proj['id']}"):
                st.write(f"[Open repo]({proj['repo']})")
        with c2:
            if st.button("📖 Show README", key=f"readme_{proj['id']}"):
                content = fetch_raw_url(proj.get("readme_url"))
                if content:
                    st.markdown("---")
                    st.markdown(f"### README — {proj['name']}")
                    st.markdown(content)
                    # TTS option
                    if st.session_state.tts_enabled:
                        audio_bytes = generate_tts_bytes(content[:2500])  # avoid too long
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.warning("README not found at expected raw URL. Open repository link to inspect.")
        with c3:
            if st.button("💬 Ask about this project", key=f"ask_{proj['id']}"):
                # pre-fill question
                prompt = f"Explain the '{proj['name']}' project end-to-end. Include dataset, steps, key queries/code location (repo: {proj['repo']}), and business impact."
                st.session_state.messages.append({"role":"user","content":prompt})
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Render projects in rows
for i, p in enumerate(PROJECTS_INDEX):
    render_proj_card(p, cols[i % 4])

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ---------- Chat input ----------
user_input = st.chat_input("Ask about Robin's projects, SQL, DAX, Excel formulas, or request a README...")
if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # Prepare recent history and call Groq if available
    recent = st.session_state.messages[-6:]
    try:
        with st.chat_message("assistant", avatar="🤖"):
            placeholder = st.empty()
            placeholder.markdown("Thinking...")

            if groq_client:
                # call groq
                response_text, err = call_groq_chat(ROBIN_CONTEXT, recent)
                if err:
                    placeholder.error("LLM call failed: " + err)
                    # fallback local assistant-style reply using context (short)
                    reply = "I couldn't reach the LLM — I can still fetch READMEs and show code from your GitHub repos. Try 'Show README for <project name>'."
                    st.session_state.messages.append({"role":"assistant","content":reply})
                    placeholder.markdown(reply)
                else:
                    st.session_state.messages.append({"role":"assistant","content":response_text})
                    placeholder.markdown(response_text)
                    if st.session_state.tts_enabled:
                        audio_bytes = generate_tts_bytes(response_text[:3000])
                        if audio_bytes:
                            st.audio(audio_bytes, format="audio/mp3")
            else:
                # Groq not configured
                placeholder.info("Groq LLM not configured. Set GROQ_API_KEY in Streamlit secrets to enable chat. Meanwhile, I can fetch READMEs & code from GitHub.")
                st.session_state.messages.append({"role":"assistant","content":"Groq not configured. I can fetch README files and code directly from your GitHub repos — ask 'Show README for <project name>'."})
    except Exception as e:
        st.error("Error while processing your request: " + str(e))

# ---------- Footer ----------
st.markdown("---")
st.markdown("<div class='small-muted'>Tip: For exact SQL/DAX/Excel formulas, click 'Show README' for a project to view the authentic README and code files from that repository. If you want, provide repo branch or path in the PROJECTS_INDEX in robi_context.py.</div>", unsafe_allow_html=True)
