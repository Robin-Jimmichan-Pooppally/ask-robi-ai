import streamlit as st
from groq import Groq
import json
from robi_context import context
import time

# ==============================
# 💡 App Configuration
# ==============================
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# ==============================
# 🎨 Custom Styling (Neon Frosted Glass)
# ==============================
st.markdown("""
    <style>
        body {
            background: radial-gradient(circle at 50% 50%, #000000 0%, #050505 100%);
            color: #fff;
        }
        .main {
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(0, 180, 255, 0.3);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0px 0px 30px rgba(0, 180, 255, 0.2);
        }
        .stButton button {
            background-color: rgba(0, 180, 255, 0.15);
            border: 1px solid rgba(0, 180, 255, 0.5);
            color: #00b4ff;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: rgba(0, 180, 255, 0.35);
            color: white;
            border-color: rgba(0, 180, 255, 0.8);
        }
        .chat-bubble {
            border-radius: 15px;
            padding: 10px 15px;
            margin: 8px 0;
            animation: fadeIn 0.5s ease-in-out;
        }
        .user {
            background-color: rgba(0, 180, 255, 0.2);
            border: 1px solid rgba(0, 180, 255, 0.5);
            align-self: flex-end;
        }
        .bot {
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(0, 180, 255, 0.3);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# ==============================
# 🔑 Initialize Groq Client
# ==============================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==============================
# 💬 Chatbot Greeting
# ==============================
st.title("🤖 Portfoli-AI")
st.markdown("### Your interactive Business Analytics portfolio assistant")
st.markdown("---")

# Display greeting message
with st.expander("👋 Click to read Portfoli-AI's introduction", expanded=False):
    st.markdown(context["greeting_message"])

# ==============================
# 🧩 Project Category Filters
# ==============================
st.markdown("### 🔍 Explore by Project Category")
categories = list(context["projects"].keys())
selected_category = st.radio("Select a project type:", categories, horizontal=True)

if selected_category:
    st.markdown(f"#### 📁 {selected_category} Projects")
    for name, link in context["projects"][selected_category].items():
        st.markdown(f"- [{name}]({link})")

st.markdown("---")

# ==============================
# 🧠 Chat Memory
# ==============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": context["greeting_message"]}
    ]

# ==============================
# 💭 Chat UI
# ==============================
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble user'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble bot'><b>{context['assistant_name']}:</b> {msg['content']}</div>", unsafe_allow_html=True)

# ==============================
# 🗣️ User Input
# ==============================
user_input = st.chat_input("Ask about Robin’s projects...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Query context before calling model
    system_context = f"""
    You are {context['assistant_name']}, a portfolio assistant for {context['owner_name']} ({context['owner_role']}).
    Respond ONLY using data available in context.
    If unsure, reply with: 'That specific detail isn’t available right now in Robin’s repository.'
    """

    # Prepare conversation history
    chat_history = [{"role": "system", "content": system_context}]
    chat_history.extend(st.session_state.messages)

    # Generate response via Groq
    with st.spinner("Thinking..."):
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=chat_history,
            temperature=0.3,
            max_tokens=800,
        )

    bot_reply = completion.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    # Display updated conversation
    st.experimental_rerun()
