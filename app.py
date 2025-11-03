import streamlit as st
from groq import Groq
import requests
import pandas as pd
from gtts import gTTS
import base64
import io

# --- Page Config ---
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# --- Header ---
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
        "<h2 style='text-align:center;'>🤖 Portfoli-AI — Robin Jimmichan’s Portfolio Assistant</h2>",
        unsafe_allow_html=True
    )
with col2:
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []
        st.session_state["mode"] = "Portfolio"
        st.rerun()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "mode" not in st.session_state:
    st.session_state["mode"] = "Portfolio"

# --- Greeting ---
if not st.session_state["chat_history"]:
    st.markdown("👋 **Hey Robin!** I’m your AI-powered portfolio assistant — ask me about your projects or anything in Business Analytics.")

# --- Sidebar: Info ---
st.sidebar.markdown("### 👤 Robin Jimmichan")
st.sidebar.markdown("[📧 Email](mailto:rjimmichan@gmail.com)")
st.sidebar.markdown("[💼 LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
st.sidebar.markdown("[🐙 GitHub](https://github.com/Robin-Jimmichan-Pooppally)")

# --- Sidebar: Mode Switch ---
st.sidebar.markdown("### 🧠 Assistant Mode")
mode_choice = st.sidebar.radio("Select mode:", ["Portfolio Guide", "Business Analytics Expert"])
st.session_state["mode"] = "Portfolio" if mode_choice == "Portfolio Guide" else "Business Analytics"

# --- GitHub Repo Fetch ---
@st.cache_data(show_spinner=False)
def fetch_repos(user):
    url = f"https://api.github.com/users/{user}/repos"
    r = requests.get(url)
    if r.status_code == 200:
        repos = r.json()
        filtered = [repo for repo in repos if any(k in repo["name"].lower() for k in ["project", "dashboard", "analysis"])]
        return {repo["name"]: repo["html_url"] for repo in filtered}
    else:
        return {}

repos = fetch_repos("Robin-Jimmichan-Pooppally")

# --- Project Selection ---
if repos:
    st.markdown("### 📂 Choose a Project Repository")
    project_name = st.selectbox("Select a project:", list(repos.keys()))
    project_url = repos[project_name]
    st.markdown(f"[🔗 Open {project_name}]({project_url})")

# --- Groq Client Setup ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🚨 Groq API Key not found! Please add it under Settings → Secrets as GROQ_API_KEY.")
    st.stop()

# --- Chat Input ---
user_input = st.chat_input("Ask me anything about your projects or Business Analytics...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    # Determine mode context
    context_prompt = (
        "You are Robin Jimmichan’s AI Portfolio Assistant. "
        "You help explain his GitHub projects (Excel, Power BI, Python, SQL). "
        "Give structured, professional, and beginner-friendly answers."
        if st.session_state["mode"] == "Portfolio"
        else "You are a Business Analytics AI expert helping with analytics, dashboards, and insights."
    )

    # --- Groq API Call ---
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": context_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"⚠️ API error: {e}"

    st.session_state["chat_history"].append({"user": user_input, "bot": bot_reply})

    # --- Display Assistant Message ---
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

        # --- Text-to-Speech (optional play button) ---
        try:
            tts = gTTS(bot_reply)
            tts_io = io.BytesIO()
            tts.save(tts_io)
            tts_io.seek(0)
            b64 = base64.b64encode(tts_io.read()).decode()
            audio_html = f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(audio_html, unsafe_allow_html=True)
        except Exception:
            pass

# --- Chat History ---
if st.session_state["chat_history"]:
    st.markdown("### 💬 Chat History")
    for chat in st.session_state["chat_history"]:
        st.markdown(f"**You:** {chat['user']}")
        st.markdown(f"**AI:** {chat['bot']}")
