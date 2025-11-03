import streamlit as st
import os
import random
from groq import Groq
import tempfile
import pyttsx3
from robi_context import ROBIN_CONTEXT, ROBIN_GREETING, PROJECTS as PROJECTS_INDEX, PROJECT_SUMMARY as PROJECTS_SUMMARY_TABLE

# --- APP CONFIG ---
st.set_page_config(page_title="Portfoli-AI | Robin Jimmichan", page_icon="🤖", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #FAFAFA;
    font-family: 'Poppins', sans-serif;
}
h1, h2, h3, h4 {
    color: #00C3FF;
}
.sidebar .sidebar-content {
    background-color: #0E1117;
}
[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🤖 Portfoli-AI | Robin Jimmichan’s Interactive Portfolio Assistant")
st.caption("Ask me anything about Robin’s projects, dashboards, and skills.")

# --- PROJECTS SHOWCASE ---
st.header("📁 Featured Projects")
cols = st.columns(3)

for i, proj in enumerate(PROJECTS_INDEX):
    with cols[i % 3]:
        st.markdown(f"### {proj['emoji']} {proj['id']}")
        st.write(proj['desc'])
        c1, c2 = st.columns([2, 1])
        with c1:
            if st.button("🔗 Open Repo", key=f"open_{proj['id']}"):
                st.write(f"[Open repository]({proj['repo']})")
        with c2:
            st.caption(proj['type'])

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# --- CHAT INTERFACE SETUP ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": ROBIN_CONTEXT},
        {"role": "assistant", "content": ROBIN_GREETING}
    ]

# --- TTS FUNCTION (CACHED) ---
def speak_text_cached(text):
    temp_path = os.path.join(tempfile.gettempdir(), f"tts_{random.randint(1, 9999)}.mp3")
    engine = pyttsx3.init()
    engine.save_to_file(text, temp_path)
    engine.runAndWait()
    return temp_path

# --- DISPLAY CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- USER INPUT ---
user_input = st.chat_input("Type your question about Robin’s portfolio...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # --- AI RESPONSE LOGIC ---
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        client = Groq(api_key=groq_api_key)
        try:
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=st.session_state.messages,
                temperature=0.7,
                max_tokens=800,
                top_p=1
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ Groq API error: {e}"
    else:
        reply = "👋 Hey there! I can’t reach Groq servers right now, but here’s a summary: this chatbot helps you explore Robin’s analytics projects, dashboards, and code samples interactively."

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)
        st.audio(speak_text_cached(reply))

    # Store message
    st.session_state.messages.append({"role": "assistant", "content": reply})

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/150340474?v=4", width=140)
    st.markdown("### 🧠 About Robin Jimmichan")
    st.write("Business Analyst | Data Enthusiast | Excel • SQL • Power BI • Python")
    st.write("Building insights from data and automating smarter solutions.")
    st.markdown("---")
    st.subheader("🗂️ Project Summary")
    st.dataframe(PROJECTS_SUMMARY_TABLE, use_container_width=True)
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit + Groq API + Portfoli-AI Context Engine.")
