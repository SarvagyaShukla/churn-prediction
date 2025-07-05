import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# -------------------------------
# 1) Streamlit page setup & title
# -------------------------------
st.set_page_config(page_title="Churn Dashboard", layout="wide")
st.markdown("<h1 style='text-align: center; color: teal;'>📊 Telecom Customer Churn Dashboard</h1>", unsafe_allow_html=True)
st.write("---")

# Snowflake connection info
SNOWFLAKE_USER = "ss"
SNOWFLAKE_PASSWORD = "Savv1234567890"
SNOWFLAKE_ACCOUNT = "mdrgqzk-uz88701"  # e.g., 'xy12345.us-east-1'
SNOWFLAKE_DATABASE = 'TELECOM_DB'
SNOWFLAKE_SCHEMA = 'CHURN_SCHEMA'
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"

# SQLAlchemy engine
engine = create_engine(
    f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/'
    f'{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}'
)

# -------------------------------
# 3) Load predictions from Snowflake
# -------------------------------
query = "SELECT * FROM CHURN_PREDICTIONS;"
df = pd.read_sql(query, engine)
st.success("✅ Predictions loaded successfully.")

# -------------------------------
# 4) Customer selection
# -------------------------------
customer_ids = df.index.tolist()
customer_idx = st.selectbox("🔎 Select Customer Index", customer_ids)
customer = df.loc[customer_idx]

# -------------------------------
# 5) Show customer details
# -------------------------------
st.subheader(f"📌 Customer Index: {customer_idx}")
st.dataframe(customer.to_frame().T, use_container_width=True)

# -------------------------------
# 6) Show churn probability with color-coded risk
# -------------------------------
churn_prob = customer['predicted_churn_prob'] * 100
risk_color = "green"
if churn_prob >= 70:
    risk_color = "red"
elif churn_prob >= 40:
    risk_color = "orange"

st.markdown(
    f"""
    <div style='text-align: center; font-size: 28px;'>
        <span>🛑 Churn Probability: <span style='color: {risk_color};'>{churn_prob:.2f}%</span></span>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# 7) Business-friendly explanation of prediction vs. actual outcome
# -------------------------------
actual_churn = customer['actual_churn']  # 1 if churned, 0 if stayed

if actual_churn == 1 and churn_prob < 50:
    explanation = (
        "ℹ️ **Explanation:**\n\n"
        "The model thought this customer was likely to stay (churn probability is low), "
        "but they actually churned. This means the model missed something about why they left, "
        "and we may need to add more data about customer behavior or experience."
    )
elif actual_churn == 0 and churn_prob >= 50:
    explanation = (
        "ℹ️ **Explanation:**\n\n"
        "The model predicted high risk of churn, but the customer actually stayed. "
        "This could mean the customer had risk factors but was retained, or the model overestimated their risk."
    )
else:
    explanation = (
        "ℹ️ **Explanation:**\n\n"
        "The model prediction and the actual outcome agree for this customer. "
        "This means the model successfully captured the customer's churn behavior."
    )

st.info(explanation)

# -------------------------------
# 8) Feature comparison with averages
# -------------------------------
st.subheader("📊 Feature Comparison with Averages")

# Calculate averages for churned and non-churned customers
churned_avg = df[df['actual_churn'] == 1][['tenure', 'monthlycharges', 'totalcharges']].mean()
nonchurned_avg = df[df['actual_churn'] == 0][['tenure', 'monthlycharges', 'totalcharges']].mean()

comparison_df = pd.DataFrame({
    'Churned Avg': churned_avg,
    'Stayed Avg': nonchurned_avg,
    'Customer': customer[['tenure', 'monthlycharges', 'totalcharges']]
})

fig, ax = plt.subplots(figsize=(8,5))
comparison_df.plot(kind='bar', ax=ax)
plt.title(f"Customer {customer_idx} vs. Churned & Non-Churned Averages")
plt.ylabel("Value")
plt.xticks(rotation=0)
st.pyplot(fig)