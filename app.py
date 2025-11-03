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
from io import BytesIO
import requests
import json
import os
import textwrap
from urllib.parse import urlparse


# Import your verified context (must match what we finalized)
from robi_context import context


# -----------------------
# Phase 1: Utilities & Prompt Builder
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
    - Use markdown formatting where appropriate (e.g., **bold** for emphasis, code for technical terms)
    - If you don't know something, say so rather than making up information
    - Maintain a professional but friendly tone
    - If the user asks about skills or technologies, reference the context when possible
    """


    return base_prompt.strip()


# -----------------------
# Phase 1.1: Page config & session defaults
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")


# Initialize session state keys safely
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


# -----------------------
# Phase 1.2: New Sticky Header + Greeting (Legendary look)
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
        .spacer { height: 62px; } /* keeps content from being hidden behind header */


        /* Greeting card */
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
        <h4>👋 Hey!</h4>
        <p>
        I'm <b style='color:var(--accent)'>Portfoli-AI 🤖</b>, your portfolio assistant — here to explain projects, talk BA,
        or help craft README summaries. Try: <i>"Explain my Telco Churn Dashboard"</i>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.greeted = True


# -----------------------
# Phase 1.3: Global CSS (bubbles, micro-interactions, inputs)
# -----------------------
st.markdown("""
<style>
:root{
  --accent:#00E5FF;
  --bg:#050509;
  --panel: rgba(12,14,18,0.6);
  --muted:#a9cbd9;
  --text:#e6f5fb;
  --card-border: rgba(0,229,255,0.10);
}


body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; }


/* Section card style */
.section-card {
  background: var(--panel);
  border-radius: 12px;
  padding: 14px;
  border: 1px solid var(--card-border);
  box-shadow: 0 8px 30px rgba(0,0,0,0.6);
}


/* Portfolio sidebar items */
.sidebar-item { display:flex; align-items:center; gap:8px; margin:6px 0; color:var(--muted); font-weight:500; }
.sidebar-item .count { margin-left:auto; font-weight:700; color:var(--accent); padding:4px 8px; border-radius:8px; background: rgba(0,229,255,0.04); }


/* Category buttons (we will render them as columns/buttons) */
.stButton>button.category-btn {
  border-radius: 10px;
  padding: 8px 10px;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.04);
  color: var(--muted);
  transition: all 170ms ease;
  font-weight:600;
}
.stButton>button.category-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,229,255,0.05);
  color: var(--text);
  border-color: rgba(0,229,255,0.12);
  background: linear-gradient(180deg, rgba(0,229,255,0.02), rgba(255,255,255,0.01));
}


/* Active category visual (underline) - we will set class via markdown/html where possible */
.category-active {
  color: var(--text) !important;
  border-bottom: 3px solid var(--accent) !important;
  border-radius: 6px;
}


/* Chat bubbles */
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


/* Input */
.input-wrap { display:flex; gap:8px; align-items:center; margin-top: 12px; }
.streamlit-expanderHeader, .stTextInput>div, .stTextInput label {
  font-family: 'Inter', sans-serif;
}
input[aria-label="Type your message..."] {
  background: rgba(255,255,255,0.02) !important;
  border: 1px solid rgba(255,255,255,0.04) !important;
  padding: 10px 12px !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  outline: none !important;
  transition: box-shadow 200ms ease, border-color 200ms ease;
}
input[aria-label="Type your message..."]:focus {
  box-shadow: 0 6px 28px rgba(0,229,255,0.12);
  border-color: var(--accent) !important;
}


/* small muted text */
.small-muted { color: var(--muted); font-size:12px; }


/* footer */
.footer { color: var(--muted); font-size:12px; margin-top:18px; }


