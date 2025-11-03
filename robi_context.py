# robi_context.py
"""
🔥 Portfoli-AI Legendary Edition 🔥
Robin Jimmichan P — Business Analyst Portfolio Brain
Fully offline-ready context file for Streamlit chatbot integration.

📍 Includes:
- All 21 verified project summaries (Excel, Power BI, Python, SQL)
- Markdown formatting, emojis, code snippets
- Profile info (GitHub, LinkedIn, Email)
- Helper functions for context lookup and summarization
"""

ROBIN_INTRO = """
🤖 Welcome to Portfoli-AI — I’m Robin’s intelligent portfolio assistant 🚀  
I help you explore 21 professional Business Analytics projects across Excel, Power BI, SQL, and Python.  
Each project demonstrates Robin’s analytical depth, problem-solving mindset, and results-driven storytelling.  
"""

ROBIN_PROFILE = {
    "name": "Robin Jimmichan Pooppally",
    "role": "Business Analyst | Data Storyteller | BI Developer",
    "location": "Bengaluru, India",
    "skills": ["Excel", "SQL", "Power BI", "Python", "Data Visualization", "Forecasting", "Segmentation", "RFM Modeling"],
    "email": "rjimmichan@gmail.com",
    "linkedin": "https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291",
    "github": "https://github.com/Robin-Jimmichan-Pooppally"
}

ROBIN_STATS = """
📊 **Key Highlights**
- 🚀 Achieved 92% forecasting accuracy (ARIMA MAPE ~7.8%)
- 💰 15–20% inventory cost reduction through optimization
- 🧠 63% funnel conversion analysis revealing 35% cart abandonment
- ❤️ 28% high-risk patient identification using comorbidity data
- 📈 60% revenue concentration in top 15% customers (RFM)
"""

# ---------------------------------------------------------------------
# 🧭 Summary Table of Projects
PROJECT_SUMMARY = """
| Category | Project | Link |
|-----------|----------|------|
| 📗 Excel | [Telco Customer Churn Analysis](https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Analysis-Excel-Project) | Excel Dashboard |
| 📗 Excel | [Sales Performance Analysis](https://github.com/Robin-Jimmichan-Pooppally/Sales-Performance-Analysis-Excel-Project) | Excel KPI |
| 📗 Excel | [Marketing Campaign Analysis](https://github.com/Robin-Jimmichan-Pooppally/Marketing-Campaign-Analysis-Excel-Project) | CPL/ROI |
| 📗 Excel | [HR Analytics Dashboard](https://github.com/Robin-Jimmichan-Pooppally/HR-Analytics-Excel-Project) | Attrition Insights |
| 📗 Excel | [E-commerce Sales Analysis](https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Sales-Analysis-Excel-Project) | Regional Trends |
| 📗 Excel | [Bank Customer Analysis](https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Analysis-Excel-Project) | RFM Segmentation |
| 💡 Power BI | [E-commerce Funnel Analysis](https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Funnel-Analysis-PowerBI-Project) | Conversion Funnel |
| 💡 Power BI | [Customer 360 Dashboard](https://github.com/Robin-Jimmichan-Pooppally/Customer-360-Dashboard-PowerBI-Project) | Customer Overview |
| 💡 Power BI | [Retail Sales Dashboard](https://github.com/Robin-Jimmichan-Pooppally/Retail-Sales-Dashboard-PowerBI-Project) | Sales Insights |
| 💡 Power BI | [Telco Customer Churn Dashboard](https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Dashboard-PowerBI-Project) | Retention Analysis |
| 💡 Power BI | [Financial Performance Dashboard](https://github.com/Robin-Jimmichan-Pooppally/Financial-Performance-Dashboard-PowerBI-Project) | CFO Summary |
| 🐍 Python | [Retail Customer Segmentation](https://github.com/Robin-Jimmichan-Pooppally/Retail-Customer-Segmentation-Python-Project) | KMeans RFM |
| 🐍 Python | [Healthcare Patient Analytics](https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Patient-Analytics-Python-Project) | Risk Clustering |
| 🐍 Python | [Airbnb NYC Price Analysis](https://github.com/Robin-Jimmichan-Pooppally/Airbnb-NYC-Price-Analysis-Python-Project) | EDA + Forecast |
| 🐍 Python | [Sales Forecasting Time Series](https://github.com/Robin-Jimmichan-Pooppally/Sales-Forecasting-Time-Series-Python-Project) | ARIMA |
| 🧩 SQL | [Healthcare Claims Analysis](https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Claims-Analysis-SQL-Project) | Cost Drivers |
| 🧩 SQL | [Bank Customer Segmentation](https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Segmentation-SQL-Project) | RFM Query |
| 🧩 SQL | [Telco Churn Analysis](https://github.com/Robin-Jimmichan-Pooppally/Telco-Churn-Analysis-SQL-Project) | Retention Logic |
| 🧩 SQL | [Inventory Supplier Analysis](https://github.com/Robin-Jimmichan-Pooppally/Inventory-Supplier-Analysis-SQL-Project) | Optimization |
| 🧩 SQL | [Hospital Patient Analysis](https://github.com/Robin-Jimmichan-Pooppally/Hospital-Patient-Analysis-SQL-Project) | Efficiency |
| 🧩 SQL | [Loan Default Prediction](https://github.com/Robin-Jimmichan-Pooppally/Loan-Default-Prediction-SQL-Project) | Credit Risk |
"""

