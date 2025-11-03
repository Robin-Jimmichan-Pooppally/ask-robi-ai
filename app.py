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

# Import your verified context (must match what we finalized)
from robi_context.py import context

def build_system_prompt(chat_mode, selected_project=None):
    """
    Build the system prompt based on chat mode and selected project.
    
    Args:
        chat_mode (str): Either "General Assistant" or "Business Analytics Assistant"
        selected_project (str, optional): The URL of the selected project. Defaults to None.
    
    Returns:
        str: The system prompt to use for the chat
    """
    # Base system prompt
    base_prompt = f"""
    You are {context.get('assistant_name', 'Portfoli-AI')}, a helpful AI assistant for {context.get('owner_name', 'the user')}'s portfolio.
    {context.get('owner_name', 'The user')} is a {context.get('owner_role', 'professional')}.
    """
    
    # Add mode-specific context
    if chat_mode == "Business Analytics Assistant":
        base_prompt += """
        You are in Business Analytics Assistant mode. Focus on providing insights, analysis, and explanations
        related to data analytics, visualization, and business intelligence.
        """
    else:  # General Assistant
        base_prompt += """
        You are in General Assistant mode. You can discuss a wide range of topics but maintain a professional tone
        appropriate for a portfolio assistant.
        """
    
    # Add project context if a project is selected
    if selected_project:
        # Find the project details
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
        
        When relevant, incorporate details about this project into your responses.
        If the user asks questions about the project, be as helpful as possible based on the context.
        """
    
    # Add general instructions
    base_prompt += """
    
    Guidelines:
    - Be concise but thorough in your responses
    - Use markdown formatting where appropriate (e.g., **bold** for emphasis, `code` for technical terms)
    - If you don't know something, say so rather than making up information
    - Maintain a professional but friendly tone
    - If the user asks about skills or technologies, reference the context when possible
    """
    
    return base_prompt.strip()

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
            height: 65px; /* keeps content from being hidden behind header */
        }
    </style>
    <div class="sticky-header">
        <div class="header-title">🤖 Portfoli-AI — Robin Jimmichan's Portfolio Assistant</div>
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
        <h4 style='color:#00bfff;'>👋 Hey!</h4>
        <p style='color:white;'>
        I'm <b style='color:#00bfff;'>Portfoli-AI 🤖</b>, your portfolio assistant.<br><br>
        Ask me about your <b>projects</b>, <b>skills</b>, or <b>business analytics insights</b>.<br>
        Try saying: <i>"Explain my Telco Churn Dashboard project.</i>"
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# -----------------------
# CSS (neon blue frosted glass)
# -----------------------
st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)

# -----------------------
# Sidebar: portfolio overview + links + filters
# -----------------------
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown(f"### 👋 {context['owner_name']}")
st.sidebar.markdown(f"**{context['owner_role']}**")
st.sidebar.markdown("---")
st.sidebar.markdown("📬 **Contact**")
st.sidebar.markdown(f"- Email: <a href='mailto:{'rjimmichan@gmail.com'}'>{'rjimmichan@gmail.com'}</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- LinkedIn: <a href='{ 'https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291'}'>Profile</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- GitHub: <a href='{ 'https://github.com/Robin-Jimmichan-Pooppally'}'>Robin-Jimmichan-Pooppally</a>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Portfolio overview counts (from context)
summary = context.get("summary", {})
st.sidebar.markdown("### 📊 Portfolio Overview")
for k, v in summary.items():
    st.sidebar.markdown(f"- **{k}**: {v}")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Prepare projects list (flattened and grouped)
# -----------------------
projects_by_cat = context.get("projects", {})
# Flatten into list of tuples: (category, project_name, repo_url)
all_projects = []
for cat, d in projects_by_cat.items():
    for pname, repo in d.items():
        all_projects.append((cat, pname, repo))

# Category filter buttons (top, horizontally)
st.markdown("### 🔎 Filter by category")
cols = st.columns(4)
cats = list(projects_by_cat.keys())
# ensure fixed order Excel, Power BI, Python, SQL
ordered = []
for want in ["Excel", "Power BI", "Python", "SQL"]:
    if want in cats:
        ordered.append(want)
if not ordered:
    ordered = cats

selected_cat = None
for i, cat in enumerate(ordered):
    if cols[i % 4].button(cat):
        selected_cat = cat

# Keep selection in session (persist)
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if selected_cat:
    st.session_state.selected_category = selected_cat

# Show currently selected category
if st.session_state.get("selected_category", "All") == "All":
    st.markdown("Showing projects: **All categories**")
else:
    st.markdown(f"Showing projects: **{st.session_state['selected_category']}**")

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

# -----------------------
# Chat mode toggle
# -----------------------
st.markdown("---")
mode = st.radio("Chat mode", ("General Assistant", "Business Analytics Assistant"), horizontal=True)
# Persist mode
if "chat_mode" not in st.session_state or st.session_state.get("chat_mode") != mode:
    st.session_state.chat_mode = mode
    st.session_state.history = []  # reset conversation on mode change

# -----------------------
# Groq client init (safe)
# -----------------------
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
# Helpers: fetch README from GitHub
# -----------------------
def extract_owner_repo(repo_url):
    parsed = urlparse(repo_url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None

def fetch_readme_lines(repo_url, max_lines=20):
    owner, repo = extract_owner_repo(repo_url)
    if not owner:
        return None, "Invalid repo URL"
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
# Helper: gTTS speak
# -----------------------
def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en", slow=False)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        st.audio(buf.read(), format="audio/mp3")
    except Exception as e:
        st.warning("TTS unavailable: " + str(e))

# -----------------------
# Chat history initialization
# -----------------------
if "history" not in st.session_state:
    st.session_state.history = []
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "readme_full" not in st.session_state:
    st.session_state.readme_full = None
if "readme_preview" not in st.session_state:
    st.session_state.readme_preview = None
if "show_more" not in st.session_state:
    st.session_state.show_more = False

# -----------------------
# When project selection changes -> load README preview and reset chat for that project
# -----------------------
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
        st.session_state.show_more = False

# -----------------------
# Display selected project card above chat
# -----------------------
if st.session_state.get("selected_project"):
    repo_url = st.session_state.selected_project
    card_cat = card_name = None
    for c, name, r in all_projects:
        if r == repo_url:
            card_cat, card_name = c, name
            break
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"### 📁 {card_name}")
    st.markdown(f"**Category:** {card_cat}  ")
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

# -----------------------
# Chat UI: display history
# -----------------------
for m in st.session_state.history:
    role = m.get("role")
    text = m.get("content")
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'><b>{context.get('assistant_name','Portfoli-AI')}:</b> {text}</div>", unsafe_allow_html=True)

# -----------------------
# User input
# -----------------------

tts_toggle = st.checkbox("🔊 Play responses (TTS)", value=False)

# --- Chat input with Send and Erase buttons ---
col1, col2 = st.columns([8, 1.2])

with col1:
    user_input = st.text_input("Type your message...", key="chat_input", placeholder="Ask me anything...")

with col2:
    send = st.button("🚀")
    erase = st.button("🧹")

# Handle button actions
if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    # Use st.rerun() to clear the input field
    st.rerun()

if erase:
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.rerun()

# -----------------------
# Send question -> Groq
# -----------------------
if user_input:
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
# Footer / credits
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)

Can u do these chnages
