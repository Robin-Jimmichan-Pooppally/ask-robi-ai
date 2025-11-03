# ============================================================
# Robin's Portfoli-AI — Legendary Context File
# robi_context.py
# ============================================================
# This file defines:
# 1️⃣ ROBIN_GREETING  – shown on startup
# 2️⃣ ROBIN_CONTEXT   – system persona for the AI assistant
# 3️⃣ PROJECTS        – index of all real portfolio projects
# 4️⃣ PROJECT_SUMMARY – optional quick summary table
# ============================================================

# ---------------- 1️⃣ Greeting Message ----------------
ROBIN_GREETING = """
🧠 **Welcome to Portfoli-AI — Robin’s Intelligent Portfolio Assistant 🚀**

I can walk you through **Robin Jimmichan P’s 21 real Business Analytics projects**  
across **Excel, SQL, Power BI, and Python.**

Ask me things like:
- “Show the SQL used in the *Telco Customer Churn Analysis* project.”  
- “What DAX measures are used in the *Retail Sales Dashboard*?”  
- “Explain the steps in the *Sales Forecasting Time Series* project.”  

You can browse projects below or ask directly —  
I’ll show dataset details, key steps, formulas, and business insights.

🔗 **GitHub:** [Robin-Jimmichan-Pooppally](https://github.com/Robin-Jimmichan-Pooppally)  
💼 **LinkedIn:** [Profile](https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291)  
📧 **Email:** rjimmichan@gmail.com
"""

# ---------------- 2️⃣ System Persona ----------------
ROBIN_CONTEXT = """
You are **Portfoli-AI**, an intelligent portfolio assistant created by **Robin Jimmichan P**.

Your purpose:
- Help visitors explore Robin’s verified data-analytics projects.
- Answer questions **only** using data and content from these projects.
- Show accurate SQL queries, Python logic, DAX measures, Excel formulas, and business insights.
- Never fabricate or hallucinate details.

Tone:
Professional, helpful, concise, and portfolio-focused.
Always speak as “Robin’s portfolio assistant,” not as Robin himself.
"""

