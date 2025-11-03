# robi_context.py
"""
ROBI.AI Context and Project Index
Contains:
- ROBIN_CONTEXT: system prompt with Robin's skills, achievements, and guidance
- PROJECTS_INDEX: list of project dicts (id, name, repo, category, short, readme_url)
"""

# System context for the LLM (business-friendly, metrics-first)
ROBIN_CONTEXT = '''
You are Robin Jimmichan P, an experienced Business Analyst focused on SQL, Excel, Power BI, and Python.
Location: Bengaluru, India (Originally from Kerala)
Core skills: SQL, Excel, Power BI, Python, Data Visualization, BI, Time-series forecasting, RFM segmentation, Data modeling.

KEY ACHIEVEMENTS:
- 92% forecasting accuracy (ARIMA MAPE ~7.8%)
- 15-20% cost reduction via inventory optimization
- 60% revenue concentration in VIP segment via RFM (15% customers = 60% revenue)
- 28% high-risk patient identification using comorbidity analysis
- 8-12% hospital stay reduction identified via operational analytics
- 63% e-commerce funnel conversion; 35% cart abandonment opportunity identified
- 10-15% loan default reduction from risk segmentation

How to respond:
- Be enthusiastic and business-focused.
- Always reference measurable outcomes (use numbers above).
- When asked for exact code or README, fetch from the repository link provided in PROJECTS_INDEX.
- If exact code is not available locally, explain you will fetch from GitHub raw URL and display exact content.
- For SQL/DAX/Excel formulas: if exact snippet exists in repo README or files, display it verbatim; otherwise provide a clearly labeled template/example and instruct where to place it.
'''

# PROJECTS_INDEX: 21 projects with links and raw README URLs
# Raw README URL format assumes 'main' branch. Change branch if needed.
OWNER = "Robin-Jimmichan-Pooppally"

