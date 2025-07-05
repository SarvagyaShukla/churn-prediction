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