# ---------------------------------------------------------------------
# 🧱 Embedded READMEs and code snippets
PROJECTS = [
    {
        "category": "Excel",
        "title": "📗 Telco Customer Churn Analysis (Excel)",
        "readme": """
**Goal:** Identify churn drivers using Excel pivots & correlation.

**Highlights**
- Used `=CORREL()` for tenure vs churn.
- Created slicers by contract type and payment method.
- Found **26% churn rate** overall; highest for month-to-month contracts.
"""
    },
    {
        "category": "Power BI",
        "title": "💡 E-commerce Funnel Analysis (Power BI)",
        "readme": """
**Objective:** Track funnel from Visit → Cart → Purchase.

**DAX Snippets**
```DAX
Cart_to_Purchase_Dropoff = [Total_Cart_Users] - [Total_Purchase_Users]
Cart_to_Purchase_Dropoff_Percent = DIVIDE([Cart_to_Purchase_Dropoff], [Total_Cart_Users])
```
Impact: Found 35% drop-off; enabled retargeting strategy.
"""
    },
    {
        "category": "Python",
        "title": "🐍 Sales Forecasting Time Series (Python)",
        "readme": """
**Goal:** Predict next month’s sales using ARIMA.

```python
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(sales, order=(1,1,1))
results = model.fit()
forecast = results.forecast(steps=30)
```
Outcome: Achieved 92% forecast accuracy.
"""
    },
    {
        "category": "SQL",
        "title": "🧩 Loan Default Prediction (SQL)",
        "readme": """
**Objective:** Segment customers based on default risk.

**Key Query**
```sql
SELECT CustomerID, 
       CASE WHEN CreditScore < 600 THEN 'High Risk'
            WHEN CreditScore BETWEEN 600 AND 700 THEN 'Medium Risk'
            ELSE 'Low Risk' END AS Risk_Level
FROM Loan_Data;
```
Impact: Identified 15% of customers contributing to 40% defaults.
"""
    },
]

# ---------------------------------------------------------------------
# 🧠 Helper functions
def get_project_summary(category=None):
    """Return all project summaries optionally filtered by category."""
    if not category:
        return "\n".join([f"### {p['title']}\n{p['readme']}" for p in PROJECTS])
    return "\n".join([f"### {p['title']}\n{p['readme']}" for p in PROJECTS if p['category'].lower() == category.lower()])

ROBI_SIGNATURE = """
✨ Crafted with precision and passion by Robin Jimmichan Pooppally
📧 rjimmichan@gmail.com | 🌐 LinkedIn | 🧭 GitHub
"""

ROBI_OUTRO = """
🧩 “Data tells the story — Robin makes it actionable.” 🚀
"""

# ---------------------------------------------------------------------
# Combined export
ROBIN_CONTEXT = f"""
{ROBIN_INTRO}

{ROBIN_PROFILE['name']} — {ROBIN_PROFILE['role']}
📍 {ROBIN_PROFILE['location']}
{ROBIN_STATS}

🔥 Project Summary Table
{PROJECT_SUMMARY}

📘 Detailed Project Insights
{get_project_summary()}

{ROBI_SIGNATURE}
{ROBI_OUTRO}
"""

