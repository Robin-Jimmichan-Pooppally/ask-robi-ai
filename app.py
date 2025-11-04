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
import re
from urllib.parse import urlparse

# Import your verified context (must match what we finalized)
from robi_context import context

# -----------------------
# Helper: build system prompt
# -----------------------
def build_system_prompt(chat_mode, selected_project=None):
    """
    Build the system prompt based on chat mode and selected project.
    """
    base_prompt = f"""
    You are {context.get('assistant_name', 'Portfoli-AI')}, a helpful AI assistant for {context.get('owner_name', 'the user')}'s portfolio.
    {context.get('owner_name', 'The user')} is a {context.get('owner_role', 'professional')}.
    """
    if chat_mode == "Business Analytics Assistant":
        base_prompt += """
        You are in Business Analytics Assistant mode. Focus on providing insights, analysis, and explanations
        related to data analytics, visualization, and business intelligence.
        """
    else:
        base_prompt += """
        You are in General Assistant mode. You can discuss a wide range of topics but maintain a professional tone.
        """
    if selected_project:
        project_name = "the selected project"
        project_category = None
        for cat, projs in context.get("projects", {}).items():
            for name, url in projs.items():
                if url == selected_project:
                    project_name = name
                    project_category = cat
                    break
        base_prompt += f"""
        The user is currently looking at their project: {project_name}
        Category: {project_category or 'Not specified'}
        Repository: {selected_project}
        """
    base_prompt += """
    Guidelines:
    - Be concise but thorough
    - Use markdown
    - Maintain a professional but friendly tone
    """
    return base_prompt.strip()

# -----------------------
# Page config
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# -----------------------
# Session state defaults
# -----------------------
if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "history" not in st.session_state: st.session_state.history = []
if "awaiting_clear" not in st.session_state: st.session_state.awaiting_clear = False
# code blocks parsed from README
if "code_blocks" not in st.session_state: st.session_state.code_blocks = []

# --- Sticky Header ---
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
        .clear-btn-container {
            position: absolute; top: 8px; right: 20px;
        }
        .clear-btn {
            background-color:#1e88e5; border:none; color:white;
            padding:5px 10px; border-radius:8px; cursor:pointer; font-weight:500;
            transition: all 0.2s ease-in-out;
        }
        .clear-btn:hover { transform: scale(1.05); box-shadow: 0 0 10px rgba(0,191,255,0.4); }
        .spacer { height: 65px; }
    </style>
    <div class="sticky-header">
        <div class="header-title">🤖 Portfoli-AI — Robin Jimmichan's Portfolio Assistant</div>
        <div class="clear-btn-container">
            <form action="" method="get">
                <button class="clear-btn" name="clear" type="submit" aria-label="Clear chat">🧹 Clear Chat</button>
            </form>
        </div>
    </div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)

# -----------------------
# Greeting
# -----------------------
if "greeted" not in st.session_state:
    st.session_state.greeted = False

