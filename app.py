"""
Portfoli-AI — Streamlit app (Groq + Enhanced Intelligence + Context-Aware)
Requirements: see requirements.txt
Place robi_context.py (enhanced context with 21 projects) in same folder.
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

# Import your enhanced context (21 projects - no hallucination)
from robi_context import context

# -----------------------
# Helper: Build intelligent system prompt
# -----------------------
def build_intelligent_system_prompt(chat_mode, selected_project=None):
    """
    Build enhanced system prompt with deep project knowledge.
    Prevents hallucination by grounding in actual context data.
    """
    
    # Base instruction - firm on accuracy
    base_prompt = f"""You are {context.get('assistant_name', 'Portfoli-AI')}, intelligent portfolio assistant for {context.get('owner_name')}.

**CRITICAL: ACCURACY REQUIREMENT**
- ONLY use data from the knowledge base below
- NEVER invent metrics, formulas, or project details
- If information is not in knowledge base, say: "That specific detail isn't available in Robin's repository"
- Be specific: use exact numbers, exact project names, exact formulas
- Admit uncertainty rather than guess

**ROBIN'S PORTFOLIO SUMMARY**
- Total Projects: 21 (Excel: 6, Power BI: 5, Python: 4, SQL: 6)
- Total Records Analyzed: 185,000+
- Industries: E-commerce, Healthcare, Finance, Telecom, Retail, Supply Chain
- Data Span: 2019-2025

**CORE PROJECTS DATA:**
"""
    
    # Add project details for context awareness
    for category, projects in context.get("projects_detailed", {}).items():
        base_prompt += f"\n{category.upper()} PROJECTS:\n"
        for proj_name, proj_data in projects.items():
            base_prompt += f"- {proj_name}: {proj_data.get('dataset_size', 'N/A')}. "
            if 'key_metrics' in proj_data:
                metrics = proj_data['key_metrics']
                if isinstance(metrics, dict):
                    sample_metrics = list(metrics.items())[:2]
                    base_prompt += f"Key metrics: {', '.join([f'{k}={v}' for k,v in sample_metrics])}. "
            base_prompt += f"GitHub: {proj_data.get('url', 'N/A')}\n"
    
    if chat_mode == "Business Analytics Assistant":
        base_prompt += """
**BUSINESS ANALYTICS MODE**
Focus on:
- Specific metrics and KPIs from projects
- Business impact and ROI
- Industry patterns and insights
- Data-driven recommendations
- Exact formulas/queries when requested
"""
    else:
        base_prompt += """
**GENERAL ASSISTANT MODE**
- Relate back to Robin's expertise when relevant
- Discuss analytics methodologies
- Explain project approaches
- Maintain professional tone
"""
    
    if selected_project:
        # Add specific project context if user selected one
        project_name, project_category = "Unknown", "N/A"
        project_details = {}
        
        for cat, projs in context.get("projects_detailed", {}).items():
            for pname, pdata in projs.items():
                if pdata.get('url') == selected_project:
                    project_name = pname
                    project_category = cat
                    project_details = pdata
                    break
        
        base_prompt += f"""

**CURRENT PROJECT CONTEXT**
Name: {project_name}
Category: {project_category}
URL: {selected_project}

Available data on this project:
- Dataset: {project_details.get('dataset_size', 'Not specified')}
- Objective: {project_details.get('objective', 'Not specified')}
- Key Metrics: {json.dumps(project_details.get('key_metrics', {}), indent=2)}
- Techniques: {', '.join(project_details.get('techniques', []))}
- Business Impact: {project_details.get('business_impact', 'Not specified')}

When answering, prioritize insights from THIS project.
"""
    
    base_prompt += """

**RESPONSE GUIDELINES**
1. Use EXACT project names: "Telco Customer Churn Analysis" not "Telecom project"
2. Quote EXACT metrics: "26.54% churn rate" not "around 25%"
3. Provide EXACT code when asked: DAX formulas, SQL queries, Python code
4. Explain the "why" behind technical choices
5. Link insights to business outcomes
6. Keep responses 150-500 words (concise but thorough)

**IF ASKED FOR:**
- Code/Formulas: Provide exact snippets from projects
- Project Details: Cite dataset size, key metrics, GitHub link
- Comparison: Use actual numbers from multiple projects
- Methodology: Explain exact techniques used (K-Means, ARIMA, DAX, etc.)
- Business Impact: Reference specific outcomes ($, %, improvements)

