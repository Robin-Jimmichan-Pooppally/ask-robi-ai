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
from robi_context import context

# --- ACCENT COLOR DEFINITION (Vibrant Cyan) ---
ACCENT_COLOR = "#00FFFF"
ACCENT_RGB_LOW = "rgba(0, 255, 255, 0.15)" # Used for backgrounds
ACCENT_RGB_MEDIUM = "rgba(0, 255, 255, 0.4)" # Used for borders
ACCENT_RGB_HIGH = "rgba(0, 255, 255, 0.8)" # Used for text/emphasis

def build_system_prompt(chat_mode, selected_project=None):
    """
    Build the system prompt based on chat mode and selected project.
    
    Args:
        chat_mode (str): Either "General Assistant" or "Business Analytics Assistant"
        selected_project (str, optional): The URL of the selected project. Defaults to None.
    
    Returns:
        str: The system prompt to use for the chat
    """
    # Base system prompt (NO CHANGE)
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
    else:  # General Assistant
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
# Page config (NO CHANGE)
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# -----------------------
# Initialize session state (NO CHANGE)
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "history" not in st.session_state:
    st.session_state.history = []

if "tts_toggle" not in st.session_state:
    st.session_state.tts_toggle = False

# --- Sticky Header (REMOVED/SIMPLIFIED - Streamlit header is complex to override safely) ---
# NOTE: Removed the complex sticky header, relying on native Streamlit layout for safety.
st.title("Portfoli-AI")
# st.markdown("""...""", unsafe_allow_html=True) # REMOVED: Rely on simpler layout

# -----------------------
# Greeting message (NO CHANGE)
# -----------------------
if "greeted" not in st.session_state:
    st.session_state.greeted = False

