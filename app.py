"""
Final Portfoli-AI — Streamlit app (Groq + neon frosted UI + GitHub README preview + gTTS)
Place robi_context.py (the context you finalized) in same folder.
Add your Groq API key to Streamlit secrets: GROQ_API_KEY = "gsk_..."
"""

# -----------------------
# Phase 0: Imports & Context
# -----------------------
import streamlit as st
from groq import Groq
from gtts import gTTS
import tempfile
import os
import base64
from io import BytesIO
from io import BytesIO
import requests
import json
import os
import tempfile
import textwrap
import time
import base64
from urllib.parse import urlparse
import streamlit.components.v1 as components

# Import your verified context (must match what we finalized)
try:
    from robi_context import context
except ImportError:
    # Fallback context if robi_context.py is missing
    context = {
        'assistant_name': 'Portfoli-AI',
        'owner_name': 'Robin Jimmichan',
        'owner_role': 'Professional',
        'summary': {
            'Excel Projects': 5,
            'Power BI Projects': 3,
            'Python Projects': 4,
            'SQL Projects': 2
        },
        'projects': {
            'Excel': {'Project 1': 'https://github.com/example/excel1'},
            'Power BI': {'Dashboard 1': 'https://github.com/example/powerbi1'},
            'Python': {'App 1': 'https://github.com/python/app1'},
            'SQL': {'Database 1': 'https://github.com/example/sql1'}
        }
    }
    st.warning("Using fallback context. Please create robi_context.py for your personal details.")

# -----------------------
# Phase 1: Utilities & Prompt Builder
# -----------------------
def build_system_prompt(chat_mode, selected_project=None):
    """Build the system prompt based on chat mode and selected project."""
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
        You are in General Assistant mode. You can discuss a wide range of topics but maintain a professional tone
        appropriate for a portfolio assistant.
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

        When relevant, incorporate details about this project into your responses.
        If the user asks questions about the project, be as helpful as possible based on the context.
        """

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
# Phase 1.1: Page config & session defaults
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "history" not in st.session_state:
    st.session_state.history = []
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "All"
if "selected_project" not in st.session_state:
    st.session_state.selected_project = None
if "readme_full" not in st.session_state:
    st.session_state.readme_full = None
if "readme_preview" not in st.session_state:
    st.session_state.readme_preview = None
if "show_more" not in st.session_state:
    st.session_state.show_more = False

# -----------------------
# Phase 1.2: Sticky Header + Greeting
# -----------------------
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root{
            --bg:#050509;
            --panel: rgba(12,14,18,0.6);
            --muted:#cfdde6;
            --text:#e6f5fb;
            --accent:#00E5FF;
            --card-border: rgba(0,229,255,0.12);
            --glass-shadow: 0 10px 30px rgba(0,0,0,0.6);
        }
        body, .reportview-container, .streamlit-expanderHeader {
            font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
            background: linear-gradient(180deg, #000000 0%, #050509 100%);
            color: var(--text);
        }
        .sticky-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: linear-gradient(90deg, rgba(255,255,255,0.02), rgba(0,0,0,0.2));
            z-index: 9999;
            padding: 10px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            backdrop-filter: blur(6px);
        }
        .header-title {
            text-align: center;
            font-size: 20px;
            font-weight: 700;
            color: var(--accent);
            letter-spacing: 0.2px;
            text-shadow: 0 6px 20px rgba(0,229,255,0.06);
        }
        .clear-btn-container { position:absolute; right: 16px; top: 12px; }
        .clear-btn {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.04);
            color: var(--muted);
            padding: 6px 10px;
            border-radius: 10px;
            cursor: pointer;
            font-weight:600;
        }
        .spacer { height: 62px; }
        .greeting {
            border-radius: 12px;
            padding: 16px;
            background: linear-gradient(180deg, rgba(0,229,255,0.03), rgba(255,255,255,0.01));
            border: 1px solid var(--card-border);
            box-shadow: var(--glass-shadow);
            margin-bottom: 20px;
        }
        .greeting h4 { color: var(--accent); margin: 0 0 6px 0; font-weight:700; }
        .greeting p { color: var(--muted); margin:0; line-height:1.4; }
        .section-card {
            background: var(--panel);
            border-radius: 12px;
            padding: 14px;
            border: 1px solid var(--card-border);
            box-shadow: 0 8px 30px rgba(0,0,0,0.6);
        }
        .sidebar-item { display:flex; align-items:center; gap:8px; margin:6px 0; color:var(--muted); font-weight:500; }
        .sidebar-item .count { margin-left:auto; font-weight:700; color:var(--accent); padding:4px 8px; border-radius:8px; background: rgba(0,229,255,0.04); }
        .chat-row { display:flex; gap:12px; align-items:flex-start; margin:8px 0; }
        .chat-avatar { width:40px; height:40px; border-radius:50%; flex:0 0 40px; display:inline-block; overflow:hidden; border:1px solid rgba(255,255,255,0.04); }
        .chat-bubble {
            max-width:78%;
            padding:12px 14px;
            border-radius:12px;
            line-height:1.45;
            font-size:14px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.6);
        }
        .chat-bubble-user { 
            margin-left:auto;
            background: linear-gradient(180deg, rgba(0,229,255,0.04), rgba(0,0,0,0.12));
            border: 1px solid rgba(0,229,255,0.08);
            color: var(--text);
            border-top-right-radius:4px;
        }
        .chat-bubble-bot {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(0,0,0,0.06));
            border: 1px solid rgba(255,255,255,0.03);
            color: var(--text);
            border-top-left-radius:4px;
        }
        .icon-link { 
            display:inline-flex; 
            align-items:center; 
            gap:8px; 
            padding:6px 8px; 
            border-radius:8px; 
            text-decoration:none; 
            color:var(--muted); 
            border:1px solid rgba(255,255,255,0.03);
            margin: 4px 0;
            transition: all 0.2s ease;
        }
        .icon-link:hover { 
            color:var(--text); 
            border-color: rgba(0,229,255,0.10); 
            background: rgba(0,229,255,0.02); 
        }
        .small-muted { color: var(--muted); font-size:12px; margin-top: 8px; }
        input[aria-label="Type your message..."] {
            background: rgba(255,255,255,0.02) !important;
            border: 1px solid rgba(255,255,255,0.04) !important;
            padding: 10px 12px !important;
            border-radius: 12px !important;
            color: var(--text) !important;
            outline: none !important;
            transition: box-shadow 200ms ease, border-color 200ms ease;
            width: 100%;
        }
        input[aria-label="Type your message..."]:focus {
            box-shadow: 0 6px 28px rgba(0,229,255,0.12);
            border-color: var(--accent) !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, #00E5FF, #0088FF);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 229, 255, 0.2);
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

if not st.session_state.greeted:
    st.markdown("""
    <div class='greeting'>
        <h4>👋 Hey there!</h4>
        <p>
        I'm <b style='color:var(--accent)'>Portfoli-AI 🤖</b>, your portfolio assistant — here to explain projects, talk business analytics,
        or help craft README summaries. Try: <i>"Explain my latest project"</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True

