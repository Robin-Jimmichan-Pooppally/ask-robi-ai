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
import requests, json, os, re
from urllib.parse import urlparse
from robi_context import context

# ----------------------- Page Config -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# ----------------------- Session Defaults -----------------------
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "history" not in st.session_state: st.session_state.history = []
if "awaiting_clear" not in st.session_state: st.session_state.awaiting_clear = False
if "code_blocks" not in st.session_state: st.session_state.code_blocks = []

# ----------------------- Sticky Header -----------------------
st.markdown("""
<style>
    .sticky-header {
        position: fixed; top: 0; left: 0; width: 100%;
        background-color: #000; z-index: 9999; padding: 0.6rem 0;
        border-bottom: 1px solid #00bfff33;
    }
    .header-title {
        text-align: center; font-size: 22px; font-weight: 600;
        color: #00bfff; text-shadow: 0 0 12px #00bfff;
    }
    .clear-btn-container { position: absolute; top: 8px; right: 20px; }
    .clear-btn {
        background-color:#1e88e5; border:none; color:white;
        padding:5px 10px; border-radius:8px; cursor:pointer; font-weight:500;
        transition: all 0.2s ease-in-out;
    }
    .clear-btn:hover { transform: scale(1.05); box-shadow: 0 0 10px rgba(0,191,255,0.4); }
    .spacer { height: 65px; }
</style>
<div class="sticky-header">
    <div class="header-title">🤖 Portfoli-AI — Robin Jimmichan Pooppally's Portfolio Assistant</div>
    <div class="clear-btn-container">
        <form action="" method="get">
            <button class="clear-btn" name="clear" type="submit">🧹 Clear Chat</button>
        </form>
    </div>
</div>
<div class="spacer"></div>
""", unsafe_allow_html=True)

# ----------------------- Greeting -----------------------
if "greeted" not in st.session_state:
    st.session_state.greeted = False