if not st.session_state.greeted:
    st.markdown(f"""
    <div style='
        border-radius: 15px;
        padding: 18px;
        background: {ACCENT_RGB_LOW};
        border: 1px solid {ACCENT_RGB_MEDIUM};
        box-shadow: 0 0 15px {ACCENT_RGB_MEDIUM};
        font-family: "Inter", sans-serif;
        margin-bottom: 20px;
    '>
        <h4 style='color:{ACCENT_COLOR};'>👋 Hey!</h4>
        <p style='color:white;'>
        I'm <b style='color:{ACCENT_COLOR};'>Portfoli-AI 🤖</b>, your portfolio assistant.<br><br>
        Ask me about your <b>projects</b>, <b>skills</b>, or <b>business analytics insights</b>.<br>
        Try saying: <i>"Explain my Telco Churn Dashboard project.</i>"
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# -----------------------
# CSS (Updated for "Legendary" Look)
# -----------------------
st.markdown(
    f"""
<style>
/* --- General and Typography --- */
body {{ background: #000000; color: #E0E0E0; font-family: 'Inter', 'Poppins', sans-serif; }}
h1, h2, h3, .header-title {{ 
    color: {ACCENT_COLOR}; 
    text-shadow: 0 0 8px {ACCENT_COLOR}; 
    font-family: 'Poppins', sans-serif;
}}
/* --- Frosted Card Style --- */
.section-card {{
    background: rgba(10,12,18,0.75); /* Darker, slightly frosted */
    border-radius: 14px;
    padding: 14px;
    border: 1px solid {ACCENT_RGB_MEDIUM};
    box-shadow: 0 6px 26px {ACCENT_RGB_LOW};
}}

/* --- Chat Bubbles (User/Bot Differentiation) --- */
.chat-bubble-user {{
    background: {ACCENT_RGB_LOW};
    border: 1px solid {ACCENT_RGB_MEDIUM};
    color: #cffcff; /* Light, slightly cyan text */
    padding: 12px 16px;
    border-radius: 16px 16px 4px 16px; /* Unique shape */
    margin: 8px 0;
    margin-left: 20%; /* Pushes user bubble to the right */
}}
.chat-bubble-bot {{
    background: rgba(255,255,255,0.08); /* Lighter background for bot */
    border: 1px solid rgba(255,255,255,0.15);
    color: #E0E0E0; /* Light gray text for bot */
    padding: 12px 16px;
    border-radius: 16px 16px 16px 4px; /* Unique shape */
    margin: 8px 0;
    margin-right: 20%; /* Pushes bot bubble to the left */
}}

/* --- Button/Interactive Elements (Hover/Active Effects) --- */
button.stButton>button {{ 
    border-radius: 8px; 
    transition: all 0.2s ease;
}}
button.stButton>button:hover {{
    background-color: {ACCENT_COLOR};
    color: #000000;
    border: 1px solid {ACCENT_COLOR};
    box-shadow: 0 0 10px {ACCENT_COLOR};
}}
/* --- Active Category Button Highlight --- */
.stButton button[data-testid*="stButton"]:focus {{
    background-color: {ACCENT_COLOR} !important;
    color: #000000 !important;
    border: 1px solid {ACCENT_COLOR} !important;
}}

/* --- Text Input (Glow on Focus) --- */
div[data-testid="stTextInput"] > div > div > input:focus {{
    box-shadow: 0 0 15px {ACCENT_COLOR} !important;
    border-color: {ACCENT_COLOR} !important;
}}

/* --- Sidebar Link Icons (to make them look actionable) --- */
a[href*="linkedin.com"] {{ content: "🔗 "; }}
a[href*="github.com"] {{ content: "🐙 "; }}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------
# Sidebar: portfolio overview + links + filters (UPDATED)
# -----------------------
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)

# Profile Area
st.sidebar.markdown(f"### 👨‍💻 {context['owner_name']}")
st.sidebar.markdown(f"**{context['owner_role']}**")
st.sidebar.markdown("---")

# Contact Section (Icons added via inline markdown)
st.sidebar.markdown("### 📬 Contact")
st.sidebar.markdown(f"- 📧 Email: <a href='mailto:{'rjimmichan@gmail.com'}' style='color:{ACCENT_COLOR}'>{'rjimmichan@gmail.com'}</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- 🔗 LinkedIn: <a href='{ 'https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291'}' target='_blank'>Profile</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"- 🐙 GitHub: <a href='{ 'https://github.com/Robin-Jimmichan-Pooppally'}' target='_blank'>Robin-Jimmichan-Pooppally</a>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# TTS Toggle moved to Sidebar
tts_toggle = st.sidebar.checkbox("🔊 Play responses (TTS)", value=st.session_state.get("tts_toggle", False), key="tts_toggle_sidebar")
st.session_state.tts_toggle = st.session_state.tts_toggle_sidebar # Sync the state

# Portfolio overview counts (with icons and highlighted numbers)
summary = context.get("summary", {})
st.sidebar.markdown("### 📊 Portfolio Overview")

# Icon mapping for improved sidebar
icon_map = {
    "Excel Projects": "📊",
    "Power BI Projects": "📈",
    "Python Projects": "🐍",
    "SQL Projects": "💾",
    "Total Projects": "⭐"
}

for k, v in summary.items():
    icon = icon_map.get(k, "•")
    if "Total Projects" in k:
        # Highlight total projects
        st.sidebar.markdown(f"**{icon} {k}**: <span style='color:{ACCENT_COLOR}; font-weight:bold;'>{v}</span>", unsafe_allow_html=True)
        st.sidebar.markdown("---") # Visual separator
    else:
        # Highlight count for individual projects
        st.sidebar.markdown(f"- {icon} **{k.replace(' Projects', '')}**: <span style='color:{ACCENT_COLOR}; font-weight:bold;'>{v}</span>", unsafe_allow_html=True)
        
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Prepare projects list (flattened and grouped) (NO CHANGE)
# -----------------------
projects_by_cat = context.get("projects", {})
# Flatten into list of tuples: (category, project_name, repo_url)
all_projects = []
for cat, d in projects_by_cat.items():
    for pname, repo in d.items():
        all_projects.append((cat, pname, repo))

# Category filter buttons (top, horizontally - ADDED CUSTOM CSS CLASS FOR HOVER/ACTIVE)
st.markdown(f"### 🔎 Filter by category")
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
    # Use key to help manage state and ensure unique buttons
    if cols[i % 4].button(cat, key=f"cat_btn_{cat}"):
        selected_cat = cat

# Keep selection in session (persist)
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if selected_cat:
    st.session_state.selected_category = selected_cat

# Show currently selected category (HIGHLIGHTED)
if st.session_state.get("selected_category", "All") == "All":
    st.markdown("Showing projects: **All categories**")
else:
    st.markdown(f"Showing projects: <span style='color:{ACCENT_COLOR}; font-weight:bold;'>{st.session_state['selected_category']}</span>", unsafe_allow_html=True)

# Build dropdown project list filtered by the selected category (NO CHANGE)
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
# Chat mode toggle (UPDATED - highlighted active mode)
# -----------------------
st.markdown("---")
mode = st.radio(
    "Chat mode", 
    ("General Assistant", "Business Analytics Assistant"), 
    horizontal=True,
    # Inject CSS to style the active radio button
    index=0 if st.session_state.get("chat_mode", "General Assistant") == "General Assistant" else 1,
)

# Persist mode
if "chat_mode" not in st.session_state or st.session_state.get("chat_mode") != mode:
    st.session_state.chat_mode = mode
    st.session_state.history = []  # reset conversation on mode change

# -----------------------
# Groq client init (safe) (NO CHANGE)
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
# Helpers: fetch README from GitHub (NO CHANGE)
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
# Helper: gTTS speak (NO CHANGE)
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
# Chat history initialization (NO CHANGE)
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
# When project selection changes -> load README preview and reset chat for that project (NO CHANGE)
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
# Display selected project card above chat (NO CHANGE)
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

# -----------------------
# Chat UI: display history (UPDATED - added assistant avatar placeholder)
# -----------------------
for m in st.session_state.history:
    role = m.get("role")
    text = m.get("content")
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        # Added a simple text avatar (emoji)
        st.markdown(f"<div class='chat-bubble-bot'><b>🤖 {context.get('assistant_name','Portfoli-AI')}:</b> {text}</div>", unsafe_allow_html=True)


# -----------------------
# User input (MAJOR CHANGE: Removed buttons, added on_submit handler)
# -----------------------

# The TTS toggle is now in the sidebar, synced by the key="tts_toggle_sidebar" above.

# Function to handle sending message when Enter is pressed
def handle_submit():
    user_input = st.session_state.chat_input_key
    if user_input.strip():
        # Append message and clear the input field
        st.session_state.history.append({"role": "user", "content": user_input})
        st.session_state.chat_input_key = "" # Clear the input
        # Note: The Groq call logic is triggered below when st.session_state.history changes.
        st.rerun()

# Use st.text_input with an on_change and key to capture Enter press
# The label is set to an empty string for cleaner UI, relying on the placeholder
st.text_input(
    "", # Empty label
    key="chat_input_key", 
    placeholder="Type your message and press ENTER to send...", 
    on_change=handle_submit, # Triggers when Enter is pressed
    # Custom CSS class can be injected here if needed for audio wave placement
)


# -----------------------
# Send question -> Groq (UPDATED: Check tts_toggle state from session)
# -----------------------
# The logic below now checks if the last item in history is a user message
if st.session_state.history and st.session_state.history[-1].get("role") == "user":
    user_input_content = st.session_state.history[-1].get("content")
    
    # We already appended the user message in handle_submit, so we proceed directly
    system_prompt = build_system_prompt(st.session_state.chat_mode, st.session_state.get("selected_project"))
    messages = [{"role": "system", "content": system_prompt}]
    
    # Use the history (including the just-added user message)
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
    
    # Check the tts state from the synced session variable
    if st.session_state.tts_toggle:
        try:
            speak_text(bot_text)
        except Exception:
            st.warning("TTS failed for this response.")
    
    # Rerun to display the bot's response
    st.rerun()


# -----------------------
# Footer / credits (NO CHANGE)
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