# ---------------- 3️⃣ Project Index ----------------
PROJECTS = [

# ===== Excel Projects (6) =====
{
    "id": "excel1",
    "name": "Telco Customer Churn Analysis (Excel)",
    "category": "Excel",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Analysis-Excel-Project",
    "short": "Analyzed telecom churn trends with Excel dashboards, retention KPIs, and customer segmentation.",
},
{
    "id": "excel2",
    "name": "Sales Performance Analysis (Excel)",
    "category": "Excel",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Performance-Analysis-Excel-Project",
    "short": "Tracked regional and product-wise sales performance using pivot tables and KPI dashboards.",
},
{
    "id": "excel3",
    "name": "Marketing Campaign Analysis (Excel)",
    "category": "Excel",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Marketing-Campaign-Analysis-Excel-Project",
    "short": "Evaluated marketing campaign effectiveness and ROI using Excel trend analysis and segmentation.",
},
{
    "id": "excel4",
    "name": "HR Analytics Dashboard (Excel)",
    "category": "Excel",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/HR-Analytics-Excel-Project",
    "short": "Built an HR dashboard analyzing attrition, employee performance, and demographics.",
},
{
    "id": "excel5",
    "name": "E-commerce Sales Analysis (Excel)",
    "category": "Excel",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Sales-Analysis-Excel-Project",
    "short": "Performed E-commerce order and revenue analysis with Excel dashboards.",
},
{
    "id": "excel6",
    "name": "Bank Customer Analysis (Excel)",
    "category": "Excel",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Analysis-Excel-Project",
    "short": "Analyzed customer demographics and churn trends for a retail bank using Excel tools.",
},

# ===== Power BI Projects (5) =====
{
    "id": "pbi1",
    "name": "E-commerce Funnel Analysis (Power BI)",
    "category": "Power BI",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Funnel-Analysis-PowerBI-Project",
    "short": "Visualized funnel drop-offs and conversion metrics using advanced DAX and Power BI visuals.",
},
{
    "id": "pbi2",
    "name": "Customer 360 Dashboard (Power BI)",
    "category": "Power BI",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Customer-360-Dashboard-PowerBI-Project",
    "short": "Unified customer view dashboard tracking engagement, satisfaction, and churn risk.",
},
{
    "id": "pbi3",
    "name": "Retail Sales Dashboard (Power BI)",
    "category": "Power BI",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Sales-Dashboard-PowerBI-Project",
    "short": "Retail performance dashboard with DAX measures for revenue, margin, and YoY growth.",
},
{
    "id": "pbi4",
    "name": "Telco Customer Churn Dashboard (Power BI)",
    "category": "Power BI",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Dashboard-PowerBI-Project",
    "short": "Analyzed telecom churn with Power BI visuals and predictive KPIs via DAX.",
},
{
    "id": "pbi5",
    "name": "Financial Performance Dashboard (Power BI)",
    "category": "Power BI",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Financial-Performance-Dashboard-PowerBI-Project",
    "short": "Monitored company-wide P&L, cashflow, and key ratios through DAX-powered KPIs.",
},

# ===== Python Projects (4) =====
{
    "id": "py1",
    "name": "Retail Customer Segmentation (Python)",
    "category": "Python",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Customer-Segmentation-Python-Project",
    "short": "Performed RFM and clustering-based segmentation using Python (pandas, scikit-learn).",
},
{
    "id": "py2",
    "name": "Healthcare Patient Analytics (Python)",
    "category": "Python",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Patient-Analytics-Python-Project",
    "short": "Analyzed patient data and healthcare KPIs using pandas, seaborn, and regression models.",
},
{
    "id": "py3",
    "name": "Airbnb NYC Price Analysis (Python)",
    "category": "Python",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Airbnb-NYC-Price-Analysis-Python-Project",
    "short": "Explored Airbnb NYC dataset, performing price trend and neighborhood-based insights.",
},
{
    "id": "py4",
    "name": "Sales Forecasting Time Series (Python)",
    "category": "Python",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Forecasting-Time-Series-Python-Project",
    "short": "Developed ARIMA time-series model to forecast monthly sales performance.",
},

# ===== SQL Projects (6) =====
{
    "id": "sql1",
    "name": "Healthcare Claims Analysis (SQL)",
    "category": "SQL",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Claims-Analysis-SQL-Project",
    "short": "Queried healthcare claims to identify cost trends, provider efficiency, and anomalies.",
},
{
    "id": "sql2",
    "name": "Bank Customer Segmentation (SQL)",
    "category": "SQL",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Segmentation-SQL-Project",
    "short": "Used SQL to segment customers by demographics and product holdings for targeted campaigns.",
},
{
    "id": "sql3",
    "name": "Telco Churn Analysis (SQL)",
    "category": "SQL",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Churn-Analysis-SQL-Project",
    "short": "Analyzed telecom churn causes using joins, aggregations, and retention KPIs in SQL.",
},
{
    "id": "sql4",
    "name": "Inventory Supplier Analysis (SQL)",
    "category": "SQL",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Inventory-Supplier-Analysis-SQL-Project",
    "short": "Evaluated supplier performance, inventory efficiency, and fulfillment metrics.",
},
{
    "id": "sql5",
    "name": "Hospital Patient Analysis (SQL)",
    "category": "SQL",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Hospital-Patient-Analysis-SQL-Project",
    "short": "Analyzed hospital admissions, treatment outcomes, and doctor performance via SQL.",
},
{
    "id": "sql6",
    "name": "Loan Default Prediction (SQL)",
    "category": "SQL",
    "repo": "https://github.com/Robin-Jimmichan-Pooppally/Loan-Default-Prediction-SQL-Project",
    "short": "Investigated borrower default trends using SQL aggregations and risk segmentation.",
},
]

# ---------------- 4️⃣ Summary Table ----------------
PROJECT_SUMMARY = """
| Category | Project Count | Example Project |
|-----------|----------------|----------------|
| Excel     | 6 | Telco Customer Churn Analysis |
| Power BI  | 5 | Retail Sales Dashboard |
| Python    | 4 | Sales Forecasting Time Series |
| SQL       | 6 | Loan Default Prediction |
"""