# -----------------------
# Phase 2: Sidebar
# -----------------------
with st.sidebar:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.markdown(f"### 👋 {context.get('owner_name','Robin J')}")
    st.markdown(f"**{context.get('owner_role','Professional')}**")
    st.markdown("---")

    # Contact info
    st.markdown("📬 **Contact**")
    st.markdown(f"<a class='icon-link' href='mailto:rjimmichan@gmail.com'>✉️ Email — rjimmichan@gmail.com</a>", unsafe_allow_html=True)
    st.markdown(f"<a class='icon-link' href='https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291' target='_blank'>🔗 LinkedIn</a>", unsafe_allow_html=True)
    st.markdown(f"<a class='icon-link' href='https://github.com/Robin-Jimmichan-Pooppally' target='_blank'>🐱 GitHub</a>", unsafe_allow_html=True)
    st.markdown("---")

    # TTS Toggle
    tts_toggle = st.checkbox("🔊 Play responses (TTS)", value=False)
    
    # Save chat locally
    save_local = st.checkbox("💾 Save chat locally", value=False)
    
    # Clear chat button
    if st.button("🧹 Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.history = []
        try:
            if os.path.exists("chat_memory.json"):
                os.remove("chat_memory.json")
        except Exception:
            pass
        st.experimental_rerun()

    # Portfolio overview
    st.markdown("### 📊 Portfolio Overview")
    summary = context.get("summary", {})
    for k, v in summary.items():
        icon = "📊" if "Excel" in k or "Power" in k else ("🐍" if "Python" in k else "🗄️")
        st.markdown(f"<div class='sidebar-item'>{icon} <strong>{k}</strong> <span class='count'>{v}</span></div>", unsafe_allow_html=True)
    
    # Calculate and display total projects
    total_projects = sum(summary.values()) if summary else 0
    st.markdown("<hr style='border-color: rgba(255,255,255,0.03)'>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight:700; color:var(--text);'>Total Projects: <span style='color:var(--accent);'>{total_projects}</span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Project Selection
# -----------------------
projects_by_cat = context.get("projects", {})
all_projects = []
for cat, projs in projects_by_cat.items():
    for name, url in projs.items():
        all_projects.append((cat, name, url))

# Category filter
st.markdown("### 🔎 Filter by category")
cols = st.columns(4)
cats = list(projects_by_cat.keys())
ordered = []
for want in ["Excel", "Power BI", "Python", "SQL"]:
    if want in cats:
        ordered.append(want)
if not ordered:
    ordered = cats

selected_cat = None
for i, cat in enumerate(ordered):
    if cols[i % 4].button(cat, key=f"cat_{cat}"):
        selected_cat = cat

if selected_cat:
    st.session_state.selected_category = selected_cat

st.markdown(f"Showing projects: **{st.session_state['selected_category'] if st.session_state['selected_category'] != 'All' else 'All categories'}")

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

# -----------------------
# Groq client initialization
# -----------------------
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ Missing Groq API key. Add GROQ_API_KEY to Streamlit secrets or environment variables.")
        st.stop()
    try:
        client = Groq(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"❌ Failed to initialize Groq client: {e}")
        st.stop()

client = init_groq()

# -----------------------
# Helper functions
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

def speak_text(text):
    try:
        # Limit text length to prevent very long audio generation
        if len(text) > 200:
            text = text[:200] + "... [truncated]"
        
        # Create a status message
        status = st.empty()
        status.info("🔊 Preparing audio...")
        
        # Generate speech using gTTS
        # Using clearer, professional voice (slow=True) and default tld 'com'
        tts = gTTS(text=text, lang='en', tld='com', slow=True)
        
        # Use BytesIO to handle audio in memory
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Create a data URI for the audio
        audio_b64 = base64.b64encode(audio_buffer.read()).decode('utf-8')
        audio_html = f'''
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        '''
        
        # Display the audio player
        components.html(audio_html, height=60)
        
        # Show success message
        status.success("🔊 Audio ready!")
        return True
        
    except Exception as e:
        st.error(f"Failed to generate speech: {str(e)}")
        st.warning("""
        If you're running this on Streamlit Cloud, please note that:
        1. Audio playback might be blocked by the browser
        2. Try clicking the refresh button in the audio player
        3. Make sure your browser allows autoplay
        """)
        return False

def save_chat_local(history):
    try:
        with open("chat_memory.json", "w", encoding="utf-8") as fh:
            json.dump(history, fh, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"Failed to save chat: {e}")

# -----------------------
# Project display
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

if st.session_state.get("selected_project"):
    repo_url = st.session_state.selected_project
    card_cat = card_name = None
    for c, name, r in all_projects:
        if r == repo_url:
            card_cat, card_name = c, name
            break
    
    with st.container():
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
# Chat interface
# -----------------------
assistant_name = context.get('assistant_name', 'Portfoli-AI')
assistant_avatar_svg = """<svg viewBox="0 0 64 64" width="40" height="40" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="12" fill="#071014"/>
  <path d="M32 12c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 26c-9.941 0-18 8.059-18 18h36c0-9.941-8.059-18-18-18z" fill="#00E5FF" opacity="0.95"/>
</svg>"""

# Display chat history
for m in st.session_state.history:
    role = m.get("role")
    text = m.get("content")
    if role == "user":
        st.markdown(f"""
            <div class="chat-row" style="justify-content:flex-end;">
              <div class="chat-bubble chat-bubble-user"><b>You:</b><br>{text}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="chat-row">
              <div class="chat-avatar">{assistant_avatar_svg}</div>
              <div class="chat-bubble chat-bubble-bot"><b>{assistant_name}:</b><br>{text}</div>
            </div>
        """, unsafe_allow_html=True)

# Chat input form
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input(
        "Type your message...", 
        key="user_input", 
        placeholder="Ask me anything...",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button("Send")

# Process form submission
if submit_button and user_input:
    # Append user message to history
    st.session_state.history.append({"role": "user", "content": user_input})

    # Optional: save locally
    if save_local:
        save_chat_local(st.session_state.history)

    # Build system prompt and send to Groq
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
            # defensive access
            bot_text = ""
            if completion and hasattr(completion, "choices") and len(completion.choices) > 0:
                # some SDKs return different structures; be defensive
                choice = completion.choices[0]
                if hasattr(choice, "message") and hasattr(choice.message, "content"):
                    bot_text = choice.message.content.strip()
                elif isinstance(choice, dict) and "message" in choice and "content" in choice["message"]:
                    bot_text = choice["message"]["content"].strip()
                else:
                    # fallback to string repr
                    bot_text = str(choice)
            else:
                bot_text = "⚠️ Received empty response from Groq."

        except Exception as e:
            bot_text = f"⚠️ Groq API error: {e}"

    # Append assistant response
    st.session_state.history.append({"role": "assistant", "content": bot_text})

    # Optional: save locally after assistant reply
    if save_local:
        save_chat_local(st.session_state.history)

    # TTS (plays if toggled in sidebar)
    if tts_toggle:
        success = speak_text(bot_text)
        if not success:
            st.warning("""
            Couldn't generate speech. Please try these steps:
            1. Check your internet connection
            2. Refresh the page and try again
            3. Make sure your browser allows audio autoplay
            """)

    # Rerun to update the UI
    st.experimental_rerun()

# -----------------------
# Footer / credits
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
