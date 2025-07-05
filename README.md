# 📊 Telecom Customer Churn Prediction

This project predicts customer churn for a telecom company and visualizes results in a Streamlit dashboard.

---

## 🚀 What’s included?

- **churn_analysis.py**  
  Loads customer data from Snowflake, trains a churn prediction model, evaluates performance, and writes predictions back to Snowflake.

- **streamlit_app.py**  
  A modern Streamlit dashboard to explore churn predictions, customer details, and feature comparisons.

---

## 🏗️ How it works

1. **Data**  
   - Customer data is stored in Snowflake in the table: `CHURN_SCHEMA.CUSTOMER_DATA`.
   - Model predictions are saved to `CHURN_SCHEMA.CHURN_PREDICTIONS`.

2. **Model training**  
   - `churn_analysis.py` trains a Random Forest model on customer features like tenure and charges.
   - Predictions and churn probabilities are saved back to Snowflake.

3. **Dashboard**  
   - `streamlit_app.py` connects to Snowflake and shows:
     - Detailed customer information.
     - Predicted churn probability with color-coded risk.
     - A simple explanation comparing the model prediction with the actual churn outcome.
     - A bar chart comparing each customer’s features to averages for churned and non-churned customers.

---

## 📦 How to run it

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>

   Install dependencies:


pip install pandas scikit-learn matplotlib seaborn streamlit snowflake-sqlalchemy
Run churn analysis and write predictions to Snowflake:


python churn_analysis.py
Start the dashboard:


streamlit run streamlit_app.py


📝 Notes
Ensure your Snowflake credentials in both scripts are correct before running.

CHURN_PREDICTIONS table must exist; the first run of churn_analysis.py will overwrite it with predictions.

The dashboard will update automatically once new predictions are written.

The project was designed for demo and proof-of-concept purposes; it can be enhanced by adding more customer behavior data (e.g., service calls, competitor offers) for better accuracy.

📧 Contact
For questions or support, contact SARVAGYA SHUKLA.

