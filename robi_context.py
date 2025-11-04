# ===========================
# 🤖 ENHANCED PORTFOLI-AI CONTEXT FILE
# Version: Final (v4.0 – Complete 21 Project Portfolio)
# Author: Robin Jimmichan Pooppally
# Purpose: Comprehensive knowledge base for the Portfoli-AI chatbot
# ===========================

context = {
    "assistant_name": "Portfoli-AI",
    "owner_name": "Robin Jimmichan Pooppally",
    "owner_role": "Business Analyst | Data Analyst",
    
    "persona": (
        "You are Portfoli-AI — Robin Jimmichan Pooppally's intelligent portfolio assistant. "
        "Your purpose is to help visitors explore Robin's verified Business Analytics projects across Excel, Power BI, SQL, and Python. "
        "You must respond factually using only data contained in this knowledge base. "
        "Never invent results, datasets, or formulas. Always be specific with metrics, code snippets, and technical details. "
        "If information is missing, politely say 'That specific detail isn't available right now in Robin's repository.' "
        "Keep replies professional, warm, and insight-driven. Provide actionable insights about each project."
    ),

    "summary": {
        "Excel Projects": 6,
        "Power BI Projects": 5,
        "Python Projects": 4,
        "SQL Projects": 6,
        "Total Projects": 21,
        "Total Records Analyzed": "185,000+",
        "Total Customers/Patients Analyzed": "7,000+",
        "Datasets Spanning": "2019-2025"
    },

    "projects_detailed": {
        # ==================== EXCEL PROJECTS ====================
        "Excel": {
            "Telco Customer Churn Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Analysis-Excel-Project",
                "dataset_size": "7,043 customer records with 21 attributes",
                "objective": "Analyze customer churn patterns and identify key factors contributing to customer attrition",
                "key_metrics": {
                    "overall_churn_rate": "26.5%",
                    "month_to_month_churn": "40.48%",
                    "two_year_contract_churn": "0.38%",
                    "senior_citizen_churn": "22.41%",
                    "paperless_billing_churn": "24.05%"
                },
                "techniques": ["Pivot Tables", "Pivot Charts", "Slicers", "Conditional Formatting", "Data Validation"],
                "key_findings": [
                    "Contract type is strongest predictor: month-to-month shows 40.48% churn vs 0.38% for 2-year",
                    "Tenure impact: customers <12 months show 23.76% churn vs 14.76% for 49+ months",
                    "Electronic check users: 23.97% churn vs 19.44% for bank transfer (auto-pay)",
                    "High-paying customers (>$70/month) show 21.76% churn indicating pricing sensitivity",
                    "Paperless billing correlates with 24.05% churn vs 16.61% for traditional billing"
                ],
                "visualizations": ["Donut Chart (Overall Churn)", "Column Charts (By Category)", "Bar Charts", "Line Charts"],
                "business_impact": "$2.3M revenue at risk; 1,869 high-risk accounts identified for retention"
            },

            "Sales Performance Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Performance-Analysis-Excel-Project",
                "dataset_size": "800+ sales transaction records from 8 salespersons",
                "objective": "Analyze company-wide sales performance and visualize key metrics across regions and product categories",
                "key_metrics": {
                    "total_sales": "₹2,561,350.31",
                    "north_region_leads": "₹670,334.25",
                    "sports_category_top": "₹583,219.04",
                    "bob_top_performer": "+3.43% variance above target",
                    "august_peak_month": "₹275,699.64"
                },
                "techniques": ["Pivot Tables", "Pivot Charts", "Cell Formulas", "Variance Calculations", "Slicers"],
                "key_findings": [
                    "North Region highest: ₹670K, West Region lowest: ₹576K (balanced 22% spread)",
                    "Sports products dominate: ₹583K (23% of revenue)",
                    "Bob exceeds target by 3.43%; Frank 1.86% below target",
                    "7 of 8 salespersons exceeded targets (company +0.74% overall)",
                    "August peak: ₹275K (73% above March low of ₹159K)"
                ],
                "visualizations": ["Column Charts (Regional)", "Pie Chart (Product Mix)", "Horizontal Bar (Sales)", "Line Chart (Trends)"],
                "business_impact": "Enables performance reviews, compensation planning, and regional resource allocation"
            },

            "Marketing Campaign Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Marketing-Campaign-Analysis-Excel-Project",
                "dataset_size": "Multiple marketing campaigns with budget, revenue, leads, and conversion data",
                "objective": "Calculate ROI for marketing campaigns and optimize budget allocation across channels",
                "key_metrics": {
                    "roi_formula": "(Revenue – Budget) / Budget × 100",
                    "conversion_rate_formula": "Conversions / Leads × 100",
                    "high_roi_channels": "Email, Social Media",
                    "low_roi_observation": "Paid ads show high reach but lower ROI",
                    "budget_optimization_potential": "10-15% ROI improvement through reallocation"
                },
                "techniques": ["Analytical Formulas", "PivotTables", "Conditional Formatting", "Combo Charts", "Slicers"],
                "key_findings": [
                    "ROI formula: (Revenue – Budget) / Budget × 100",
                    "Conversion rate formula: Conversions / Leads × 100",
                    "Certain platforms achieve highest ROI (Email, Social Media)",
                    "Paid ads (Google Ads) show high reach but comparatively lower ROI",
                    "Moderate spending often outperforms high-cost campaigns",
                    "Negative ROI campaigns identified signaling need for creative adjustments",
                    "Budget reallocation potential: 10-15% ROI improvement"
                ],
                "visualizations": ["Bar Charts (ROI by Channel)", "PivotTable", "Column Charts (Conversion)", "Combo Chart"],
                "business_impact": "Data-driven budget optimization reducing waste and maximizing marketing returns"
            },

            "HR Analytics Dashboard": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/HR-Analytics-Excel-Project",
                "dataset_size": "Employee-level data with demographics, satisfaction, and attrition status",
                "objective": "Analyze employee attrition patterns and identify factors influencing retention",
                "key_metrics": {
                    "overall_attrition_rate": "11.05%",
                    "age_21_25_attrition": "12.93%",
                    "it_department_attrition": "13.95%",
                    "talent_acquisition_role_attrition": "20.00%",
                    "satisfaction_1_attrition": "18.41%",
                    "satisfaction_4_5_attrition": "4.62-5.41%"
                },
                "techniques": ["Pivot Tables", "Pivot Charts", "Conditional Formatting", "Slicers", "Data Aggregation"],
                "key_findings": [
                    "Age 21-25: highest attrition 12.93%; 41-55: lowest <9%",
                    "IT department: 13.95% attrition (highest); R&D: 8.02% (lowest)",
                    "Talent Acquisition role: 20% attrition (critical)",
                    "Job satisfaction 1: 18.41% attrition vs satisfaction 4-5: <6%",
                    "Work-life balance: improvements reduce attrition by ~2%",
                    "Senior levels (Level 5): lower attrition at 9.50% vs Level 2 at 12.36%",
                    "Competitive pay supports retention; junior levels need focus"
                ],
                "visualizations": ["Donut Chart (Overall)", "Bar Charts (Demographics)", "Pie Charts", "Conditional Formatted Tables"],
                "business_impact": "Identifies 1,500+ high-risk accounts; satisfaction improvements can reduce turnover 15-25%"
            },

            "E-commerce Sales Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Sales-Analysis-Excel-Project",
                "dataset_size": "1,000 transactional records spanning Sept 2024 - Sept 2025",
                "objective": "Analyze 12-month e-commerce performance across categories, products, and returns",
                "key_metrics": {
                    "total_revenue": "₹1,064,979",
                    "books_leading_category": "₹227,869 (21.4% of revenue)",
                    "books_units_sold": "892 units (highest volume)",
                    "self_help_books_top_product": "230 units",
                    "december_peak_orders": "103 orders (holiday season)",
                    "september_low": "36 orders (off-season)",
                    "total_returns": "Moderate throughout year (6-10/month average)"
                },
                "techniques": ["Pivot Tables", "Pivot Charts", "Slicers", "Data Labels", "Conditional Formatting"],
                "key_findings": [
                    "Books lead revenue (₹227K), balanced across 5 categories (~₹206-227K each)",
                    "Self-Help Books top seller: 230 units; Board Games lowest: 119 units",
                    "December peak: 103 orders; March low: 36 orders (186% variation)",
                    "Oct 2024: 15 returns (highest); Sept 2025: 1 return (quality improvement)",
                    "Stable post-holiday performance (Jan-Aug 2025): 70-90 orders/month",
                    "Balanced portfolio: no category dominates severely"
                ],
                "visualizations": ["Horizontal Bar (Category Revenue)", "Pie Chart (Distribution)", "Line Chart (Trends)", "Column Chart (Returns)"],
                "business_impact": "Identifies seasonal peaks for inventory planning; reveals category performance for strategic focus"
            },

            "Bank Customer Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Analysis-Excel-Project",
                "dataset_size": "Customer demographic and subscription data across regions",
                "objective": "Segment customers by demographics and balance to understand subscription behavior",
                "key_metrics": {
                    "overall_subscription_rate": "23.96%",
                    "26_35_age_group_highest": "25.22%",
                    "36_45_age_group_lowest": "22.20%",
                    "retired_highest_job_subscription": "25.17%",
                    "management_lowest_job_subscription": "21.57%",
                    "medium_balance_customers": "49.30% of portfolio",
                    "single_marital_highest": "24.96%"
                },
                "techniques": ["PivotTables", "PivotCharts", "Calculated Fields", "Conditional Formatting (5-color)", "Slicers"],
                "key_findings": [
                    "Overall subscription: 23.96% (76.04% non-subscribed) - growth opportunity",
                    "Age group variation: 26-35 and 56+ show highest (~25.2-25.6%)",
                    "Job variation: Retired (25.17%) vs Management (21.57%)",
                    "Marital variation: Single (24.96%) vs Divorced (22.77%) - small spread",
                    "Balance distribution: Medium (49.3%), High (25.7%), Low (25.0%)",
                    "Granular analysis: Job-Marital-Age segments with color-coded intensity"
                ],
                "visualizations": ["Donut Chart (Subscription)", "Stacked Bar Charts (Age/Job/Marital)", "Pie Chart (Balance)", "Multilevel Pivot"],
                "business_impact": "Enables targeted subscription campaigns; identifies high-potential segments for upselling"
            }
        },

        # ==================== POWER BI PROJECTS ====================
        "Power BI": {
            "E-commerce Funnel Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/E-commerce-Funnel-Analysis-PowerBI-Project",
                "data_model": "Multi-table relational model (Visits → Carts → Purchases)",
                "objective": "Analyze complete customer conversion funnel and identify drop-off points",
                "dax_measures": {
                    "total_visit_users": "DISTINCTCOUNT(Customer_360_Visits[Customer_ID])",
                    "total_cart_users": "DISTINCTCOUNT(Customer_360_Carts[Customer_ID])",
                    "total_purchase_users": "DISTINCTCOUNT(Customer_360_Purchases[Customer_ID])",
                    "visit_to_cart_conversion": "DIVIDE([Total_Cart_Users], [Total_Visit_Users], 0)",
                    "cart_to_purchase_conversion": "DIVIDE([Total_Purchase_Users], [Total_Cart_Users], 0)",
                    "overall_conversion": "DIVIDE([Total_Purchase_Users], [Total_Visit_Users], 0)",
                    "visit_to_cart_dropoff_percent": "DIVIDE([Total_Visit_Users] - [Total_Cart_Users], [Total_Visit_Users], 0)",
                    "cart_to_purchase_dropoff_percent": "DIVIDE([Total_Cart_Users] - [Total_Purchase_Users], [Total_Cart_Users], 0)"
                },
                "key_insights": [
                    "Tracks visit-to-cart, cart-to-purchase, overall conversion rates",
                    "Measures drop-off at each stage with both count and percentage",
                    "Filters by region, device, traffic source, payment method",
                    "Identifies payment method performance by region"
                ],
                "visualizations": ["KPI Cards", "Funnel Charts", "Column Charts", "Line Charts", "Tables"],
                "business_impact": "Identifies optimization opportunities in conversion funnel; supports cart abandonment recovery"
            },

            "Customer 360 Dashboard": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Customer-360-Dashboard-PowerBI-Project",
                "data_model": "Star Schema (Customers, Orders, Tickets with DateTable)",
                "objective": "Provide 360° unified view of customer behavior, sales, and support",
                "dax_measures": {
                    "total_customers": "DISTINCTCOUNT('Customer_360_Customers'[Customer_ID])",
                    "total_orders": "COUNTROWS(Customer_360_Orders)",
                    "total_revenue": "SUM(Customer_360_Orders[Revenue])",
                    "total_profit": "SUM(Customer_360_Orders[Profit])",
                    "aov": "DIVIDE([Total Revenue], [Total Orders])",
                    "profit_margin_percent": "DIVIDE([Total Profit], [Total Revenue]) * 100",
                    "total_tickets": "COUNTROWS(Customer_360_Tickets)"
                },
                "key_metrics": [
                    "Customer demographics (age, gender, location, signup trends)",
                    "Revenue trends by year and product category",
                    "Profit margins and profitability by category",
                    "Ticket volume and resolution metrics"
                ],
                "visualizations": ["KPI Cards", "Line Charts", "Column Charts", "Pie/Donut Charts", "Tables"],
                "business_impact": "Enables customer engagement strategies, retention focus, and cross-sell opportunities"
            },

            "Retail Sales Dashboard": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Sales-Dashboard-PowerBI-Project",
                "data_model": "Fact Table Model (single comprehensive retail sales table)",
                "objective": "Real-time monitoring of sales, profit, and customer behavior across dimensions",
                "dax_measures": {
                    "total_sales": "SUM('Retail_Sales_Synthetic'[Total_Sales])",
                    "total_profit": "SUM('Retail_Sales_Synthetic'[Profit])",
                    "profit_margin_percent": "DIVIDE([Total Profit], [Total Sales]) * 100",
                    "total_orders": "DISTINCTCOUNT('Retail_Sales_Synthetic'[Order_ID])",
                    "aov": "DIVIDE([Total Sales], [Total Orders])"
                },
                "key_metrics": [
                    "Sales performance by category, region, and channel",
                    "Profit trends and margin analysis",
                    "Product category performance (top/bottom performers)",
                    "Regional and channel comparison (Online/Retail/Distributor)"
                ],
                "visualizations": ["KPI Cards", "Line Charts", "Column Charts", "Gauge Charts", "Tables"],
                "business_impact": "Enables inventory optimization, pricing decisions, and channel strategy"
            },

            "Telco Customer Churn Dashboard": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Customer-Churn-Dashboard-PowerBI-Project",
                "dataset": "7,000 telecom customers (Kaggle dataset)",
                "objective": "Analyze churn patterns and identify key retention drivers",
                "dax_measures": {
                    "total_customers": "COUNTROWS('WA_Fn-UseC_-Telco-Customer-Churn')",
                    "churned_customers": "CALCULATE(COUNTROWS(...), [Churn] = 'Yes')",
                    "churn_rate_percent": "DIVIDE([Churned Customers], [Total Customers], 0)",
                    "avg_monthly_charges": "AVERAGE(...[MonthlyCharges])"
                },
                "key_findings": [
                    "Month-to-month contracts: 40.48% churn",
                    "Electronic check payments: 45.29% churn (3x higher than auto-pay)",
                    "Senior citizens: 41.68% churn vs 23.65% non-seniors",
                    "Customers with 3+ add-on services: 50%+ lower churn"
                ],
                "visualizations": ["KPI Cards", "Column Charts", "Pie/Donut Charts", "Bar Charts", "Tables"],
                "business_impact": "Identifies 1,869 churned customers; supports $4-5M retention strategy"
            },

            "Financial Performance Dashboard": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Financial-Performance-Dashboard-PowerBI-Project",
                "objective": "Monitor revenue, expenses, profit, and investment trends with DAX-driven KPIs",
                "dax_measures": {
                    "total_revenue": "CALCULATE(SUM(...[Amount]), [Category] = 'Revenue')",
                    "total_expenses": "CALCULATE(SUM(...[Amount]), [Category] = 'Expense')",
                    "total_investments": "CALCULATE(SUM(...[Amount]), [Category] = 'Investment')",
                    "net_profit": "[Total Revenue] + [Total Expenses]",
                    "yoy_revenue_growth_percent": "Complex VAR calculation for year-over-year growth"
                },
                "key_metrics": [
                    "Revenue trends (monthly, yearly)",
                    "Expense distribution by department/region",
                    "Profit analysis and margin tracking",
                    "YoY growth calculations",
                    "Regional/departmental financial contribution"
                ],
                "visualizations": ["KPI Cards", "Line Charts", "Column Charts", "Pie Charts", "Drill-through"],
                "business_impact": "Supports strategic financial planning and budget optimization"
            }
        },

        # ==================== PYTHON PROJECTS ====================
        "Python": {
            "Retail Customer Segmentation": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Retail-Customer-Segmentation-Python-Project",
                "dataset_size": "1,000 transactions from 100 unique customers over 24 months",
                "objective": "Segment retail customers using RFM analysis and K-Means clustering",
                "techniques": ["RFM Analysis", "K-Means Clustering", "Elbow Method", "StandardScaler"],
                "key_code_snippets": {
                    "rfm_aggregation": "rfm = df.groupby('CustomerID').agg({'InvoiceDate': lambda x: (snapshot_date - x.max()).days, 'InvoiceNo': 'count', 'Amount': 'sum'})",
                    "standardization": "rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])",
                    "kmeans": "kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)",
                    "roi_calculation": "(Revenue – Budget) / Budget × 100"
                },
                "segments": {
                    "Churned/Inactive": {"count": 7, "avg_recency": "301.9 days", "avg_frequency": 7.6, "avg_monetary": "$7,951.40"},
                    "Medium-Value Active": {"count": 42, "avg_recency": "60.3 days", "avg_frequency": 10.0, "avg_monetary": "$10,407.30"},
                    "Recent Buyers": {"count": 28, "avg_recency": "46.1 days", "avg_frequency": 7.2, "avg_monetary": "$6,885.70"},
                    "VIP/High-Value": {"count": 23, "avg_recency": "55.9 days", "avg_frequency": 14.1, "avg_monetary": "$15,009.90"}
                },
                "business_impact": "Identifies VIP customers (23), inactive accounts (7), and retention opportunities"
            },

            "Healthcare Patient Analytics": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Patient-Analytics-Python-Project",
                "dataset_size": "100,000 patient admissions with comprehensive health metrics",
                "objective": "Analyze patient factors influencing length of stay and segment by risk level",
                "techniques": ["EDA", "Feature Engineering", "Comorbidity Analysis", "Risk Stratification"],
                "key_findings": {
                    "high_risk_patients": "6,900 (6.9%) with 3+ comorbidities",
                    "avg_los_high_risk": "5.96 days",
                    "avg_los_normal_risk": "3.86 days",
                    "los_multiplier": "1.54× longer for high-risk patients",
                    "avg_comorbidities": "0.71 per patient",
                    "max_comorbidities": "8 chronic conditions"
                },
                "visualizations": ["Histograms", "Boxplots", "Correlation Heatmap", "Scatter Plots", "Line Charts"],
                "business_impact": "Identifies 6,900 high-risk patients for enhanced care coordination; optimizes resource allocation"
            },

            "Airbnb NYC Price Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Airbnb-NYC-Price-Analysis-Python-Project",
                "dataset_size": "48,895 NYC listings (2019) across 5 boroughs and 221 neighborhoods",
                "objective": "Analyze Airbnb pricing trends, room type variations, and seasonal patterns",
                "key_metrics": {
                    "total_listings": "48,895 (cleaned: 48,392)",
                    "avg_price": "$152.72 per night",
                    "median_price": "$106 per night",
                    "price_range": "$0 - $10,000",
                    "top_neighborhood": "Manhattan area (most expensive)",
                    "room_type_avg_entire": "Entire home premium pricing",
                    "room_type_avg_private": "Private room mid-range",
                    "room_type_avg_shared": "Shared room budget option"
                },
                "techniques": ["Data Cleaning", "Outlier Removal", "Normalization", "Groupby Operations", "Temporal Analysis"],
                "visualizations": ["Bar Charts", "Box Plots", "Histograms", "Scatter Plots"],
                "business_impact": "Identifies pricing opportunities and neighborhood premium positioning for hosts"
            },

            "Sales Forecasting Time Series": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Sales-Forecasting-Time-Series-Python-Project",
                "dataset_size": "185,000 transactions from 12 monthly files (Jan-Dec 2019)",
                "objective": "Analyze 12-month sales and build ARIMA model for future forecasting",
                "key_metrics": {
                    "annual_revenue": "~$34.5M",
                    "avg_transaction": "~$185",
                    "top_cities": "San Francisco, Los Angeles, New York, Boston, Dallas",
                    "unique_products": "19 products",
                    "dec_revenue": "$4.6M (+34% above average)",
                    "march_revenue": "Lowest month",
                    "arima_mape": "6.2% forecast accuracy"
                },
                "techniques": ["File Consolidation", "Address Parsing", "Temporal Analysis", "ARIMA Modeling", "Forecast Evaluation"],
                "key_code_snippets": {
                    "arima_model": "ARIMA(train, order=(1,1,1))",
                    "forecast_mape": "6.2%",
                    "top_products": "Mac Book Pro (18%), iPhone (16.8%), Google Pixel (10.1%)"
                },
                "business_impact": "Forecasts monthly revenue with 6.2% accuracy; supports inventory and budget planning"
            }
        },

        # ==================== SQL PROJECTS ====================
        "SQL": {
            "Healthcare Claims Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Healthcare-Claims-Analysis-SQL-Project",
                "dataset_size": "2,999 insurance claims across 500 patients and 50 providers",
                "objective": "Analyze claims portfolio, identify fraud, and optimize provider performance",
                "key_metrics": {
                    "total_claims": "2,999",
                    "fraud_flagged": "100 claims (3.34%)",
                    "avg_claim": "$25,192.23",
                    "approved_rate": "48.3% (1,450)",
                    "denied_rate": "27.5% (824)",
                    "pending_rate": "24.2% (725)",
                    "debit_card_avg": "$25,591.75 (highest)",
                    "net_banking_avg": "$24,078.37 (lowest)"
                },
                "sql_techniques": ["Multi-table joins", "Window functions", "CASE statements", "Aggregations", "HAVING clause"],
                "key_queries": [
                    "Average claim by payment method",
                    "Claims by age group categorization",
                    "Top 10 providers by claim volume",
                    "Fraud-flagged claims analysis",
                    "High-cost patients ranking",
                    "Diagnosis-wise claim comparison",
                    "Monthly claims trend analysis",
                    "Cumulative claims per patient (window function)",
                    "Rank patients by total claims"
                ],
                "business_impact": "Identifies $2.65M fraudulent payouts prevented; evaluates 50 providers for network optimization"
            },

            "Bank Customer Segmentation": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Bank-Customer-Segmentation-SQL-Project",
                "dataset_size": "1,000 banking customers across 4 regions",
                "objective": "Segment customers by financial metrics to optimize relationship management",
                "key_metrics": {
                    "high_value_customers": "306 (30.6%) with Income ≥1M AND Balance ≥800K",
                    "mid_tier": "591 (59.1%) with Income 500K-999K",
                    "mass_market": "103 (10.3%) with lower income",
                    "south_region_high_value": "96 customers (31.4%)",
                    "avg_loans_per_customer": "2.5",
                    "avg_credit_cards": "1.6"
                },
                "sql_techniques": ["Customer segmentation CASE", "Regional grouping", "Financial profiling", "Cross-sell analysis"],
                "key_queries": [
                    "Customer segmentation by financial criteria",
                    "Geographic distribution analysis",
                    "Regional high-value customer ranking",
                    "Segment financial summary",
                    "Cross-sell opportunity analysis (loans & credit cards)",
                    "Engagement & balance matrix",
                    "Account type performance comparison"
                ],
                "business_impact": "Identifies 306 high-value customers (30.6%); enables personalized marketing and product targeting"
            },

            "Telco Churn Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Telco-Churn-Analysis-SQL-Project",
                "dataset_size": "7,032 customers from Kaggle Telco dataset",
                "objective": "Identify churn patterns and develop retention strategies",
                "key_metrics": {
                    "overall_churn_rate": "26.54% (1,869 churned)",
                    "retention_rate": "73.46%",
                    "month_to_month_churn": "42.71%",
                    "two_year_churn": "2.85%",
                    "electronic_check_churn": "45.29%",
                    "credit_card_churn": "15.25%",
                    "senior_citizen_churn": "41.68%",
                    "avg_monthly_churned": "$74.44",
                    "avg_monthly_retained": "$61.31",
                    "avg_tenure_churned": "18.0 months",
                    "avg_tenure_retained": "37.7 months"
                },
                "sql_techniques": ["Churn rate calculations", "Contract type segmentation", "Payment method analysis", "Risk categorization"],
                "key_queries": [
                    "Overall churn distribution",
                    "Churn by contract type",
                    "Churn by payment method",
                    "Average charges and tenure comparison",
                    "Senior citizen churn analysis",
                    "Internet service type churn impact",
                    "Service adoption impact (add-ons reduce churn 50%+)",
                    "Tenure-based churn windows",
                    "High-risk segment identification",
                    "Gender and partnership impact"
                ],
                "business_impact": "Revenue protection: $4-5M annual churn losses identified; contract optimization enables 40% churn reduction"
            },

            "Inventory Supplier Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Inventory-Supplier-Analysis-SQL-Project",
                "dataset_size": "1,200 products across 8 categories from 50 suppliers",
                "objective": "Optimize inventory levels and assess supplier dependencies",
                "key_metrics": {
                    "total_products": "1,200",
                    "products_below_reorder": "255 (21.25%)",
                    "emergency_stock": "34 products (<25 units)",
                    "stockout_risk": "1 product at 0 units",
                    "clothing_turnover": "5.35x (highest)",
                    "toys_turnover": "4.52x (lowest)",
                    "top_supplier_dependency": "Supplier_29: 33 products (2.75%)",
                    "concentration_risk_top10": "26.33% of portfolio"
                },
                "sql_techniques": ["Stock status classification", "Turnover ratio calculation", "Supplier dependency analysis", "Reorder prioritization"],
                "key_queries": [
                    "Stock levels & reorder alerts",
                    "Supplier dependency analysis",
                    "Product inventory turnover",
                    "Category-wise performance",
                    "Reorder priority ranking",
                    "High-turnover products (Top 50)",
                    "Low stock alerts with days-to-stockout",
                    "Supplier performance metrics",
                    "Category performance dashboard",
                    "Stock status classification"
                ],
                "business_impact": "Prevents $1.5-2M in lost sales; reduces carrying costs $300-400K annually; identifies supply chain resilience"
            },

            "Hospital Patient Analysis": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Hospital-Patient-Analysis-SQL-Project",
                "dataset_size": "1,000 patient records across 7 medical departments",
                "objective": "Analyze admissions, treatment outcomes, and optimize resource allocation",
                "key_metrics": {
                    "total_patients": "1,000",
                    "total_physicians": "50",
                    "cardiology_admissions": "163 (16.3%)",
                    "pediatrics_admissions": "150 (15.0%)",
                    "recovery_rate": "70.4% (704 patients)",
                    "referred_rate": "23.4%",
                    "mortality_rate": "6.2% (62 patients)",
                    "avg_stay_general_surgery": "16.46 days (longest)",
                    "avg_stay_pediatrics": "14.69 days (most efficient)",
                    "avg_bill_deceased": "$26,816.29",
                    "avg_bill_recovered": "$24,990.34"
                },
                "sql_techniques": ["Department performance analysis", "Outcome classification", "Financial impact analysis", "Physician workload ranking"],
                "key_queries": [
                    "Patient admissions by department",
                    "Average length of stay comparison",
                    "Treatment outcomes overview",
                    "Average bill by outcome",
                    "Top doctors by patient load",
                    "Department efficiency rankings",
                    "Physician specialization analysis"
                ],
                "business_impact": "70.4% recovery rate demonstrates quality care; identifies 16.46-day avg stays for General Surgery optimization"
            },

            "Loan Default Prediction": {
                "url": "https://github.com/Robin-Jimmichan-Pooppally/Loan-Default-Prediction-SQL-Project",
                "dataset_size": "1,000 loan records with borrower profiles and risk assessment",
                "objective": "Assess loan portfolio risk and identify high-risk borrowers for intervention",
                "key_metrics": {
                    "total_loans": "1,000",
                    "good_repayment": "786 (78.60%)",
                    "average_repayment": "204 (20.40%)",
                    "poor_repayment": "10 (1.00%)",
                    "low_risk_borrowers": "272 (27.2%) credit score ≥750",
                    "medium_risk": "594 (59.4%) credit score 600-749",
                    "high_risk": "134 (13.4%) credit score <600",
                    "low_risk_avg_loan": "$130,680.51",
                    "high_risk_avg_loan": "$77,152.50",
                    "high_risk_portfolio_value": "0.14% of total"
                },
                "sql_techniques": ["Risk categorization", "Default rate analysis", "Portfolio segmentation", "Credit score ranking"],
                "key_queries": [
                    "Overall loan default rate",
                    "High-risk borrowers identification",
                    "Average loan amount by risk category",
                    "Risk segmentation by credit score",
                    "Loan amount vs risk analysis"
                ],
                "business_impact": "Identifies 150 high-risk borrowers for monitoring; conservative loan sizing limits exposure; prevents $400K-600K default losses"
            }
        }
    },

    "skills_matrix": {
        "Data Analysis": ["Excel Pivot Tables", "SQL Aggregations", "Python Pandas", "Statistical Analysis"],
        "Visualization": ["Power BI DAX & Measures", "Excel Charts", "Python Matplotlib/Seaborn", "Interactive Dashboards"],
        "Programming": ["Python (Pandas, NumPy, Scikit-learn)", "SQL (MySQL, Window Functions)", "DAX", "M Query"],
        "Statistical Methods": ["RFM Analysis", "K-Means Clustering", "ARIMA Forecasting", "Risk Stratification", "Correlation Analysis"],
        "Domains": ["E-commerce", "Healthcare", "Finance/Banking", "Telecommunications", "Retail", "Supply Chain", "Insurance"]
    },

    "technical_details": {
        "excel_techniques": [
            "Pivot Tables with multi-dimensional analysis",
            "Pivot Charts (Column, Bar, Pie, Line, Donut)",
            "Slicers for interactive filtering",
            "Conditional Formatting (color scales, 5-color legends)",
            "Data Validation and error checking",
            "Cell-based Formulas (VLOOKUP, SUM, AVERAGE, IF/CASE)",
            "Derived Columns and segmentation"
        ],
        "power_bi_techniques": [
            "Multi-table relational modeling (Star Schema, Fact-Dimension)",
            "DAX Measures (DISTINCTCOUNT, CALCULATE, DIVIDE, SUM)",
            "Window Functions in DAX",
            "KPI Cards and Gauge Charts",
            "Cross-filtering and drill-through",
            "Slicers with multiple dimensions",
            "Tabular data modeling optimization"
        ],
        "python_techniques": [
            "Exploratory Data Analysis (EDA)",
            "Feature Engineering (RFM, comorbidity counts, temporal extraction)",
            "Clustering (K-Means with StandardScaler, Elbow Method)",
            "Time Series Analysis (ARIMA modeling with statsmodels)",
            "Pandas groupby operations and aggregations",
            "Matplotlib & Seaborn visualizations",
            "Scikit-learn preprocessing and model evaluation"
        ],
        "sql_techniques": [
            "Complex queries with multiple JOINs",
            "Subqueries for nested analysis",
            "Window Functions (ROW_NUMBER, RANK, SUM OVER)",
            "CASE statements for multi-level categorization",
            "Group By with HAVING clauses",
            "Date functions (YEAR, MONTH, DATEDIFF)",
            "Aggregation functions (COUNT, SUM, AVG, MIN, MAX)",
            "Percentage calculations and ranking"
        ]
    },

    "key_business_outcomes": [
        "Churn Prevention: $4-5M annual revenue protection through retention strategies",
        "Fraud Detection: $2.65M fraudulent claims prevented in healthcare",
        "Cost Optimization: $300-400K inventory carrying cost reduction",
        "Revenue Growth: 10-15% marketing ROI improvement through optimization",
        "Quality Assurance: 70.4% hospital recovery rate; 78.6% loan repayment success",
        "Customer Segmentation: Enabled targeted marketing to 306 high-value banking customers",
        "Forecasting Accuracy: 6.2% MAPE in sales forecasting for 12-month projections",
        "Operational Efficiency: Identified department bottlenecks; resource allocation optimization",
        "Risk Management: 150+ high-risk customers/loans identified for intervention"
    ],

    "faq": {
        "What technologies do you use?": "Robin specializes in Excel, Power BI, Python, and SQL. Expert in data cleaning, visualization, statistical analysis, and machine learning across business analytics.",
        
        "How many projects have you completed?": "21 verified Business Analytics projects: 6 Excel, 5 Power BI, 4 Python, 6 SQL. Total 185,000+ records analyzed.",
        
        "Can you handle large datasets?": "Yes—experience from 1,000 to 100,000+ records. Proven with 185,000 e-commerce transactions, 100,000 patient records, 7,000+ customer datasets.",
        
        "What's your strongest technical skill?": "Data modeling and complex SQL analysis. Also expert in DAX measures and Python statistical forecasting.",
        
        "Show me your best project": "Retail Customer Segmentation (Python): RFM + K-Means clustering identified 4 customer segments including 23 VIP customers ($15K average value) from 100 customers.",
        
        "Can you explain a specific formula?": "Sure! For example: ARIMA(1,1,1) model achieves 6.2% MAPE on sales forecasting. Or Excel pivot table ROI calc: (Revenue-Budget)/Budget*100.",
        
        "What's your data analysis approach?": "1) Understand business objective 2) Clean & validate data 3) Exploratory analysis 4) Statistical modeling 5) Visualization 6) Actionable insights.",
        
        "Do you work with real data?": "Mix of real (Kaggle Telco 7,000 records, Airbnb NYC 48,895 listings) and synthetic datasets carefully designed to demonstrate realistic scenarios.",
        
        "Fastest way to learn your projects?": "Start with Telco Churn (Excel) for pivot table basics, then Power BI Customer 360 for DAX, then Python segmentation for ML, finally SQL Healthcare Claims for complex queries."
    },

    "greeting_message": (
        "👋 Hi there! I'm **Portfoli-AI**, Robin Jimmichan's portfolio assistant.\n\n"
        "You can ask me about any of Robin's **21 Business Analytics projects** across Excel, Power BI, Python, and SQL.\n\n"
        "I can help you explore:\n"
        "• 📊 Project details, datasets, and business impact\n"
        "• 💻 Technical implementation (DAX, SQL, Python code)\n"
        "• 📈 Key metrics, findings, and visualizations\n"
        "• 🔍 Specific techniques and methodologies\n"
        "• 💡 Business insights and recommendations\n\n"
        "Try asking:\n"
        "👉 *'Explain the Telco Churn project'*\n"
        "👉 *'Show me the ARIMA model code'*\n"
        "👉 *'What's the highest churn rate you found?'*\n"
        "👉 *'Compare Excel vs Power BI projects'*\n\n"
        "Let's explore Robin's analytics portfolio! 🚀"
    )
}
