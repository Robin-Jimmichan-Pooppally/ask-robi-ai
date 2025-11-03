import streamlit as st
from groq import Groq
from robi_context import ROBIN_GREETING, ROBIN_CONTEXT, PROJECTS, PROJECT_SUMMARY

# ------------------ Groq Setup ------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Portfoli-AI | Robin’s Portfolio Assistant",
    page_icon="💙",
    layout="wide"
)

# ------------------ Custom CSS ------------------
st.markdown("""
<style>
/* Global layout */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #000000 0%, #0a0a0f 100%);
    color: #e0f0ff;
    font-family: 'Poppins', sans-serif;
}

/* Neon header */
h1, h2, h3, h4 {
    color: #00bfff;
    text-shadow: 0 0 12px #00bfff;
}

/* Chat containers */
.chat-bubble-user, .chat-bubble-bot {
    border-radius: 20px;
    padding: 15px 20px;
    margin: 8px 0;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0,191,255,0.3);
    box-shadow: 0 0 10px rgba(0,191,255,0.2);
}
.chat-bubble-user {
    background: rgba(0,191,255,0.1);
    color: #00bfff;
    align-self: flex-end;
}
.chat-bubble-bot {
    background: rgba(255,255,255,0.05);
    color: #e0f0ff;
    align-self: flex-start;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(15px);
    border-right: 2px solid rgba(0,191,255,0.3);
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #001f33, #003366);
    color: #00bfff;
    border: 1px solid #00bfff;
    border-radius: 10px;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(0,191,255,0.4);
}
div.stButton > button:hover {
    background: #00bfff;
    color: #000;
    box-shadow: 0 0 20px #00bfff;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ------------------ UI Header ------------------
st.markdown("<h1 style='text-align:center;'>💙 Portfoli-AI — Robin’s Intelligent Portfolio Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#9edbff;'>Explore verified Excel, SQL, Power BI, and Python projects with real code, logic, and insights.</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ Sidebar ------------------
st.sidebar.image("https://avatars.githubusercontent.com/u/167973515?v=4", width=100)
st.sidebar.markdown("### 🔗 Connect")
st.sidebar.markdown("""
- [GitHub](https://github.com/Robin-Jimmichan-Pooppally)
- [LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)
- 📧 rjimmichan@gmail.com
""")
st.sidebar.markdown("---")

# ------------------ Category Filter ------------------
categories = ["All", "Excel", "Power BI", "SQL", "Python"]
selected_category = st.sidebar.radio("🧩 Filter by Category", categories)

# Filter projects
filtered_projects = PROJECTS if selected_category == "All" else [p for p in PROJECTS if p["category"] == selected_category]

# ------------------ Display Projects ------------------
st.subheader(f"📁 Showing {len(filtered_projects)} {selected_category} Projects")

for proj in filtered_projects:
    with st.container():
        st.markdown(f"""
        <div class='chat-bubble-bot'>
            <b>{proj['name']}</b><br>
            <small><i>{proj['short']}</i></small><br>
            🔗 <a href='{proj['repo']}' target='_blank' style='color:#00bfff;'>View on GitHub</a>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ------------------ Chat Section ------------------
st.subheader("💬 Chat with Portfoli-AI")

if "history" not in st.session_state:
    st.session_state.history = [{"role": "assistant", "content": ROBIN_GREETING}]

# Display chat history
for chat in st.session_state.history:
    if chat["role"] == "assistant":
        st.markdown(f"<div class='chat-bubble-bot'>{chat['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-user'>{chat['content']}</div>", unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask about a project, dataset, or formula...")
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": ROBIN_CONTEXT},
                *st.session_state.history
            ]
        )
        answer = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": answer})
        st.experimental_rerun()
