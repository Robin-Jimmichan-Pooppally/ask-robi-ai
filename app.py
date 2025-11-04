# app.py
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

# -----------------------
# Colors & links (user-provided)
# -----------------------
ACCENT = "#00bfff"  # electric blue - unified accent
HOVER_ACCENT = "#007acc"  # darker hover contrast
GITHUB_URL = "https://github.com/Robin-Jimmichan-Pooppally"
LINKEDIN_URL = "https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291"
EMAIL = "rjimmichan@gmail.com"

# -----------------------
# Public inline robot logo SVG (no repo dependency)
# Slight neon-line style (stroke-based), will be tinted with ACCENT via CSS
robot_svg = """
<svg viewBox="0 0 24 24" width="40" height="40" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
    <rect x="3.5" y="6" width="17" height="11" rx="2.2"/>
    <path d="M8 6V4.4a1.4 1.4 0 0 1 1.4-1.4h5.2A1.4 1.4 0 0 1 16 4.4V6"/>
    <circle cx="9" cy="11.5" r="0.9"/>
    <circle cx="15" cy="11.5" r="0.9"/>
    <path d="M9.5 15.5c.7.7 1.8.7 2.5 0"/>
    <path d="M7 18v1.2M17 18v1.2"/>
  </g>
</svg>
"""