/* Icon links */
.icon-link { display:inline-flex; align-items:center; gap:8px; padding:6px 8px; border-radius:8px; text-decoration:none; color:var(--muted); border:1px solid rgba(255,255,255,0.03); }
.icon-link:hover { color:var(--text); border-color: rgba(0,229,255,0.10); background: rgba(0,229,255,0.02); }
</style>
""", unsafe_allow_html=True)


# -----------------------
# Phase 2: Sidebar redesign (contacts, portfolio overview, TTS moved here)
# -----------------------
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown(f"### 👋 {context.get('owner_name','Robin J')}")
st.sidebar.markdown(f"**{context.get('owner_role','Professional')}**")
st.sidebar.markdown("---")


# Contact with icon links (inline SVGs for LinkedIn/GitHub)
linkedin_svg = '''<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M4.98 3.5C4.98 4.88071 3.86 6 2.48 6C1.1 6 0 4.88071 0 3.5C0 2.11929 1.1 1 2.48 1C3.86 1 4.98 2.11929 4.98 3.5Z" fill="currentColor"/>
<path d="M6.5 8H0V24H6.5V8Z" fill="currentColor"/>
<path d="M24 24H17.5V15.5C17.5 13 16 11.5 13.75 11.5C11.5 11.5 10.5 13.1 10.5 15.5V24H4V8H10.25V10.1H10.3C11.1 9 12.9 7.8 15.8 7.8C20.75 7.8 24 10.9 24 16.5V24Z" fill="currentColor"/>
</svg>'''
github_svg = '''<svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M8 .198a8 8 0 00-2.53 15.59c.4.073.547-.173.547-.385 0-.19-.007-.693-.01-1.36-2.226.483-2.695-1.073-2.695-1.073-.364-.923-.89-1.17-.89-1.17-.727-.497.055-.487.055-.487.803.057 1.225.826 1.225.826.714 1.223 1.873.87 2.33.665.072-.518.28-.87.508-1.07-1.777-.202-3.644-.888-3.644-3.953 0-.873.312-1.587.824-2.147-.083-.203-.357-1.017.078-2.12 0 0 .672-.215 2.2.82A7.627 7.627 0 018 4.68c.68.003 1.367.092 2.008.27 1.526-1.035 2.197-.82 2.197-.82.437 1.103.163 1.917.08 2.12.513.56.823 1.274.823 2.147 0 3.073-1.87 3.748-3.653 3.947.288.248.544.737.544 1.486 0 1.073-.01 1.94-.01 2.203 0 .214.145.461.55.382A8 8 0 008 .197z" fill="currentColor"/>
</svg>'''


st.sidebar.markdown("📬 **Contact**")
st.sidebar.markdown(f"<a class='icon-link' href='mailto:{'rjimmichan@gmail.com'}'>✉️ Email — rjimmichan@gmail.com</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"<a class='icon-link' href='{ 'https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291'}' target='_blank'>{linkedin_svg} LinkedIn</a>", unsafe_allow_html=True)
st.sidebar.markdown(f"<a class='icon-link' href='{ 'https://github.com/Robin-Jimmichan-Pooppally'}' target='_blank'>{github_svg} GitHub</a>", unsafe_allow_html=True)
st.sidebar.markdown("---")


# TTS control moved to sidebar (previously below input)
tts_toggle = st.sidebar.checkbox("🔊 Play responses (TTS)", value=False)


# Option: Save chat locally
save_local = st.sidebar.checkbox("💾 Save chat locally (chat_memory.json)", value=False)


# Erase / clear moved to sidebar for convenience
if st.sidebar.button("🧹 Clear Conversation"):
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.session_state.history = []
    # remove local file if exists and save_local is True
    try:
        if os.path.exists("chat_memory.json"):
            os.remove("chat_memory.json")
    except Exception:
        pass
    st.experimental_rerun()


# Portfolio overview with icons and highlighted counts
st.sidebar.markdown("### 📊 Portfolio Overview")
summary = context.get("summary", {})
projects_by_cat = context.get("projects", {})


# Build all_projects flattened list
all_projects = []
for cat, d in projects_by_cat.items():
    for pname, repo in d.items():
        all_projects.append((cat, pname, repo))


# Render portfolio counts with small icons
for k, v in summary.items():
    icon = "📈" if ("Excel" in k or "Power" in k) else ("🐍" if "Python" in k else "🗄️")
    st.sidebar.markdown(f"<div class='sidebar-item'>{icon} <strong>{k}</strong> <span class='count'>{v}</span></div>", unsafe_allow_html=True)


# Total projects visual separation
total_projects = sum(summary.values()) if summary else len(all_projects)
st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.03)'>", unsafe_allow_html=True)
st.sidebar.markdown(f"<div style='font-weight:700; color:var(--text);'>Total Projects: <span style='color:var(--accent);'>{total_projects}</span></div>", unsafe_allow_html=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)


# -----------------------
# Phase 2.1: Prepare projects list (flattened and grouped)
# -----------------------
# all_projects already built above


# Category filter buttons (top, horizontally) - improved visuals
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


if st.session_state.get("selected_category", "All") == "All":
    st.markdown("Showing projects: **All categories**")
else:
    st.markdown(f"Showing projects: **{st.session_state['selected_category']}**")


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
# Phase 2.2: Chat mode toggle
# -----------------------
st.markdown("---")
mode = st.radio("Chat mode", ("General Assistant", "Business Analytics Assistant"), horizontal=True)
if "chat_mode" not in st.session_state or st.session_state.get("chat_mode") != mode:
    st.session_state.chat_mode = mode
    st.session_state.history = []  # reset conversation on mode change


# -----------------------
# Phase 2.3: Groq client init (safe)
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
# Phase 2.4: Helpers: fetch README from GitHub
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
# Phase 2.5: Helper: gTTS speak
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
# Phase 2.6: Chat history initialization
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
# Phase 2.7: When project selection changes -> load README preview and reset chat for that project
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
# Phase 3: Display selected project card above chat (unchanged logic + UI polish)
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
    st.markdown(f"**Category:** {card_cat}  ")
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
# Phase 3.1: Chat UI display (new avatar + bubble differences)
# -----------------------
assistant_name = context.get('assistant_name', 'Portfoli-AI')
assistant_avatar_svg = """<svg viewBox="0 0 64 64" width="40" height="40" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="12" fill="#071014"/>
  <path d="M32 12c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm0 26c-9.941 0-18 8.059-18 18h36c0-9.941-8.059-18-18-18z" fill="#00E5FF" opacity="0.95"/>
