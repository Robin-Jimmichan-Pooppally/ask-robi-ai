import streamlit as st
import requests
import json

# -----------------------
# Page Config
# -----------------------
st.set_page_config(page_title="Portfoli-AI", page_icon="🤖", layout="wide")

# --- Header ---
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown("<h2 style='text-align: center; color:#00FFFF; text-shadow: 0 0 15px #00FFFF;'>🤖 Portfoli-AI — Robin Jimmichan’s Portfolio Assistant</h2>", unsafe_allow_html=True)
with col2:
    if st.button("🧹 Clear Chat"):
        st.session_state["chat_history"] = []
        st.session_state["history"] = []
        st.session_state["greeted"] = False
        st.rerun()

# -----------------------
# Chat history initialization + Greeting
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
if "greeted" not in st.session_state:
    st.session_state.greeted = False

# ✅ Greeting message (only once, glowing)
if not st.session_state.greeted:
    greeting_html = """
    <div style='
        border-radius: 15px;
        padding: 18px;
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid rgba(0,255,255,0.3);
        box-shadow: 0 0 15px rgba(0,255,255,0.4);
        font-family: "Inter", sans-serif;
    '>
        <h4 style='color:#00FFFF;'>👋 Hey Robin!</h4>
        <p style='color:white;'>
        I'm <b style='color:#00FFFF;'>Portfoli-AI 🤖</b>, your glowing digital portfolio assistant.<br><br>
        You can ask me anything about your <b>projects</b>, <b>skills</b>, or <b>business analytics insights</b>.<br>
        Start by selecting a project from the sidebar or simply say: <i>"Explain my churn analysis project."</i>
        </p>
    </div>
    """
    st.markdown(greeting_html, unsafe_allow_html=True)
    st.session_state.history.append({
        "role": "assistant",
        "content": "👋 Hey Robin! I'm Portfoli-AI 🤖, your glowing portfolio assistant."
    })
    st.session_state.greeted = True

# -----------------------
# Project Dictionary
# -----------------------
projects = {
    "Excel": {
        "Telco Customer Churn Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Analysis-Excel-Project",
        "Sales Performance Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Performance-Analysis-Excel-Project",
        "Marketing Campaign Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Marketing-Campaign-Analysis-Excel-Project",
        "HR Analytics Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/HR-Analytics-Excel-Project",
        "E-commerce Sales Analysis": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Sales-Analysis-Excel-Project",
        "Bank Customer Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Analysis-Excel-Project",
    },
    "Power BI": {
        "E-commerce Funnel Analysis": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Funnel-Analysis-PowerBI-Project",
        "Customer 360 Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Customer-360-Dashboard-PowerBI-Project",
        "Retail Sales Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Sales-Dashboard-PowerBI-Project",
        "Telco Customer Churn Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Dashboard-PowerBI-Project",
        "Financial Performance Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Financial-Performance-Dashboard-PowerBI-Project",
    },
    "Python": {
        "Retail Customer Segmentation": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Customer-Segmentation-Python-Project",
        "Healthcare Patient Analytics": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Patient-Analytics-Python-Project",
        "Airbnb NYC Price Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Airbnb-NYC-Price-Analysis-Python-Project",
        "Sales Forecasting Time Series": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Forecasting-Time-Series-Python-Project",
    },
    "SQL": {
        "Healthcare Claims Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Claims-Analysis-SQL-Project",
        "Bank Customer Segmentation": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Segmentation-SQL-Project",
        "Telco Churn Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Churn-Analysis-SQL-Project",
        "Inventory Supplier Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Inventory-Supplier-Analysis-SQL-Project",
        "Hospital Patient Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Hospital-Patient-Analysis-SQL-Project",
        "Loan Default Prediction": "https://github.com/Robin-Jimmichan-Pooppally/Loan-Default-Prediction-SQL-Project",
    }
}

# -----------------------
# Sidebar - Filter & Selection
# -----------------------
selected_category = st.sidebar.radio("📂 Filter by Category", list(projects.keys()))
selected_project = st.sidebar.selectbox("🔍 Choose a Project", list(projects[selected_category].keys()))

if selected_project:
    repo_url = projects[selected_category][selected_project]
    st.markdown(f"### 🔗 [{selected_project}]({repo_url})")

# -----------------------
# Chat Section
# -----------------------
for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    if role == "user":
        st.chat_message("user").markdown(content)
    else:
        st.chat_message("assistant").markdown(content)

if prompt := st.chat_input("Ask about this project or your portfolio..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role": "user", "content": prompt})

    # Placeholder for actual Groq API logic (to be connected later)
    response = f"Here’s some info about **{selected_project}** from the {selected_category} category!"
    st.chat_message("assistant").markdown(response)
    st.session_state.history.append({"role": "assistant", "content": response})
