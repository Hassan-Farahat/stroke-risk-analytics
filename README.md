# 🏥 Healthcare Stroke Risk Analytics

An interactive healthcare analytics dashboard evaluating stroke risk factors across patient demographics, glucose levels, and BMI status. Built using Python, SQL Server via SQLAlchemy, and Streamlit.

🔗 **Live Demo:** https://hassan-farahat-stroke-risk-analytics-app-v2vsnx.streamlit.app

## 🛠️ Tech Stack & Architecture

* **Language:** Python
* **Database:** SQL Server (SQLAlchemy + PyODBC)
* **Frontend Dashboard:** Streamlit
* **Visualization:** Seaborn, Matplotlib

## ✨ Features

* Automated data ingestion pipeline handling missing values via subgroup median imputation and storing clean records in SQL Server.
* Dynamic sidebar filtering across Gender, Work Type, Age Range, and Hypertension status.
* Key performance metrics tracking total patients, stroke counts, stroke rate (%), and average glucose levels.
* Exploratory visualizations analyzing stroke prevalence across age tiers and glucose-to-BMI scatter distributions.
* Embedded dataset inspector for direct data exploration.

## 🚀 How to Run Locally

Clone the repository:
   ```bash
   git clone [https://github.com/Hassan-Farahat/stroke-risk-analytics.git](https://github.com/Hassan-Farahat/stroke-risk-analytics.git)
