import streamlit as st
from openai import OpenAI
from robi_context import context

# --------------------------
# 🔧 APP CONFIGURATION
# --------------------------
st.set_page_config(page_title="Portfoli-AI | Robin Jimmichan", page_icon="🤖", layout="centered")

# --------------------------
# 🎨 CUSTOM CSS (Dark Frosted Glass UI)
# --------------------------
st.markdown("""
    <style>
    body {
        background: radial-gradient(circle at top left, #0a0a0a, #111);
        color: #eaeaea;
    }
    .stChatMessage {
        background: rgba(25, 25, 25, 0.6);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 14px;
        margin: 8px 0;
        color: #fff;
        animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(10px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .chat-bubble {
        border-radius: 18px;
        padding: 12px 16px;
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 0 10px rgba(0,255,255,0.2);
    }
    h1 {
        text-align: center;
        color: #00ffff;
        text-shadow: 0 0 12px #00ffff;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# ⚙️ LOAD MODEL CLIENT
# --------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --------------------------
# 🚀 APP HEADER
# --------------------------
st.title("🤖 Portfoli-AI")
st.caption(f"Meet {context['owner_name']}’s intelligent portfolio assistant")

# --------------------------
# 💬 CHAT SETUP
# --------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    # Auto-greet when app starts
    st.session_state["messages"].append({"role": "assistant", "content": context["greeting_message"]})

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(f"<div class='chat-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

# --------------------------
# ✏️ USER INPUT
# --------------------------
prompt = st.chat_input("Ask about Robin’s projects...")

if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-bubble'>{prompt}</div>", unsafe_allow_html=True)

    # Build the full prompt for the model
    full_prompt = f"{context['persona']}\n\nUser question: {prompt}\n\nUse only verified info from context below:\n{context}"

    with st.chat_message("assistant"):
        with st.spinner("Analyzing Robin’s portfolio..."):
            response = client.chat.completions.create(
                model="gpt-5",
                messages=[{"role": "system", "content": full_prompt}],
                temperature=0.2
            )
            answer = response.choices[0].message.content
            st.markdown(f"<div class='chat-bubble'>{answer}</div>", unsafe_allow_html=True)

    st.session_state["messages"].append({"role": "assistant", "content": answer})
