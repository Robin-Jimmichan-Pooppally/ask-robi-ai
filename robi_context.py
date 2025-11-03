# robi_context.py
"""
Expanded ROBIN_CONTEXT and PROJECTS_INDEX
Contains:
- ROBIN_CONTEXT: system message with detailed project summaries and key code snippets
- PROJECTS_INDEX: list of all 21 projects with repo links and short summaries (used by the UI)
"""

ROBIN_CONTEXT = r"""
You are Robin Jimmichan P, an aspiring Business Analyst with expertise in SQL, Excel, Power BI, and Python.

Contact:
- Email: rjimmichan@gmail.com
- LinkedIn: https://www.linkedin.com/in/robin-jimmichan-pooppally-676061291
- GitHub: https://github.com/Robin-Jimmichan-Pooppally

Professional focus:
- End-to-end analytics projects across Excel (6), Power BI (5), SQL (6), Python (4)
- Emphasis on business impact, reproducible code, and production-ready dashboards

GUIDELINES:
- When answering, be enthusiastic & confident.
- Provide business-focused explanations and exact code snippets when the user asks.
- Use the project-specific code and measures included below where relevant.
- NEVER hallucinate repository contents — rely on provided READMEs / code snippets.

--- KEY ACHIEVEMENTS (short) ---
- 92% forecasting accuracy (ARIMA MAPE 7.8%)
- 17% excess stock reduction (inventory optimization)
- VIP segment = 15% customers generating 60% revenue (RFM/KMeans)
- 10-15% default reduction from loan-risk segmentation
- 28% high-risk patient identification in healthcare analytics
"""

# -------------------------
# PROJECTS_INDEX for UI
# -------------------------
PROJECTS_INDEX = [
    # Excel (6)
    {"id":"excel_1","name":"Telco Customer Churn Analysis (Excel)","category":"Excel",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Analysis-Excel-Project",
     "short":"Pivot-based churn analysis, correlation and tenure-based insights."},
    {"id":"excel_2","name":"Sales Performance Analysis (Excel)","category":"Excel",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Sales-Performance-Analysis-Excel-Project",
     "short":"Sales vs. Target dashboards, regional analysis and KPI tracking."},
    {"id":"excel_3","name":"Marketing Campaign Analysis (Excel)","category":"Excel",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Marketing-Campaign-Analysis-Excel-Project",
     "short":"Campaign-level ROI, channel CPL optimization and budget allocation."},
    {"id":"excel_4","name":"HR Analytics (Excel)","category":"Excel",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/HR-Analytics-Excel-Project",
     "short":"Attrition analysis, department insights and workforce KPIs."},
    {"id":"excel_5","name":"E-commerce Sales Analysis (Excel)","category":"Excel",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Sales-Analysis-Excel-Project",
     "short":"Transaction consolidation, revenue pivot dashboards."},
    {"id":"excel_6","name":"Bank Customer Analysis (Excel)","category":"Excel",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Analysis-Excel-Project",
     "short":"Banking customer segmentation & balance analysis."},

    # Power BI (5)
    {"id":"pbi_1","name":"E-commerce Funnel Analysis (Power BI)","category":"Power BI",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Funnel-Analysis-PowerBI-Project",
     "short":"Visit -> Cart -> Purchase funnel, conversion metrics and cohort insights."},
    {"id":"pbi_2","name":"Customer 360 Dashboard (Power BI)","category":"Power BI",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Customer-360-Dashboard-PowerBI-Project",
     "short":"Unified view of customers with tickets and purchases for retention analysis."},
    {"id":"pbi_3","name":"Retail Sales Dashboard (Power BI)","category":"Power BI",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Retail-Sales-Dashboard-PowerBI-Project",
     "short":"Star schema model with regional maps, KPIs and time intelligence."},
    {"id":"pbi_4","name":"Telco Customer Churn Dashboard (Power BI)","category":"Power BI",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Dashboard-PowerBI-Project",
     "short":"Churn by contract & payment method, DAX measures for retention."},
    {"id":"pbi_5","name":"Financial Performance Dashboard (Power BI)","category":"Power BI",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Financial-Performance-Dashboard-PowerBI-Project",
     "short":"P&L tracking, YoY growth, investments and profit margin DAX measures."},

    # Python (4)
    {"id":"py_1","name":"Retail Customer Segmentation (Python)","category":"Python",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Retail-Customer-Segmentation-Python-Project",
     "short":"RFM + KMeans clustering with Apriori cross-sell analysis."},
    {"id":"py_2","name":"Healthcare Patient Analytics (Python)","category":"Python",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Patient-Analytics-Python-Project",
     "short":"Comorbidity analysis & LOS insights with feature engineering."},
    {"id":"py_3","name":"Airbnb NYC Price Analysis (Python)","category":"Python",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Airbnb-NYC-Price-Analysis-Python-Project",
     "short":"Price EDA and prediction model for NYC listings."},
    {"id":"py_4","name":"Sales Forecasting - Time Series (Python)","category":"Python",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Sales-Forecasting-Time-Series-Python-Project",
     "short":"ARIMA forecasting with MAPE 7.8% and seasonality insights."},

    # SQL (6)
    {"id":"sql_1","name":"Healthcare Claims Analysis (SQL)","category":"SQL",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Claims-Analysis-SQL-Project",
     "short":"Fraud detection, provider performance and high-cost patient analysis."},
    {"id":"sql_2","name":"Bank Customer Segmentation (SQL)","category":"SQL",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Segmentation-SQL-Project",
     "short":"RFM & segment analysis with CASE and percentile-based grouping."},
    {"id":"sql_3","name":"Telco Churn Analysis (SQL)","category":"SQL",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Telco-Churn-Analysis-SQL-Project",
     "short":"Churn segmentation queries, tenure windows, payment method analysis."},
    {"id":"sql_4","name":"Inventory & Supplier Analysis (SQL)","category":"SQL",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Inventory-Supplier-Analysis-SQL-Project",
     "short":"Turnover ratios, reorder alerts and supplier concentration metrics."},
    {"id":"sql_5","name":"Hospital Patient Analysis (SQL)","category":"SQL",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Hospital-Patient-Analysis-SQL-Project",
     "short":"Admissions, LOS, outcomes and physician performance queries."},
    {"id":"sql_6","name":"Loan Default Prediction (SQL)","category":"SQL",
     "repo":"https://github.com/Robin-Jimmichan-Pooppally/Loan-Default-Prediction-SQL-Project",
     "short":"Risk segmentation, high-risk borrower flagging and portfolio analysis."},
]