**ABSOLUTE RULES:**
- Never say "probably" or "likely" without data
- Never invent dataset sizes, metrics, or results
- Never hallucinate formulas or code
- Always ground answers in the 21 projects listed above
- When uncertain, ask for clarification or admit gap
"""
    
    return base_prompt.strip()


def classify_user_query(query_text):
    """
    Classify query to determine response strategy.
    Returns: {'type': 'code'|'metrics'|'explanation'|'comparison'|'general', 'context': {...}}
    """
    query_lower = query_text.lower()
    
    # Code extraction queries
    code_patterns = {
        'dax': r'\b(dax|measure|measures?)\b',
        'sql': r'\b(sql|query|select|where|join)\b',
        'python': r'\b(python|script|\.py|import|def|pandas|sklearn)\b',
        'formula': r'\b(formula|equation|function)\b'
    }
    
    # Metrics queries
    metrics_patterns = r'\b(metric|rate|average|total|percentage|churn|revenue|profit)\b'
    
    # Comparison queries
    comparison_patterns = r'\b(vs|versus|compare|difference|better|similar)\b'
    
    # Classification logic
    for code_type, pattern in code_patterns.items():
        if re.search(pattern, query_lower):
            return {'type': 'code', 'language': code_type}
    
    if re.search(comparison_patterns, query_lower):
        return {'type': 'comparison'}
    
    if re.search(metrics_patterns, query_lower):
        return {'type': 'metrics'}
    
    if any(word in query_lower for word in ['explain', 'how', 'why', 'understand', 'tell me']):
        return {'type': 'explanation'}
    
    return {'type': 'general'}


def extract_code_blocks_from_readme(readme_text):
    """
    Extract fenced code blocks from README using literal regex.
    Returns list of {'lang': 'python'|'sql'|'dax'|..., 'code': '...'}
    """
    blocks = []
    if not readme_text:
        return blocks
    
    # Matches ```lang\n...``` fenced code blocks
    pattern = re.compile(r"```([\w\-\+]+)?\n(.*?)```", re.DOTALL | re.IGNORECASE)
    
    for m in pattern.finditer(readme_text):
        lang = (m.group(1) or "").strip().lower()
        code = m.group(2).rstrip()
        blocks.append({"lang": lang, "code": code})
    
    return blocks


def detect_requested_lang(user_text):
    """Detect if user is asking for specific code language."""
    u = user_text.lower()
    
    code_keyword_map = {
        "dax": ["dax", "measure", "measures", "powerbi", "power bi"],
        "sql": ["sql", "query", "select", "where", "join"],
        "python": ["python", "py", ".py", "script", "import"],
        "m": ["m query", "powerquery", "m-query"],
    }
    
    for lang, keys in code_keyword_map.items():
        for k in keys:
            if k in u:
                return lang
    return None


def find_code_blocks_for_lang(lang):
    """Return list of code strings matching language."""
    blocks = st.session_state.get("code_blocks", []) or []
    
    if not lang:
        return blocks
    
    matches = [b for b in blocks if b.get("lang", "") == lang]
    
    if not matches and lang == "m":
        matches = [b for b in blocks if b.get("lang", "") in ("m", "powerquery")]
    
    return matches


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
if "code_blocks" not in st.session_state: st.session_state.code_blocks = []
if "response_cache" not in st.session_state: st.session_state.response_cache = {}

# -----------------------
# Colors & links
# -----------------------
ACCENT = "#00bfff"
HOVER_ACCENT = "#007acc"
GITHUB_URL = "https://github.com/Robin-Jimmichan-Pooppally"
LINKEDIN_URL = "https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291"
EMAIL = "rjimmichan@gmail.com"

# Robot logo SVG (unchanged)
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
# Sticky Header (EXACT - unchanged)
# -----------------------
st.markdown(f"""
    <style>
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
# Global CSS (EXACT - unchanged)
# -----------------------
st.markdown(f"""
<style>
body {{ background: transparent; color:#e8f7ff; font-size:16px; line-height:1.6; scroll-behavior:smooth; }}
h1,h2,h3 {{ color:var(--accent); text-shadow:0 0 12px var(--accent); }}

@keyframes fadeInUp {{
  0% {{ opacity: 0; transform: translateY(8px); }}
  100% {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulseGlow {{
  0% {{ box-shadow: 0 6px 16px rgba(0,0,0,0.2), 0 0 0 0 rgba(0,191,255,0.0); }}
  50% {{ box-shadow: 0 8px 28px rgba(0,0,0,0.25), 0 0 24px rgba(0,191,255,0.06); }}
  100% {{ box-shadow: 0 6px 16px rgba(0,0,0,0.2), 0 0 0 0 rgba(0,191,255,0.0); }}
}}
.chat-bubble-user, .chat-bubble-bot {{
  padding:12px 16px; border-radius:14px; margin:10px 0;
  transition: background 0.22s ease, transform 0.18s ease, box-shadow 0.18s ease;
  animation: fadeInUp .35s ease both;
}}
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

button.stButton>button {{
  border-radius:10px; transition: all 0.18s ease-in-out;
  border: 1px solid var(--accent)22;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.00));
}}
button.stButton>button:hover {{
  transform: translateY(-2px);
  box-shadow: 0 10px 30px var(--accent)22;
  border-color: var(--hover-accent);
  background: linear-gradient(180deg, rgba(0,191,255,0.1), rgba(0,191,255,0.05));
}}

.stSelectbox [data-baseweb="select"], select {{
  border-color: var(--accent) !important; box-shadow: 0 0 18px var(--accent)15 !important;
  accent-color: var(--accent);
}}
input[type="radio"], input[type="checkbox"], select {{
  accent-color: var(--accent);
}}

/* Radio button blue styling */
[data-testid="stRadio"] {{
  color: var(--accent);
}}
[data-testid="stRadio"] label {{
  color: #e8f7ff;
}}
[data-testid="stRadio"] [role="radio"] {{
  accent-color: var(--accent) !important;
  border-color: var(--accent) !important;
}}
[data-testid="stRadio"] input[type="radio"] {{
  accent-color: var(--accent) !important;
}}

/* Category buttons - remove red on hover/select */
button {{
  background-color: transparent !important;
}}
button:hover {{
  background-color: rgba(0, 191, 255, 0.1) !important;
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}}
button:focus {{
  background-color: rgba(0, 191, 255, 0.1) !important;
  border-color: var(--accent) !important;
  color: var(--accent) !important;
}}
button[kind="secondary"]:hover {{
  background-color: rgba(0, 191, 255, 0.15) !important;
  border: 1px solid var(--accent) !important;
  color: var(--accent) !important;
}}
.stSelectbox {{
  color: #e8f7ff;
}}
.stSelectbox [data-baseweb="select"] {{
  border: 1px solid var(--accent) !important;
  box-shadow: 0 0 18px var(--accent)15 !important;
}}
.stSelectbox svg {{
  fill: var(--accent) !important;
}}

.selected-project-label {{ color: var(--accent); font-weight:700; }}

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
.social-btn svg {{
  width:18px; height:18px; display:block;
  stroke: var(--accent); fill: none; stroke-width:1.6; stroke-linecap:round; stroke-linejoin:round;
}}
.sidebar-robot svg {{ width:44px; height:44px; stroke: var(--accent); fill: none; stroke-width:1.6; }}

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

@media (max-width: 600px) {{
  .header-title {{ font-size: 18px; }}
  .footer-icons {{ gap:10px; }}
}}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Sidebar (EXACT - unchanged structure, enhanced logic)
# -----------------------
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

# Controls section
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### ⚙️ Controls")
tts_sidebar = st.sidebar.checkbox("🔊 Play responses (TTS)", key="tts_sidebar", value=False)

if st.sidebar.button("🧹 Clear Chat History"):
    st.session_state.awaiting_clear = True

if st.session_state.get("awaiting_clear", False):
    st.sidebar.warning("Are you sure? This cannot be undone.")
    c1, c2 = st.sidebar.columns(2)
    if c1.button("Yes, clear"):
        st.session_state.history = []
        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.awaiting_clear = False
        st.rerun()
    if c2.button("No, cancel"):
        st.session_state.awaiting_clear = False

if st.sidebar.button("💾 Save Chat History"):
    history_json = json.dumps(st.session_state.get("history", []), indent=2)
    st.sidebar.download_button("Download JSON", history_json, file_name="chat_history.json", mime="application/json")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Portfolio overview
st.sidebar.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.sidebar.markdown("### 📊 Portfolio Overview")
for k, v in context.get("summary", {}).items():
    st.sidebar.markdown(f"- **{k}**: {v}")
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# Projects & Filtering (EXACT - unchanged)
# -----------------------
projects_by_cat = context.get("projects_detailed", {})
all_projects = []
for cat, d in projects_by_cat.items():
    for pname, repo_data in d.items():
        all_projects.append((cat, pname, repo_data.get('url')))

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

st.markdown("---")
mode = st.radio("Chat mode", ("General Assistant", "Business Analytics Assistant"), horizontal=True)
if "chat_mode" not in st.session_state or st.session_state.get("chat_mode") != mode:
    st.session_state.chat_mode = mode
    st.session_state.history = []

# -----------------------
# Groq initialization
# -----------------------
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Missing Groq API key. Add GROQ_API_KEY to Streamlit secrets.")
        st.stop()
    try:
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Groq: {e}")
        st.stop()

client = init_groq()

# -----------------------
# README fetch helper
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
# TTS helper
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
# Project selection & README loading
# -----------------------
if "selected_project" not in st.session_state: st.session_state.selected_project = None
if "readme_full" not in st.session_state: st.session_state.readme_full = None
if "readme_preview" not in st.session_state: st.session_state.readme_preview = None
if "show_more" not in st.session_state: st.session_state.show_more = False

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
        st.session_state.code_blocks = extract_code_blocks_from_readme(st.session_state.readme_full)
        st.session_state.show_more = False

# Display selected project card
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
# Display chat history
# -----------------------
for m in st.session_state.history:
    role, text = m.get("role"), m.get("content")
    if role == "user":
        st.markdown(f"<div class='chat-bubble-user' aria-label='User message'><b>You:</b> {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot' aria-label='Assistant message'><b>{context.get('assistant_name','Portfoli-AI')}:</b> {text}</div>", unsafe_allow_html=True)

# -----------------------
# Chat input & processing
# -----------------------
tts_toggle = st.session_state.get("tts_sidebar", False)

user_input = st.chat_input("Type your message and press Enter...")

if user_input:
    # Add to history immediately
    st.session_state.history.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='chat-bubble-user' aria-label='User message'><b>You:</b> {user_input}</div>", unsafe_allow_html=True)
    
    # Classify query for intelligent routing
    query_classification = classify_user_query(user_input)
    requested_lang = detect_requested_lang(user_input)
    code_matches = []
    
    if requested_lang:
        code_matches = find_code_blocks_for_lang(requested_lang)
    
    # If user explicitly asked for code and we have matches
    if requested_lang and code_matches and query_classification['type'] == 'code':
        st.markdown(f"<div class='code-bubble'><b>Exact `{requested_lang}` snippet(s) from README:</b>\n\n", unsafe_allow_html=True)
        for idx, blk in enumerate(code_matches[:5], start=1):
            lang_label = blk.get("lang") or "code"
            code_text = blk.get("code", "")
            st.markdown(f"<div class='code-bubble'><b>Snippet {idx} — {lang_label}</b>\n\n```{lang_label}\n{code_text}\n```</div>", unsafe_allow_html=True)
        
        st.session_state.history.append({"role": "assistant", "content": f"Displayed {len(code_matches[:5])} {requested_lang} snippet(s) from README."})
        
        if tts_toggle:
            speak_text(f"Displayed {len(code_matches[:5])} {requested_lang} snippet{'s' if len(code_matches)>1 else ''} from the README.")
    else:
        # Use intelligent Groq response
        system_prompt = build_intelligent_system_prompt(st.session_state.chat_mode, st.session_state.get("selected_project"))
        
        # Add context awareness: mention if user is asking about selected project
        enhanced_user_msg = user_input
        if st.session_state.get("selected_project"):
            for c, name, url in all_projects:
                if url == st.session_state.get("selected_project"):
                    enhanced_user_msg = f"[Regarding: {name} project] {user_input}"
                    break
        
        messages = [
            {"role": "system", "content": system_prompt},
            *[{"role": ("user" if h["role"] == "user" else "assistant"), "content": h["content"]}
              for h in st.session_state.history[-8:]]
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
        
        # Display response
        st.markdown(f"<div class='chat-bubble-bot' aria-label='Assistant message'><b>{context.get('assistant_name','Portfoli-AI')}:</b> {bot_text}</div>", unsafe_allow_html=True)
        st.session_state.history.append({"role": "assistant", "content": bot_text})
        
        # TTS
        if tts_toggle:
            speak_text(bot_text)

# -----------------------
# Footer (EXACT - unchanged)
# -----------------------
with st.sidebar:
    st.markdown("")
    st.markdown("""
    <div style='display:flex; justify-content:center; gap:20px; margin-top:10px;'>
        <a href="https://github.com/Robin-Jimmichan-Pooppally" target="_blank" style="text-decoration:none;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="28" style="filter: drop-shadow(0 0 8px #00ffff);">
        </a>
        <a href="https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291/" target="_blank" style="text-decoration:none;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="28" style="filter: drop-shadow(0 0 8px #00ffff);">
        </a>
        <a href="mailto:rjimmichan@gmail.com" target="_blank" style="text-decoration:none;">
            <img src="https://img.icons8.com/ios-filled/50/ffffff/new-post.png" width="28" style="filter: drop-shadow(0 0 8px #00ffff);">
        </a>
    </div>
    """, unsafe_allow_html=True)

# End of file