if not st.session_state.greeted:
    st.markdown("""
    <div style='border-radius:15px;padding:18px;background:rgba(0,191,255,0.08);
    border:1px solid rgba(0,191,255,0.3);box-shadow:0 0 15px rgba(0,191,255,0.4);
    font-family:"Inter",sans-serif;margin-bottom:20px;'>
        <h4 style='color:#00bfff;'>👋 Hey! I’m Portfoli-AI, your portfolio assistant for Robin’s projects.</h4>
        <p style='color:white;'>
        “Ask me about Robin’s projects, skills, or Business Analytics insights.”<br>
        Try saying: <i>"Explain my Telco Churn Dashboard project."</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# ----------------------- Global CSS -----------------------
st.markdown("""
<style>
body { background:#000; color:#e8f7ff; font-size:16px; line-height:1.6; }
h1,h2,h3 { color:#00bfff; text-shadow:0 0 12px #00bfff; }
.section-card {
  background: rgba(10,12,18,0.6);
  border-radius: 14px; padding: 14px;
  border: 1px solid rgba(0,191,255,0.18);
  box-shadow: 0 6px 26px rgba(0,191,255,0.06);
}
.chat-bubble-user,.chat-bubble-bot{padding:10px 14px;border-radius:12px;margin:8px 0;}
.chat-bubble-user{background:rgba(0,191,255,0.12);border:1px solid rgba(0,191,255,0.25);color:#cffcff;}
.chat-bubble-bot{background:rgba(255,255,255,0.04);border:1px solid rgba(0,191,255,0.12);color:#e8f7ff;}
button.stButton>button:hover{transform:scale(1.03);box-shadow:0 0 10px rgba(0,191,255,0.4);}
.code-bubble{background:rgba(3,8,15,0.9);border-left:3px solid #00bfff;padding:10px;margin:8px 0;
border-radius:8px;font-family:monospace;white-space:pre-wrap;overflow-x:auto;}
.small-muted{color:#98cfe6;font-size:12px;text-align:center;margin-top:10px;}
</style>
""", unsafe_allow_html=True)

# ----------------------- Sidebar -----------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/4712/4712102.png", width=80)
st.sidebar.markdown("### 🤖 Built by Robin Jimmichan Pooppally")

# Controls
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### ⚙️ Controls")
tts_sidebar = st.sidebar.checkbox("🔊 Play responses (TTS)", key="tts_sidebar", value=False)
if st.sidebar.button("🧹 Clear Chat History"): st.session_state.history, st.session_state.messages, st.session_state.chat_history = [], [], []
if st.sidebar.button("💾 Save Chat History"):
    history_json = json.dumps(st.session_state.get("history", []), indent=2)
    st.sidebar.download_button("Download JSON", history_json, "chat_history.json", "application/json")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Portfolio
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📊 Portfolio Overview")
summary = context.get("summary", {})
for k, v in summary.items():
    st.sidebar.markdown(f"- **{k}**: {v}")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Contact
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📬 Contact")
st.sidebar.markdown("- Email: [rjimmichan@gmail.com](mailto:rjimmichan@gmail.com)")
st.sidebar.markdown("- [LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
st.sidebar.markdown("- [GitHub](https://github.com/Robin-Jimmichan-Pooppally)")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ----------------------- Functions -----------------------
def build_system_prompt(chat_mode, selected_project=None):
    base_prompt = f"""
    You are {context.get('assistant_name','Portfoli-AI')}, a helpful AI assistant for {context.get('owner_name','the user')}'s portfolio.
    """
    if chat_mode == "Business Analytics Assistant":
        base_prompt += "Focus on data analysis, visualization, and business insights."
    else:
        base_prompt += "Assist professionally and conversationally about the portfolio."
    if selected_project:
        for cat, projs in context.get("projects", {}).items():
            for name, url in projs.items():
                if url == selected_project:
                    base_prompt += f"Currently discussing {name} in {cat}."
                    break
    return base_prompt.strip()

def init_groq():
    key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    if not key: st.error("Missing Groq API key."); st.stop()
    return Groq(api_key=key)

def extract_owner_repo(url):
    parts = urlparse(url).path.strip("/").split("/")
    return (parts[0], parts[1]) if len(parts)>=2 else (None,None)

def fetch_readme_lines(repo_url, max_lines=20):
    owner, repo = extract_owner_repo(repo_url)
    for branch in ("main", "master"):
        try:
            u=f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
            r=requests.get(u,timeout=8)
            if r.status_code==200: lines=r.text.splitlines();return "\n".join(lines[:max_lines]),r.text
        except: continue
    return None,None

def extract_code_blocks_from_readme(text):
    if not text: return []
    pat=re.compile(r"```([\w\-\+]+)?\n(.*?)```",re.DOTALL|re.IGNORECASE)
    return [{"lang":(m.group(1) or '').strip().lower(),"code":m.group(2).rstrip()} for m in pat.finditer(text)]

def speak_text(txt):
    try: buf=BytesIO(); gTTS(text=txt,lang="en").write_to_fp(buf); buf.seek(0); st.audio(buf.read(),format="audio/mp3")
    except Exception as e: st.warning("TTS unavailable: "+str(e))

# ----------------------- Chat + Portfolio UI -----------------------
client = init_groq()
projects_by_cat = context.get("projects", {})
all_projects = [(c,p,r) for c,d in projects_by_cat.items() for p,r in d.items()]

st.markdown("### 🔎 Filter by category")
cols = st.columns(4)
ordered = [c for c in ["Excel","Power BI","Python","SQL"] if c in projects_by_cat] or list(projects_by_cat)
for i,cat in enumerate(ordered):
    if cols[i%4].button(cat): st.session_state["selected_category"]=cat
selected_cat=st.session_state.get("selected_category","All")
project_choices=[f"{c} — {p}" for c,p,r in all_projects if selected_cat in ("All",c)]
project_choice=st.selectbox("Choose a project",["(none)"]+project_choices)

if project_choice!="(none)":
    cat,pname=project_choice.split(" — ",1)
    repo=[r for c,n,r in all_projects if c==cat and n==pname][0]
    if st.session_state.get("selected_project")!=repo:
        st.session_state.selected_project=repo
        st.session_state.readme_preview,st.session_state.readme_full=fetch_readme_lines(repo)
        st.session_state.code_blocks=extract_code_blocks_from_readme(st.session_state.readme_full)

if st.session_state.get("selected_project"):
    st.markdown("<div class='section-card'>",unsafe_allow_html=True)
    st.markdown(f"### 📁 {pname}")
    st.markdown(f"**Category:** {cat}")
    st.markdown(f"🔗 [Repo]({repo})")
    if st.session_state.get("readme_preview"):
        st.markdown("---"); st.code(st.session_state["readme_preview"],language="markdown")
    st.markdown("</div>",unsafe_allow_html=True)

# ----------------------- Chat Logic -----------------------
for m in st.session_state.history:
    html=f"<div class='chat-bubble-{'user' if m['role']=='user' else 'bot'}'><b>{'You' if m['role']=='user' else 'Portfoli-AI'}:</b> {m['content']}</div>"
    st.markdown(html,unsafe_allow_html=True)

tts_toggle=st.session_state.get("tts_sidebar",False)
user_input=st.chat_input("Type your message and press Enter...")

if user_input:
    st.session_state.history.append({"role":"user","content":user_input})
    st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {user_input}</div>",unsafe_allow_html=True)
    sys=build_system_prompt("Business Analytics Assistant",st.session_state.get("selected_project"))
    msgs=[{"role":"system","content":sys}]+st.session_state.history[-8:]
    try:
        res=client.chat.completions.create(model="llama-3.3-70b-versatile",messages=msgs,temperature=0.25,max_tokens=800)
        bot=res.choices[0].message.content.strip()
    except Exception as e: bot=f"⚠️ Groq API error: {e}"
    st.markdown(f"<div class='chat-bubble-bot'><b>Portfoli-AI:</b> {bot}</div>",unsafe_allow_html=True)
    st.session_state.history.append({"role":"assistant","content":bot})
    if tts_toggle: speak_text(bot)
    st.markdown("<script>window.scrollTo(0,document.body.scrollHeight);</script>",unsafe_allow_html=True)

# ----------------------- Footer -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Powered by Groq & Streamlit • © Portfoli-AI</div>", unsafe_allow_html=True)