PROJECTS_INDEX = [
    # Excel (6)
    {
        "id": "excel_1",
        "name": "Telco Customer Churn Analysis (Excel)",
        "repo": f"https://github.com/{OWNER}/Telco-Customer-Churn-Analysis-Excel-Project",
        "category": "Excel",
        "short": "Telco churn analysis using Excel pivot tables, correlations, and visual dashboards.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Telco-Customer-Churn-Analysis-Excel-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "excel_2",
        "name": "Sales Performance Analysis (Excel)",
        "repo": f"https://github.com/{OWNER}/Sales-Performance-Analysis-Excel-Project",
        "category": "Excel",
        "short": "Sales performance dashboards, target vs actual, KPI tracking.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Sales-Performance-Analysis-Excel-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "excel_3",
        "name": "Marketing Campaign Analysis (Excel)",
        "repo": f"https://github.com/{OWNER}/Marketing-Campaign-Analysis-Excel-Project",
        "category": "Excel",
        "short": "Campaign ROI, cost-per-lead analysis, channel optimization.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Marketing-Campaign-Analysis-Excel-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "excel_4",
        "name": "HR Analytics Dashboard (Excel)",
        "repo": f"https://github.com/{OWNER}/HR-Analytics-Excel-Project",
        "category": "Excel",
        "short": "Attrition analysis and employee metrics using Excel.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/HR-Analytics-Excel-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "excel_5",
        "name": "E-commerce Sales Analysis (Excel)",
        "repo": f"https://github.com/{OWNER}/E-commerce-Sales-Analysis-Excel-Project",
        "category": "Excel",
        "short": "Multi-CSV consolidation and revenue dashboards via Power Query.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/E-commerce-Sales-Analysis-Excel-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "excel_6",
        "name": "Bank Customer Analysis (Excel)",
        "repo": f"https://github.com/{OWNER}/Bank-Customer-Analysis-Excel-Project",
        "category": "Excel",
        "short": "RFM segmentation and high-value customer identification in Excel.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Bank-Customer-Analysis-Excel-Project/main/README.md",
        "updated": "2025"
    },

    # Power BI (5)
    {
        "id": "pbi_1",
        "name": "E-commerce Funnel Analysis (Power BI)",
        "repo": f"https://github.com/{OWNER}/E-commerce-Funnel-Analysis-PowerBI-Project",
        "category": "Power BI",
        "short": "Visit → Cart → Purchase funnel analysis with DAX measures and cohorts.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/E-commerce-Funnel-Analysis-PowerBI-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "pbi_2",
        "name": "Customer 360 Dashboard (Power BI)",
        "repo": f"https://github.com/{OWNER}/Customer-360-Dashboard-PowerBI-Project",
        "category": "Power BI",
        "short": "Unified customer view linking tickets, purchases, and support metrics.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Customer-360-Dashboard-PowerBI-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "pbi_3",
        "name": "Retail Sales Dashboard (Power BI)",
        "repo": f"https://github.com/{OWNER}/Retail-Sales-Dashboard-PowerBI-Project",
        "category": "Power BI",
        "short": "Star schema, KPI cards, time intelligence and regional maps.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Retail-Sales-Dashboard-PowerBI-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "pbi_4",
        "name": "Telco Customer Churn Dashboard (Power BI)",
        "repo": f"https://github.com/{OWNER}/Telco-Customer-Churn-Dashboard-PowerBI-Project",
        "category": "Power BI",
        "short": "Churn by contract type, payment method and tenure with DAX measures.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Telco-Customer-Churn-Dashboard-PowerBI-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "pbi_5",
        "name": "Financial Performance Dashboard (Power BI)",
        "repo": f"https://github.com/{OWNER}/Financial-Performance-Dashboard-PowerBI-Project",
        "category": "Power BI",
        "short": "P&L tracking, YoY, waterfall and time-intelligence measures.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Financial-Performance-Dashboard-PowerBI-Project/main/README.md",
        "updated": "2025"
    },

    # Python (4)
    {
        "id": "py_1",
        "name": "Retail Customer Segmentation (Python)",
        "repo": f"https://github.com/{OWNER}/Retail-Customer-Segmentation-Python-Project",
        "category": "Python",
        "short": "RFM analysis + KMeans clustering to identify VIP segments.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Retail-Customer-Segmentation-Python-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "py_2",
        "name": "Healthcare Patient Analytics (Python)",
        "repo": f"https://github.com/{OWNER}/Healthcare-Patient-Analytics-Python-Project",
        "category": "Python",
        "short": "Comorbidity and LOS analysis, risk stratification and visualization.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Healthcare-Patient-Analytics-Python-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "py_3",
        "name": "Airbnb NYC Price Analysis (Python)",
        "repo": f"https://github.com/{OWNER}/Airbnb-NYC-Price-Analysis-Python-Project",
        "category": "Python",
        "short": "EDA and regression price model across NYC neighborhoods (2019).",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Airbnb-NYC-Price-Analysis-Python-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "py_4",
        "name": "Sales Forecasting - Time Series (Python)",
        "repo": f"https://github.com/{OWNER}/Sales-Forecasting-Time-Series-Python-Project",
        "category": "Python",
        "short": "ARIMA forecasting for monthly retail sales with model diagnostics.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Sales-Forecasting-Time-Series-Python-Project/main/README.md",
        "updated": "2025"
    },

    # SQL (6)
    {
        "id": "sql_1",
        "name": "Healthcare Claims Analysis (SQL)",
        "repo": f"https://github.com/{OWNER}/Healthcare-Claims-Analysis-SQL-Project",
        "category": "SQL",
        "short": "Claims fraud detection, provider analysis, and high-cost patient identification.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Healthcare-Claims-Analysis-SQL-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "sql_2",
        "name": "Bank Customer Segmentation (SQL)",
        "repo": f"https://github.com/{OWNER}/Bank-Customer-Segmentation-SQL-Project",
        "category": "SQL",
        "short": "RFM segmentation in SQL for banking customers and regional insights.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Bank-Customer-Segmentation-SQL-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "sql_3",
        "name": "Telco Churn Analysis (SQL)",
        "repo": f"https://github.com/{OWNER}/Telco-Churn-Analysis-SQL-Project",
        "category": "SQL",
        "short": "7,032 customers churn analysis, tenure and payment method impact.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Telco-Churn-Analysis-SQL-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "sql_4",
        "name": "Inventory & Supplier Analysis (SQL)",
        "repo": f"https://github.com/{OWNER}/Inventory-Supplier-Analysis-SQL-Project",
        "category": "SQL",
        "short": "Inventory turn, reorder priority, and supplier dependency analysis.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Inventory-Supplier-Analysis-SQL-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "sql_5",
        "name": "Hospital Patient Analysis (SQL)",
        "repo": f"https://github.com/{OWNER}/Hospital-Patient-Analysis-SQL-Project",
        "category": "SQL",
        "short": "Patient admissions, length-of-stay, outcomes and physician performance.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Hospital-Patient-Analysis-SQL-Project/main/README.md",
        "updated": "2025"
    },
    {
        "id": "sql_6",
        "name": "Loan Default Prediction (SQL)",
        "repo": f"https://github.com/{OWNER}/Loan-Default-Prediction-SQL-Project",
        "category": "SQL",
        "short": "Loan risk segmentation and portfolio level analysis.",
        "readme_url": f"https://raw.githubusercontent.com/{OWNER}/Loan-Default-Prediction-SQL-Project/main/README.md",
        "updated": "2025"
    },
]

# Optional: helper for external tools (not used directly)
def get_project_by_name(name: str):
    """Return the project dict matching name (case-insensitive) or None."""
    name_lower = name.strip().lower()
    for p in PROJECTS_INDEX:
        if p["name"].strip().lower() == name_lower:
            return p
    return None