</svg>"""


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
    ''', unsafe_allow_html=True)


# -----------------------
# Phase 3.2: Chat input form to prevent auto-resubmission
# -----------------------
with st.form(key='chat_form', clear_on_submit=True):
    user_input = st.text_input(
        "Type your message...", 
        key="user_input", 
        placeholder="Ask me anything...",
        label_visibility="collapsed"
    )
    submit_button = st.form_submit_button("Send")

# Only process if the form was actually submitted with some input
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
        try:
            speak_text(bot_text)
        except Exception:
            st.warning("TTS failed for this response.")

    # Rerun to update the UI
    st.experimental_rerun()

# -----------------------
# Phase 3.3: Local save helper (if enabled)
# -----------------------
def save_chat_local(history):
    try:
        with open("chat_memory.json", "w", encoding="utf-8") as fh:
            json.dump(history, fh, ensure_ascii=False, indent=2)
    except Exception:
        # don't crash the app if local save fails
        pass

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
                bot_text = " Received empty response from Groq."

        except Exception as e:
            bot_text = f" Groq API error: {e}"

    # Append assistant response
    st.session_state.history.append({"role": "assistant", "content": bot_text})

    # Optional: save locally after assistant reply
    if save_local:
        save_chat_local(st.session_state.history)


    # TTS (plays if toggled in sidebar)
    if tts_toggle:
        try:
            speak_text(bot_text)
        except Exception:
            st.warning("TTS failed for this response.")


    # Rerun to clear the input field (keeps behavior consistent)
    st.experimental_rerun()


# -----------------------
# Phase 4: Footer / credits
# -----------------------
st.markdown("---")
st.markdown("<div class='small-muted'>Built with ❤️ • Portfoli-AI • Contact: rjimmichan@gmail.com</div>", unsafe_allow_html=True)