# -----------------------
# Sticky Header
# -----------------------
st.markdown(f"""
    <style>
        /* Dark navy gradient background for the whole page */
        :root {{
          --accent: {ACCENT};
          --hover-accent: {HOVER_ACCENT};
        }}
        html, body {{
          height: 100%;
          margin: 0;
          padding: 0;
          background: linear-gradient(180deg, #000814 0%, #001f3f 100%);
          color: #e8f7ff;
        }}
        .sticky-header {{
            position: fixed; top: 0; left: 0; width: 100%;
            background: rgba(3,7,18,0.55); backdrop-filter: blur(6px);
            z-index: 9999; padding: 0.6rem 0;
            border-bottom: 1px solid var(--accent)33;
        }}
        .header-title {{
            text-align: center; font-size: 22px; font-weight: 600;
            color: var(--accent); text-shadow: 0 0 12px var(--accent);
        }}
        .clear-btn-container {{
            position: absolute; top: 8px; right: 20px;
        }}
        .clear-btn {{
            background-color:var(--accent); border:none; color:white;
            padding:6px 12px; border-radius:10px; cursor:pointer; font-weight:600;
            transition: all 0.18s ease-in-out;
            box-shadow: 0 6px 20px var(--accent)33, inset 0 -2px 6px rgba(0,0,0,0.35);
        }}
        .clear-btn:hover {{ transform: scale(1.04); box-shadow: 0 8px 28px var(--hover-accent)44; }}
        .spacer {{ height: 68px; }}
    </style>
    <div class="sticky-header">
        <div class="header-title">🤖 Portfoli-AI — Robin Jimmichan Pooppally's Portfolio Assistant</div>
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
    st.markdown(f"""
    <div style='border-radius:15px;padding:18px;background:linear-gradient(180deg, rgba(0,191,255,0.04), rgba(0,124,204,0.02));
    border:1px solid {ACCENT}33;box-shadow:0 0 26px {ACCENT}22;
    font-family:"Inter",sans-serif;margin-bottom:20px;'>
        <h4 style='color:{ACCENT};margin:0 0 8px 0;'>👋 Hey! I’m Portfoli-AI 🤖, your portfolio assistant for Robin’s projects.</h4>
        <p style='color:#e8f7ff;margin:0;'>
        Ask me about Robin’s projects, skills, or Business Analytics insights.<br>
        Try saying: “Explain my Telco Churn Dashboard project.”
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# -----------------------
# Global CSS (neon + consistency, animations)
# -----------------------
st.markdown(f"""
<style>
/* General */
body {{ background: transparent; color:#e8f7ff; font-size:16px; line-height:1.6; scroll-behavior:smooth; }}
h1,h2,h3 {{ color:var(--accent); text-shadow:0 0 12px var(--accent); }}

/* subtle keyframes */
@keyframes fadeInUp {{
  0% {{ opacity: 0; transform: translateY(8px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulseGlow {{
  0% {{ box-shadow: 0 6px 16px rgba(0,0,0,0.2), 0 0 0 0 rgba(0,191,255,0.0); }}
  50% {{ box-shadow: 0 8px 28px rgba(0,0,0,0.25), 0 0 24px rgba(0,191,255,0.06); }}
  100% {{ box-shadow: 0 6px 16px rgba(0,0,0,0.2), 0 0 0 0 rgba(0,191,255,0.0); }}
}}

/* Cards and bubbles */
.section-card {{
  background: linear-gradient(180deg, rgba(3,7,18,0.66), rgba(2,6,14,0.56));
  border-radius: 14px; padding: 14px;
  border: 1px solid var(--accent)2e;
  box-shadow: 0 6px 26px var(--accent)10;
}}
.chat-bubble-user, .chat-bubble-bot {{
  padding:12px 16px; border-radius:14px; margin:10px 0;
  transition: background 0.22s ease, transform 0.18s ease, box-shadow 0.18s ease;
  animation: fadeInUp .35s ease both;
  opacity: 0; /* animation will set to 1 */
  animation-fill-mode: both;
}}
.chat-bubble-user:hover, .chat-bubble-bot:hover {{ transform: translateY(-2px); }}
.chat-bubble-user {{
  background: linear-gradient(180deg, rgba(0,191,255,0.06), rgba(0,191,255,0.03));
  border: 1px solid var(--accent)33; color:#cffcff;
  box-shadow: 0 6px 20px rgba(0,191,255,0.06), 0 1px 0 rgba(0,0,0,0.4);
}}
.chat-bubble-bot {{
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid var(--accent)22; color:#e8f7ff;
  box-shadow: 0 6px 18px rgba(0,0,0,0.4), 0 0 8px rgba(0,191,255,0.02) inset;
}}

/* ensure animation actually shows opacity -> override for elements */
.chat-bubble-user, .chat-bubble-bot {{ opacity: 1; }}

/* Buttons and hover glow */
button.stButton>button {{
  border-radius:10px; transition: all 0.18s ease-in-out;
  border: 1px solid var(--accent)22;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00));
}}
button.stButton>button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 10px 30px var(--accent)22;
  border-color: var(--hover-accent);
}}

/* Selectbox focus / active uses chatbot blue */
.stSelectbox [data-baseweb="select"], select, .stSelectbox select {{
  border-color: var(--accent) !important; box-shadow: 0 0 18px var(--accent)15 !important;
  accent-color: var(--accent);
}}
input[type="radio"], input[type="checkbox"], select {{
  accent-color: var(--accent);
}}

.selected-project-label {{ color: var(--accent); font-weight:700; }}

/* Code bubble */
.code-bubble {{
  background: rgba(3,8,15,0.9);
  border-left: 3px solid var(--accent);
  padding: 12px;
  margin: 8px 0;
  border-radius: 10px;
  font-family: monospace;
  white-space: pre-wrap;
  overflow-x: auto;
}}

/* Sidebar social buttons (neon line icons) */
.social-row {{
  display:flex; gap:10px; align-items:center; margin-top:8px;
}}
.social-btn {{
  display:inline-flex; align-items:center; justify-content:center;
  width:36px; height:36px; border-radius:999px;
  border:1px solid var(--accent)33; background: rgba(255,255,255,0.008);
  box-shadow: 0 6px 18px rgba(0,0,0,0.55);
  transition: all .18s ease-in-out;
}}
.social-btn:hover {{
  transform: translateY(-3px);
  box-shadow: 0 10px 32px rgba(0,191,255,0.08);
  border-color: var(--hover-accent);
}}
/* Make inline SVGs line/stroke-based neon look */
.social-btn svg {{
  width:18px; height:18px; display:block;
  stroke: var(--accent); fill: none; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round;
}}
/* Top logo robot SVG tint */
.sidebar-robot svg {{ width:44px; height:44px; stroke: var(--accent); fill: none; stroke-width:1.6; }}

/* Footer icons (left aligned, icons only) */
.footer-icons {{
  display:flex; gap:12px; align-items:center; justify-content:flex-start;
  padding: 10px 6px;
}}
.footer-icon-btn {{
  display:inline-flex; align-items:center; justify-content:center;
  width:40px; height:40px; border-radius:10px;
  border:1px solid var(--accent)22; background: rgba(0,0,0,0.18);
  box-shadow: 0 6px 18px rgba(0,0,0,0.5);
  transition: all .22s ease-in-out;
}}
.footer-icon-btn:hover {{
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 14px 36px rgba(0,191,255,0.12), 0 0 28px rgba(0,191,255,0.06);
  border-color: var(--hover-accent);
  animation: pulseGlow 1.6s ease-in-out 1;
}}
.footer-icon-btn svg {{ width:18px; height:18px; stroke: var(--accent); fill:none; stroke-width:1.6; }}

/* small muted removed from footer per request (icons only) */

/* Responsive small */
@media (max-width: 600px) {{
  .header-title {{ font-size: 18px; }}
  .footer-icons {{ gap:10px; }}
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Sidebar top header (robot logo + name)
# -----------------------
st.sidebar.markdown("<div class='section-card' style='display:flex;align-items:center;gap:12px;'>", unsafe_allow_html=True)

st.sidebar.markdown(
    f"""
    <div style='display:flex;align-items:center;gap:12px;'>
      <div class='sidebar-robot'>{robot_svg}</div>
      <div style='line-height:1;'>
        <div style='font-weight:700;color:{ACCENT};'>🤖 Built by Robin Jimmichan P</div>
        <div style='font-size:12px;color:#bfefff;margin-top:2px;'>Portfolio Assistant</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

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

# Portfolio Overview section (stacked)
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📊 Portfolio Overview")
summary = context.get("summary", {})
for k, v in summary.items():
    st.sidebar.markdown(f"- **{k}**: {v}")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Contact section (stacked) with glowing social icons ONLY (no repeated textual labels)
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📬 Contact")

# Inline SVG icons (stroke-based) — public/open-line style, will be tinted via CSS
github_svg = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M12 .5C5.65.5.5 5.66.5 12.02c0 5.09 3.29 9.4 7.86 10.93.58.11.79-.25.79-.55 0-.27-.01-1.18-.02-2.14-3.2.69-3.88-1.54-3.88-1.54-.53-1.35-1.3-1.71-1.3-1.71-1.06-.72.08-.71.08-.71 1.17.08 1.79 1.2 1.79 1.2 1.04 1.78 2.73 1.27 3.4.97.11-.75.41-1.27.75-1.56-2.56-.29-5.26-1.28-5.26-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.21-1.49 3.18-1.18 3.18-1.18.63 1.6.23 2.78.11 3.06.74.81 1.19 1.85 1.19 3.1 0 4.42-2.71 5.39-5.29 5.67.42.36.79 1.07.79 2.16 0 1.56-.01 2.83-.01 3.22 0 .3.21.67.8.56A11.53 11.53 0 0 0 23.5 12.02C23.5 5.66 18.35.5 12 .5z"/></svg>"""
linkedin_svg = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M4.98 3.5C3.88 3.5 3 4.38 3 5.48c0 1.1.88 1.98 1.98 1.98 1.1 0 1.98-.88 1.98-1.98C6.96 4.38 6.08 3.5 4.98 3.5zM3.5 8.98h3v11.5h-3v-11.5zM9.5 8.98h2.88v1.58h.04c.4-.76 1.38-1.56 2.85-1.56 3.05 0 3.61 2.01 3.61 4.63v6.85h-3v-6.08c0-1.45-.03-3.33-2.03-3.33-2.03 0-2.34 1.58-2.34 3.21v6.2h-3v-11.5z"/></svg>"""
mail_svg = """<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.2-8 4.99-8-4.99V6l8 4.99L20 6v2.2z"/></svg>"""

st.sidebar.markdown(
    f"""
    <div class="social-row" aria-hidden="false">
      <a class="social-btn" href="{GITHUB_URL}" target="_blank" title="GitHub" aria-label="GitHub">{github_svg}</a>
      <a class="social-btn" href="{LINKEDIN_URL}" target="_blank" title="LinkedIn" aria-label="LinkedIn">{linkedin_svg}</a>
      <a class="social-btn" href="mailto:{EMAIL}" title="Email" aria-label="Email">{mail_svg}</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Close the contact card
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
    # Use the same label text and button logic
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
        # Primary initialization
        client = Groq(api_key=api_key)
        return client
    except TypeError as te:
        # Some Groq SDK versions may require different init signature.
        st.warning(f"Groq client init TypeError: {te}. Attempting fallback init.")
        try:
            client = Groq(api_key=api_key)  # attempt again (keeps behavior predictable)
            return client
        except Exception as e:
            st.error(f"Failed to initialize Groq client: {e}")
            st.stop()
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
    This function uses literal fenced-block matching (no fuzzy matching).
    """
    blocks = []
    if not readme_text:
        return blocks
    # Matches ```lang\n...``` (lang optional) - literal fenced code block matching
    pattern = re.compile(r"```([\w\-\+]+)?\n(.*?)```", re.DOTALL | re.IGNORECASE)
    for m in pattern.finditer(readme_text):
        lang = (m.group(1) or "").strip().lower()
        code = m.group(2).rstrip()
        blocks.append({"lang": lang, "code": code})
    return blocks

# -----------------------
# TTS helper (unchanged but guarded)
# -----------------------
def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buf = BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        st.audio(buf.read(), format="audio/mp3")
    except Exception as e:
        # Do not crash app if TTS fails
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
        # Parse code blocks immediately after fetching README (literal regex)
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
# --- Sidebar Contact Icons (glowing + hover pulse) ---
st.markdown("""
<div style='display:flex;justify-content:flex-start;gap:16px;padding:10px 0 4px 10px;'>
  <a href="https://github.com/Robin-Jimmichan-Pooppally" target="_blank" style="text-decoration:none;">
    <div class="footer-icon-btn" title="GitHub" aria-label="GitHub">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#00bfff" stroke-width="1.7" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 .5C5.65.5.5 5.66.5 12.02c0 5.09 3.29 9.4 7.86 10.93.58.11.79-.25.79-.55 0-.27-.01-1.18-.02-2.14-3.2.69-3.88-1.54-3.88-1.54-.53-1.35-1.3-1.71-1.3-1.71-1.06-.72.08-.71.08-.71 1.17.08 1.79 1.2 1.79 1.2 1.04 1.78 2.73 1.27 3.4.97.11-.75.41-1.27.75-1.56-2.56-.29-5.26-1.28-5.26-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.06 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.79 0c2.21-1.49 3.18-1.18 3.18-1.18.63 1.6.23 2.78.11 3.06.74.81 1.19 1.85 1.19 3.1 0 4.42-2.71 5.39-5.29 5.67.42.36.79 1.07.79 2.16 0 1.56-.01 2.83-.01 3.22 0 .3.21.67.8.56A11.53 11.53 0 0 0 23.5 12.02C23.5 5.66 18.35.5 12 .5z"/>
      </svg>
    </div>
  </a>

  <a href="https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291/" target="_blank" style="text-decoration:none;">
    <div class="footer-icon-btn" title="LinkedIn" aria-label="LinkedIn">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#00bfff" stroke-width="1.7" xmlns="http://www.w3.org/2000/svg">
        <path d="M4.98 3.5C3.88 3.5 3 4.38 3 5.48c0 1.1.88 1.98 1.98 1.98 1.1 0 1.98-.88 1.98-1.98C6.96 4.38 6.08 3.5 4.98 3.5zM3.5 8.98h3v11.5h-3v-11.5zM9.5 8.98h2.88v1.58h.04c.4-.76 1.38-1.56 2.85-1.56 3.05 0 3.61 2.01 3.61 4.63v6.85h-3v-6.08c0-1.45-.03-3.33-2.03-3.33-2.03 0-2.34 1.58-2.34 3.21v6.2h-3v-11.5z"/>
      </svg>
    </div>
  </a>

  <a href="mailto:rjimmichan@gmail.com" style="text-decoration:none;">
    <div class="footer-icon-btn" title="Email" aria-label="Email">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#00bfff" stroke-width="1.7" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.2-8 4.99-8-4.99V6l8 4.99L20 6v2.2z"/>
      </svg>
    </div>
  </a>
</div>

<style>
.footer-icon-btn {
  transition: all 0.3s ease-in-out;
  filter: drop-shadow(0 0 8px rgba(0,191,255,0.4));
}
.footer-icon-btn:hover {
  transform: scale(1.15);
  filter: drop-shadow(0 0 12px rgba(0,191,255,0.9));
}
</style>
""", unsafe_allow_html=True)


# End of file
