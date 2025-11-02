"""
Robi.AI - Production Chatbot with 21 Projects
Streaming responses, Dark Theme, Complete Project Database
"""

import streamlit as st
from groq import Groq
import time
from datetime import datetime
import base64

# Import context from separate file
from robi_context import ROBIN_CONTEXT

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Ask Robi.AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== SAMPLE QUESTIONS ====================
SAMPLE_QUESTIONS = [
    "How did Robin achieve 92% forecasting accuracy?",
    "Tell me about the Loan Default Risk project",
    "What are the key findings in the Loan Default Risk analysis?",
    "Explain the E-commerce Funnel Analysis",
    "Show me all SQL projects",
    "What Python projects has Robin done?",
    "Compare Excel vs Power BI projects",
    "What's the biggest business impact achieved?",
    "Explain the RFM segmentation approach",
    "Tell me about healthcare analytics work"
]

# ==================== SESSION STATE ====================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thinking_active" not in st.session_state:
    st.session_state.thinking_active = False

if "api_error_count" not in st.session_state:
    st.session_state.api_error_count = 0

if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = False

# ==================== GROQ CLIENT ====================
@st.cache_resource
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            st.error("❌ GROQ_API_KEY is empty in Streamlit Cloud Secrets!")
            st.stop()
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Groq Connection Error: {str(e)}")
        st.info("Make sure your GROQ_API_KEY is correct in Streamlit Cloud Secrets")
        st.stop()

try:
    client = init_groq()
except Exception as e:
    st.error(f"Failed to initialize: {str(e)}")
    st.stop()

# ==================== TTS FUNCTION ====================
def speak_response(text):
    """Use browser's native Web Speech API with male voice"""
    try:
        # JavaScript for Web Speech API with male voice
        js_code = f"""
        <script>
            var text = `{text}`;
            var utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.0;
            utterance.pitch = 0.8;
            utterance.volume = 1.0;
            
            // Set male voice
            var voices = speechSynthesis.getVoices();
            for(var i = 0; i < voices.length; i++) {{
                if(voices[i].name.includes('Male') || voices[i].name.includes('David') || voices[i].name.includes('Mark')) {{
                    utterance.voice = voices[i];
                    break;
                }}
            }}
            
            speechSynthesis.cancel();
            speechSynthesis.speak(utterance);
        </script>
        """
        return js_code
    except Exception as e:
        return None

# ==================== STREAMING RESPONSE ====================
def stream_llm_response(prompt: str, placeholder) -> tuple:
    """Stream LLM response with error handling"""
    st.session_state.thinking_active = True
    
    try:
        with st.spinner("🚀 Connecting to AI..."):
            time.sleep(0.3)
        
        messages_for_api = [
            {"role": "system", "content": ROBIN_CONTEXT},
            *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[1:]]
        ]
        
        full_response = ""
        response_placeholder = placeholder.empty()
        
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages_for_api,
                temperature=0.7,
                max_tokens=1500,
                top_p=0.9,
                stream=True,
                timeout=45
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    token = chunk.choices[0].delta.content
                    full_response += token
                    with response_placeholder.container():
                        st.markdown(full_response + "▌")
            
            with response_placeholder.container():
                st.markdown(full_response)
            
            st.session_state.thinking_active = False
            st.session_state.api_error_count = 0
            return full_response, None
            
        except Exception as stream_error:
            st.session_state.thinking_active = False
            error_msg = f"Stream Error: {str(stream_error)}"
            
            with response_placeholder.container():
                st.error(f"🚨 Connection interrupted. Please try again.")
            
            st.session_state.api_error_count += 1
            return None, error_msg
    
    except Exception as e:
        st.session_state.thinking_active = False
        error_msg = f"Connection Error: {str(e)}"
        
        with placeholder.container():
            st.error(f"🚨 Oops! I seem to have lost my connection. Please try again in a moment.")
        
        st.session_state.api_error_count += 1
        return None, error_msg

# ==================== MAIN UI ====================
st.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2.5rem;">🤖 Ask Robi.AI</h1>
        <p style="color: #f0f0f0; margin-top: 0.5rem;">Your Interactive Guide to Robin's 21 Business Analytics Projects</p>
        <p style="color: #e0e0e0; margin-top: 1rem; font-size: 0.9rem;">Powered by Groq Llama 3.3 • Streaming ⚡</p>
    </div>
""", unsafe_allow_html=True)

st.write("👋 Hi! I'm Robin's AI assistant. Ask me about his **21 projects** across **Excel, SQL, Power BI, and Python**!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Robin's projects..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    response_placeholder = st.empty()
    
    with st.chat_message("assistant", avatar="🤖"):
        response_text, error = stream_llm_response(prompt, response_placeholder)
        
        if response_text:
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })
            
            st.success("✅ Response complete!")
            
            # Auto-play TTS if enabled - using Web Speech API
            if st.session_state.tts_enabled:
                st.info("🔊 Playing audio...")
                js_code = speak_response(response_text)
                if js_code:
                    st.markdown(js_code, unsafe_allow_html=True)
        else:
            if st.session_state.api_error_count > 2:
                st.warning("💡 Multiple errors detected. Please refresh and try again.")
            else:
                st.info("Feel free to try asking again!")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    st.session_state.tts_enabled = st.toggle(
        "🔊 Enable Text-to-Speech",
        value=st.session_state.tts_enabled,
        help="Convert AI responses to audio"
    )
    
    st.markdown("---")
    st.markdown("### 📚 About")
    st.write("Robin's Business Analytics portfolio with **21 real projects** across 10+ industries.")
    
    st.markdown("### 📊 Project Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Excel", "6")
        st.metric("Power BI", "5")
    with col2:
        st.metric("SQL", "6")
        st.metric("Python", "4")
    
    st.markdown("### 🎖️ Key Achievements")
    st.success("✅ 92% Forecasting")
    st.success("✅ 60% VIP Revenue")
    st.success("✅ 28% Risk ID")
    st.success("✅ 10-15% Default Reduction")
    
    st.markdown("### 🔗 Links")
    st.markdown("[🐙 GitHub](https://github.com/Robi8995)")
    st.markdown("[💼 LinkedIn](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)")
    
    st.markdown("### 💡 Sample Questions")
    if st.button("📌 Show Examples"):
        with st.expander("Questions"):
            for q in SAMPLE_QUESTIONS[:5]:
                st.write(f"• {q}")
    
    if st.button("🔄 Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.caption("Built with ❤️ by Robin | Powered by Groq ⚡")