# -------------------------
# Key code snippets and measures (pulled from your provided READMEs / earlier conversation)
# -------------------------

# --- Financial Performance (Power BI) example DAX measures ---
FINANCIAL_DAX = r"""
-- Total Revenue
Total Revenue = 
CALCULATE(
    SUM('Financial_Performance_Synthetic'[Amount]), 
    'Financial_Performance_Synthetic'[Category] = "Revenue"
)

-- Total Expenses
Total Expenses = 
CALCULATE(
    SUM('Financial_Performance_Synthetic'[Amount]), 
    'Financial_Performance_Synthetic'[Category] = "Expense"
)

-- Total Investments
Total Investments = 
CALCULATE(
    SUM('Financial_Performance_Synthetic'[Amount]), 
    'Financial_Performance_Synthetic'[Category] = "Investment"
)

-- Net Profit
Net Profit = [Total Revenue] + [Total Expenses]

-- YoY Revenue Growth %
YoY Revenue Growth % = 
VAR CurrentYearRevenue = 
    CALCULATE(
        [Total Revenue], 
        'Financial_Performance_Synthetic'[Year] = YEAR(TODAY())
    )
VAR PreviousYearRevenue = 
    CALCULATE(
        [Total Revenue], 
        'Financial_Performance_Synthetic'[Year] = YEAR(TODAY()) - 1
    )
RETURN 
    DIVIDE(
        CurrentYearRevenue - PreviousYearRevenue, 
        PreviousYearRevenue, 
        0
    ) * 100
"""

# --- Telco Churn (SQL) core queries (from your provided SQL snippets) ---
TELCO_SQL_SNIPPETS = r"""
-- Overall Churn Distribution
SELECT Churn, COUNT(*) AS count 
FROM telco_churn 
GROUP BY Churn;

-- Churn by Contract Type
SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_percent
FROM telco_churn
GROUP BY Contract
ORDER BY churn_rate_percent DESC;

-- High-Risk Customers (credit < 600 OR poor repayment example from Loan project)
SELECT loan_id, borrower_name, credit_score, repayment_history, loan_amount
FROM loans
WHERE credit_score < 600 OR repayment_history = 'Poor'
ORDER BY credit_score ASC;
"""

# --- ARIMA forecasting summary (Python approach) ---
ARIMA_NOTES = r"""
# Key ARIMA steps used in Sales Forecasting project:
1. Merge monthly CSVs into single DataFrame.
2. Convert 'Order Date' to datetime; aggregate sales by month.
3. Test stationarity using augmented Dicky-Fuller (ADF).
4. Use differencing (d=1) to achieve stationarity for ARIMA(1,1,1).
5. Fit ARIMA and evaluate MAPE, RMSE, MAE.
6. Forecast and plot with 95% confidence intervals.

# Example ARIMA code snippet (statsmodels)
from statsmodels.tsa.arima.model import ARIMA
arima_model = ARIMA(train_series, order=(1,1,1))
arima_fit = arima_model.fit()
forecast = arima_fit.forecast(steps=12)
"""

# --- RFM & KMeans (Python) outline (Retail Segmentation) ---
RFM_KMEANS = r"""
# Steps:
1. Compute snapshot_date = last_txn_date + 1 day
2. Compute per customer: Recency (days), Frequency (count), Monetary (sum)
3. StandardScaler -> KMeans (k=4) (use elbow method)
4. Map clusters to business labels: VIP / Medium / Recent / Churned
"""

# Aggregate context object (string) used as system message
ROB_CONTEXT_FULL = ROBIN_CONTEXT + "\n\n" + "KEY_SNIPPETS:\n" + FINANCIAL_DAX + "\n" + TELCO_SQL_SNIPPETS + "\n" + ARIMA_NOTES + "\n" + RFM_KMEANS

# Make available for import
ROBIN_CONTEXT = ROB_CONTEXT_FULL

# End of robi_context.py
