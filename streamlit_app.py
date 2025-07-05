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
# 4) Customer risk category selection
# -------------------------------
st.subheader("🔎 Choose Risk Category")

risk_category = st.selectbox(
    "Select a category of customers:",
    [
        "All Customers",
        "High Risk (≥70%)",
        "Medium Risk (40–70%)",
        "Low Risk (<40%)",
        "Already Churned"
    ]
)

if risk_category == "High Risk (≥70%)":
    filtered_df = df[(df['predicted_churn_prob'] >= 0.70) & (df['actual_churn'] == 0)]
elif risk_category == "Medium Risk (40–70%)":
    filtered_df = df[(df['predicted_churn_prob'] >= 0.40) & (df['predicted_churn_prob'] < 0.70) & (df['actual_churn'] == 0)]
elif risk_category == "Low Risk (<40%)":
    filtered_df = df[(df['predicted_churn_prob'] < 0.40) & (df['actual_churn'] == 0)]
elif risk_category == "Already Churned":
    filtered_df = df[df['actual_churn'] == 1]
else:
    filtered_df = df.copy()

st.write(f"Found {len(filtered_df)} customers in '{risk_category}' category.")

if len(filtered_df) > 0:
    customer_idx = st.selectbox("Select Customer Index", filtered_df.index.tolist())
    customer = filtered_df.loc[customer_idx]
else:
    st.warning("No customers found in this category.")
    st.stop()

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
# 7) Detailed explanation with color box
# -------------------------------
actual_churn = customer['actual_churn']

if actual_churn == 1:
    explanation_color = "red"
    explanation = (
        f"🔴 **Customer has already churned.**\n\n"
        f"The model predicted a churn probability of **{churn_prob:.2f}%**, but this customer has already left. "
        "This highlights areas where we can improve early detection."
    )
elif churn_prob >= 50:
    explanation_color = "orange"
    explanation = (
        f"🟠 **Customer is in the danger zone.**\n\n"
        f"The model predicts a **{churn_prob:.2f}%** chance of churn. "
        "The customer has not churned yet — proactive outreach is advised."
    )
else:
    explanation_color = "green"
    explanation = (
        f"🟢 **Customer appears safe.**\n\n"
        f"The model predicts a low churn probability of **{churn_prob:.2f}%**, "
        "and the customer has not churned."
    )

st.markdown(
    f"""
    <div style='border: 2px solid {explanation_color}; padding: 10px; border-radius: 8px;'>
        {explanation}
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------
# 8) Feature comparison with averages (normalized)
# -------------------------------
st.subheader("📊 Feature Comparison with Averages (Normalized)")

churned_avg = df[df['actual_churn'] == 1][['tenure', 'monthlycharges', 'totalcharges']].mean()
nonchurned_avg = df[df['actual_churn'] == 0][['tenure', 'monthlycharges', 'totalcharges']].mean()

comparison_df = pd.DataFrame({
    'Churned Avg': churned_avg,
    'Stayed Avg': nonchurned_avg,
    'Customer': customer[['tenure', 'monthlycharges', 'totalcharges']]
})

normalized_df = comparison_df / comparison_df.max()

fig, ax = plt.subplots(figsize=(8,5))
normalized_df.plot(kind='bar', ax=ax)
plt.title(f"Customer {customer_idx} vs. Churned & Non-Churned Averages (Normalized)")
plt.ylabel("Normalized Value (0–1)")
plt.xticks(rotation=0)
st.pyplot(fig)
plt.close(fig)

# -------------------------------
# 9) Overall churn distribution chart
# -------------------------------
st.write("---")
st.header("📊 Overall Analytics")

st.subheader("Churned vs. Stayed Customers")
churn_counts = df['actual_churn'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
churn_counts.plot(kind='bar', color=['green', 'red'], ax=ax1)
ax1.set_xticklabels(['Stayed', 'Churned'], rotation=0)
plt.ylabel("Number of Customers")
plt.title("Actual Churn Distribution")
st.pyplot(fig1)
plt.close(fig1)

# -------------------------------
# 10) Risk category distribution chart
# -------------------------------
st.subheader("Customers by Predicted Risk Categories")

risk_bins = pd.cut(
    df['predicted_churn_prob'],
    bins=[-0.01, 0.4, 0.7, 1],
    labels=['Low Risk', 'Medium Risk', 'High Risk']
)
risk_counts = risk_bins.value_counts().sort_index()

fig2, ax2 = plt.subplots()
risk_counts.plot(kind='bar', color=['green', 'orange', 'red'], ax=ax2)
plt.ylabel("Number of Customers")
plt.title("Predicted Risk Category Distribution")
st.pyplot(fig2)
plt.close(fig2)

# -------------------------------
# 11) Feature distribution example: tenure
# -------------------------------
st.subheader("Tenure Distribution by Actual Churn Status")

fig3, ax3 = plt.subplots()
lines = []
if not df[df['actual_churn']==0].empty:
    line_stayed = df[df['actual_churn']==0]['tenure'].plot(
        kind='hist', bins=30, alpha=0.5, label='Stayed', color='green', ax=ax3)
    lines.append(line_stayed)
if not df[df['actual_churn']==1].empty:
    line_churned = df[df['actual_churn']==1]['tenure'].plot(
        kind='hist', bins=30, alpha=0.5, label='Churned', color='red', ax=ax3)
    lines.append(line_churned)

plt.xlabel("Tenure (Months)")
plt.ylabel("Number of Customers")
plt.title("Tenure Distribution by Churn Status")

if lines:
    plt.legend()

st.pyplot(fig3)
plt.close(fig3)