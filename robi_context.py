# ===========================
# 🤖 ROBI CONTEXT FILE
# Version: Final (v3.0 – Auto Response Fix)
# Author: Robin Jimmichan Pooppally
# Purpose: Central knowledge base for the Portfoli-AI chatbot
# ===========================

context = {
    "assistant_name": "Portfoli-AI",
    "owner_name": "Robin Jimmichan Pooppally",
    "owner_role": "Business Analyst | Data Analyst",
    "persona": (
        "You are Portfoli-AI — Robin Jimmichan Pooppally's intelligent portfolio assistant. "
        "Your purpose is to help visitors explore Robin's verified Business Analytics projects across Excel, Power BI, SQL, and Python. "
        "You must respond factually using only data contained in this file. "
        "Never invent results, datasets, or formulas. "
        "If information is missing, politely say 'That specific detail isn't available right now in Robin's repository.' "
        "If a user asks about total or number of projects, always say: "
        "'Robin Jimmichan Pooppally has completed a total of 21 verified Business Analytics projects — "
        "6 in Excel, 5 in Power BI, 4 in Python, and 6 in SQL.' "
        "If the user asks for a list of projects, list them exactly from the 'projects' section below."
        "Keep replies professional, warm, and insight-driven."
    ),

    # --------------------------
    # 🟢 GREETING MESSAGE
    # --------------------------
    "greeting_message": (
        "👋 Hi there! I'm **Portfoli-AI**, Robin Jimmichan's portfolio assistant.\n\n"
        "You can ask me about any of Robin's **Business Analytics projects** — whether Excel, Power BI, SQL, or Python.\n\n"
        "I can help you explore:\n"
        "• 📊 Exact DAX formulas, SQL queries, and Python scripts\n"
        "• 📈 Dashboards, KPIs, and visualization methods\n"
        "• 🧮 Excel pivot logic and calculation workflows\n"
        "• 💡 Business insights behind each project\n\n"
        "Just type something like:\n"
        "👉 *'Show me the DAX measures from the E-commerce Funnel Power BI project'* \n"
        "👉 *'Explain how customer churn rate was calculated in the Excel project.'*\n\n"
        "Let's begin exploring Robin's analytics portfolio!"
    ),

    # --------------------------
    # 🧩 PROJECT DIRECTORY
    # --------------------------
    "projects": {
        "Excel": {
            "Telco Customer Churn Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Analysis-Excel-Project",
            "Sales Performance Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Performance-Analysis-Excel-Project",
            "Marketing Campaign Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Marketing-Campaign-Analysis-Excel-Project",
            "HR Analytics Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/HR-Analytics-Excel-Project",
            "E-commerce Sales Analysis": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Sales-Analysis-Excel-Project",
            "Bank Customer Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Analysis-Excel-Project"
        },
        "Power BI": {
            "E-commerce Funnel Analysis": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Funnel-Analysis-PowerBI-Project",
            "Customer 360 Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Customer-360-Dashboard-PowerBI-Project",
            "Retail Sales Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Sales-Dashboard-PowerBI-Project",
            "Telco Customer Churn Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Dashboard-PowerBI-Project",
            "Financial Performance Dashboard": "https://github.com/Robin-Jimmichan-Pooppally/Financial-Performance-Dashboard-PowerBI-Project"
        },
        "Python": {
            "Retail Customer Segmentation": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Customer-Segmentation-Python-Project",
            "Healthcare Patient Analytics": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Patient-Analytics-Python-Project",
            "Airbnb NYC Price Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Airbnb-NYC-Price-Analysis-Python-Project",
            "Sales Forecasting Time Series": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Forecasting-Time-Series-Python-Project"
        },
        "SQL": {
            "Healthcare Claims Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Claims-Analysis-SQL-Project",
            "Bank Customer Segmentation": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Segmentation-SQL-Project",
            "Telco Churn Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Churn-Analysis-SQL-Project",
            "Inventory Supplier Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Inventory-Supplier-Analysis-SQL-Project",
            "Hospital Patient Analysis": "https://github.com/Robin-Jimmichan-Pooppally/Hospital-Patient-Analysis-SQL-Project",
            "Loan Default Prediction": "https://github.com/Robin-Jimmichan-Pooppally/Loan-Default-Prediction-SQL-Project"
        }
    },

    # --------------------------
    # 📚 PROJECT SUMMARY TABLE
    # --------------------------
    "summary": {
        "Excel Projects": 6,
        "Power BI Projects": 5,
        "Python Projects": 4,
        "SQL Projects": 6,
        "Total Projects": 21
    },

    # --------------------------
    # 💬 SAMPLE QUESTIONS
    # --------------------------
    "sample_queries": [
        "How many projects has Robin completed?",
        "List all projects by Robin.",
        "What KPIs were used in the Telco Customer Churn Dashboard?",
        "Show the Power BI DAX formulas for the E-commerce Funnel project.",
        "Explain the SQL logic behind the Loan Default Prediction project.",
        "What insights were drawn from the HR Analytics Excel project?",
        "How was customer segmentation performed in the Retail Python project?"
    ]
}