if not st.session_state.greeted:
    st.markdown("""
    <div style='border-radius:15px;padding:18px;background:rgba(0,191,255,0.08);
    border:1px solid rgba(0,191,255,0.3);box-shadow:0 0 15px rgba(0,191,255,0.4);
    font-family:"Inter",sans-serif;margin-bottom:20px;'>
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
# Global CSS (neon + accessibility + selectbox/focus tweak + code bubble)
# -----------------------
st.markdown("""
<style>
body { background:#000; color:#e8f7ff; font-size:16px; line-height:1.6; scroll-behavior:smooth; }
h1,h2,h3 { color:#00bfff; text-shadow:0 0 12px #00bfff; }
.section-card {
  background: rgba(10,12,18,0.6);
  border-radius: 14px; padding: 14px;
  border: 1px solid rgba(0,191,255,0.18);
  box-shadow: 0 6px 26px rgba(0,191,255,0.06);
}
.chat-bubble-user, .chat-bubble-bot {
  padding:10px 14px; border-radius:12px; margin:8px 0;
  transition: background 0.3s ease, transform 0.2s ease;
}
.chat-bubble-user:hover, .chat-bubble-bot:hover { transform: scale(1.02); }
.chat-bubble-user {
  background: rgba(0,191,255,0.12); border: 1px solid rgba(0,191,255,0.25); color:#cffcff;
}
.chat-bubble-bot {
  background: rgba(255,255,255,0.04); border: 1px solid rgba(0,191,255,0.12); color:#e8f7ff;
}
button.stButton>button {
  border-radius:8px; transition: all 0.2s ease-in-out;
}
button.stButton>button:hover {
  transform: scale(1.03);
  box-shadow: 0 0 10px rgba(0,191,255,0.4);
}
/* Category button hover tune (chatbot blue) */
button.stButton>button:hover { outline: 0; box-shadow: 0 0 18px rgba(0,191,255,0.12); border-color: #00bfff; }
/* Selectbox focus / active uses chatbot blue */
.stSelectbox [data-baseweb="select"] { border-color: #00bfff !important; box-shadow: 0 0 14px rgba(0,191,255,0.08) !important; }
/* Selected project label inline display color */
.selected-project-label { color: #00bfff; font-weight:700; }
/* Styled code bubble for README snippets (neon-blue accent) */
.code-bubble {
  background: rgba(3,8,15,0.9);
  border-left: 3px solid #00bfff;
  padding: 10px;
  margin: 8px 0;
  border-radius: 8px;
  font-family: monospace;
  white-space: pre-wrap;
  overflow-x: auto;
}
/* small muted text */
.small-muted { color:#98cfe6; font-size:12px; }
</style>
""", unsafe_allow_html=True)

# Optional high-contrast mode (sidebar toggle)
if st.sidebar.toggle("♿ High Contrast Mode"):
    st.markdown("<style>body{filter:contrast(1.25);}</style>", unsafe_allow_html=True)


# -----------------------
# Sidebar: Controls → Portfolio → Contact (reordered)
# -----------------------
# Controls section (stacked)
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### ⚙️ Controls")
tts_sidebar = st.sidebar.checkbox("🔊 Play responses (TTS)", key="tts_sidebar", value=False)

# Clear Chat History with confirmation
if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.awaiting_clear = True

if st.session_state.get("awaiting_clear", False):
    st.sidebar.warning("Are you sure you want to clear the chat history? This cannot be undone.")
    c1, c2 = st.sidebar.columns(2)
    if c1.button("Yes, clear"):
        st.session_state.history = []
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.awaiting_clear = False
        st.experimental_rerun()
    if c2.button("No, cancel"):
        st.session_state.awaiting_clear = False

# Save Chat History as JSON (download)
if st.sidebar.button("💾 Save Chat History"):
    history_json = json.dumps(st.session_state.get("history", []), indent=2)
    st.sidebar.download_button("Download JSON", history_json, file_name="chat_history.json", mime="application/json")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Portfolio section (stacked)
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown(f"### 👋 {context['owner_name']}")
st.sidebar.markdown(f"**{context['owner_role']}**")
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Portfolio Overview")
summary = context.get("summary", {})
for k, v in summary.items():
    st.sidebar.markdown(f"- **{k}**: {v}")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Contact section (stacked)
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📬 Contact")
st.sidebar.markdown(f"- Email: <a href='mailto:rjimmichan@gmail.com'>rjimmichan@gmail.com</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- LinkedIn: <a href='https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291'>Profile</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- GitHub: <a href='https://github.com/Robin-Jimmichan-Pooppally'>Robin-Jimmichan-Pooppally</a>", unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# (Your existing logic continues below unchanged)
# -----------------------

# Prepare projects list (flattened)
projects_by_cat = context.get("projects", {})
all_projects = []
for cat, d in projects_by_cat.items():
    for pname, repo in d.items():
        all_projects.append((cat, pname, repo))

# Category buttons
st.markdown("### 🔎 Filter by category")
cols = st.columns(4)
cats = list(projects_by_cat.keys())
ordered = [c for c in ["Excel", "Power BI", "Python", "SQL"] if c in cats] or cats
selected_cat = None
for i, cat in enumerate(ordered):
    if cols[i % 4].button(cat):
        selected_cat = cat
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if selected_cat:
    st.session_state.selected_category = selected_cat

if st.session_state.get("selected_category", "All") == "All":
    st.markdown("Showing projects: **All categories**")
else:
    st.markdown(f"Showing projects: <span class='selected-project-label'>**{st.session_state['selected_category']}**</span>", unsafe_allow_html=True)

# Build dropdown project list filtered by the selected category
def build_project_list(filter_cat):
    choices = []
    for cat, pname, repo in all_projects:
        if filter_cat in (None, "All") or cat == filter_cat:
            choices.append(f"{cat} — {pname}")
    return choices

project_choices = build_project_list(st.session_state.get("selected_category", "All"))
if not project_choices:
    st.info("No projects in this category.")
    project_choice = None
else:
    project_choice = st.selectbox("Choose a project to explore", ["(none)"] + project_choices)

# Chat mode toggle
st.markdown("---")
mode = st.radio("Chat mode", ("General Assistant", "Business Analytics Assistant"), horizontal=True)
if "chat_mode" not in st.session_state or st.session_state.get("chat_mode") != mode:
    st.session_state.chat_mode = mode
    st.session_state.history = []

# Groq client
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Missing Groq API key. Add GROQ_API_KEY to Streamlit secrets.")
        st.stop()
    try:
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        st.stop()
client = init_groq()

# -----------------------
# Helper: fetch README (unchanged)
# -----------------------
def extract_owner_repo(repo_url):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None

def fetch_readme_lines(repo_url, max_lines=20):
    owner, repo = extract_owner_repo(repo_url)
    if not owner: return None, "Invalid repo URL"
    raw_main = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
    raw_master = f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    for url in (raw_main, raw_master):
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200 and r.text.strip():
                lines = r.text.splitlines()
                preview = "\n".join(lines[:max_lines])
                full = r.text
                return preview, full
        except Exception:
            continue
    return None, None

# -----------------------
# NEW: Extract fenced code blocks from README using regex (literal match)
# -----------------------
def extract_code_blocks_from_readme(readme_text):
    """
    Returns a list of dicts: { 'lang': 'python'|'sql'|'dax'|..., 'code': '...' }
    Uses a safe regex that matches fenced code blocks like:
    ```python
    ...
    ```
    or ```sql ... ```
    """
    blocks = []
    if not readme_text:
        return blocks
    # Matches ```lang\n...``` (lang optional)
    pattern = re.compile(r"```([\w\-\+]+)?\n(.*?)```", re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(readme_text):
        lang = (m.group(1) or "").strip().lower()
        code = m.group(2).rstrip()
        blocks.append({"lang": lang, "code": code})
    return blocks

# -----------------------
# TTS helper (unchanged)
# -----------------------
def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buf = BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        st.audio(buf.read(), format="audio/mp3")
    except Exception as e:
        st.warning("TTS unavailable: " + str(e))

# -----------------------
# Chat & README sync logic
# -----------------------
if "history" not in st.session_state: st.session_state.history = []
if "selected_project" not in st.session_state: st.session_state.selected_project = None
if "readme_full" not in st.session_state: st.session_state.readme_full = None
if "readme_preview" not in st.session_state: st.session_state.readme_preview = None
if "show_more" not in st.session_state: st.session_state.show_more = False

# When project selection changes -> load README preview and reset chat for that project
if project_choice and project_choice != "(none)":
    cat, pname = project_choice.split(" — ", 1)
    repo_url = None
    for c, name, r in all_projects:
        if c == cat and name == pname:
            repo_url = r
            break
    if st.session_state.get("selected_project") != repo_url:
        st.session_state.selected_project = repo_url
        st.session_state.history = []
        st.session_state.readme_preview, st.session_state.readme_full = fetch_readme_lines(repo_url, max_lines=20)
        # Parse code blocks immediately after fetching README
        st.session_state.code_blocks = extract_code_blocks_from_readme(st.session_state.readme_full)
        st.session_state.show_more = False

# Display selected project card above chat
if st.session_state.get("selected_project"):
    repo_url = st.session_state.selected_project
    card_cat = card_name = None
    for c, name, r in all_projects:
        if r == repo_url:
            card_cat, card_name = c, name
            break
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"### 📁 {card_name}")
    st.markdown(f"**Category:** {card_cat}  ")
    st.markdown(f"🔗 **Repo:** [{repo_url}]({repo_url})")
    if st.session_state.get("readme_preview"):
        st.markdown("---")
        st.markdown("**README preview:**")
        st.code(st.session_state["readme_preview"], language="markdown")
        if st.session_state.get("readme_full"):
            if st.button("Show more" if not st.session_state.show_more else "Show less"):
                st.session_state.show_more = not st.session_state.show_more
            if st.session_state.show_more:
                st.markdown("<details open><summary>Full README</summary>", unsafe_allow_html=True)
                st.code(st.session_state["readme_full"], language="markdown")
                st.markdown("</details>", unsafe_allow_html=True)
    else:
        st.info("No README found for this repository.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Render existing history
for m in st.session_state.history:
    role, text = m.get("role"), m.get("content")
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user' aria-label='User message'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot' aria-label='Assistant message'><b>{context.get('assistant_name','Portfoli-AI')}:</b> {text}</div>", unsafe_allow_html=True)

# -----------------------
# NEW: Chat input using Enter to send (Shift+Enter for newline)
#       and README code/DAX literal extraction before calling Groq
# -----------------------
tts_toggle = st.session_state.get("tts_sidebar", False)

# Use Streamlit chat_input (press Enter to send; Shift+Enter newline)
user_input = st.chat_input("Type your message and press Enter...")

# keywords -> code language mapping for simple detection
code_keyword_map = {
    "dax": ["dax", "measure", "measures", "powerbi", "power bi"],
    "sql": ["sql", "query", "select", "where", "join"],
    "python": ["python", "py", ".py", "script"],
    "m": ["m", "m query", "powerquery", "m-query"],
    "json": ["json"]
}

def detect_requested_lang(user_text):
    u = user_text.lower()
    for lang, keys in code_keyword_map.items():
        for k in keys:
            if k in u:
                return lang
    return None

def find_code_blocks_for_lang(lang):
    """
    Return list of code strings matching lang (or empty list).
    If lang is None, return all code blocks.
    """
    blocks = st.session_state.get("code_blocks", []) or []
    if not lang:
        return blocks
    matches = [b for b in blocks if b.get("lang", "") == lang]
    # also accept common synonyms (e.g., 'powerquery' stored as 'm' or plain)
    if not matches and lang == "m":
        matches = [b for b in blocks if b.get("lang", "") in ("m", "powerquery", "power-query")]
    return matches

if user_input:
    # Append user message to history and display immediately
    st.session_state.history.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='chat-bubble-user' aria-label='User message'><b>You:</b> {user_input}</div>", unsafe_allow_html=True)

    # Check if user asked for code/DAX/SQL/Python literal from README
    requested_lang = detect_requested_lang(user_input)
    code_matches = []
    if requested_lang:
        code_matches = find_code_blocks_for_lang(requested_lang)

    # If user explicitly asked for "show code" and there are matches -> return exact snippets (no Groq)
    if requested_lang and code_matches:
        # Styled code bubble header
        st.markdown(f"<div class='code-bubble'><b>Exact `{requested_lang}` snippet(s) from README:</b>\n\n", unsafe_allow_html=True)
        # Show up to first 5 matches to avoid overwhelming the UI
        for idx, blk in enumerate(code_matches[:5], start=1):
            lang_label = blk.get("lang") or "code"
            code_text = blk.get("code", "")
            # Render code inside markdown triple-backticks inside the styled bubble
            st.markdown(f"<div class='code-bubble'><b>Snippet {idx} — {lang_label}</b>\n\n```{lang_label}\n{code_text}\n```</div>", unsafe_allow_html=True)
        # End (do not call Groq)
        st.session_state.history.append({"role": "assistant", "content": f"Displayed {len(code_matches[:5])} snippet(s) from README (language: {requested_lang})."})
        # TTS of a brief message (if enabled) — keep it short
        if tts_toggle:
            speak_text(f"Displayed {len(code_matches[:5])} {requested_lang} snippet{'s' if len(code_matches)>1 else ''} from the README.")
    else:
        # No direct code match or user didn't request code explicitly — fallback to regular Groq response
        system_prompt = build_system_prompt(st.session_state.chat_mode, st.session_state.get("selected_project"))
        messages = [{"role": "system", "content": system_prompt}] + [
            {"role": ("user" if h["role"] == "user" else "assistant"), "content": h["content"]}
            for h in st.session_state.history[-8:]
        ]

        with st.spinner("Thinking..."):
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.25,
                    max_tokens=800
                )
                bot_text = completion.choices[0].message.content.strip()
            except Exception as e:
                bot_text = f"⚠️ Groq API error: {e}"

        # Display assistant message and save to history
        st.markdown(f"<div class='chat-bubble-bot' aria-label='Assistant message'><b>{context.get('assistant_name','Portfoli-AI')}:</b> {bot_text}</div>", unsafe_allow_html=True)
        st.session_state.history.append({"role": "assistant", "content": bot_text})

        # TTS if enabled
        if tts_toggle:
            speak_text(bot_text)

# Footer
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
