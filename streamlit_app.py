import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Streamlit page config
st.set_page_config(page_title="Churn Dashboard", layout="wide")
st.title("📊 Telecom Churn Prediction Dashboard")

# Snowflake connection info
SNOWFLAKE_USER = "ss"
SNOWFLAKE_PASSWORD = "Savv1234567890"
SNOWFLAKE_ACCOUNT = "mdrgqzk-uz88701"  # e.g., 'xy12345.us-east-1'
SNOWFLAKE_DATABASE = 'TELECOM_DB'
SNOWFLAKE_SCHEMA = 'CHURN_SCHEMA'
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"

# Snowflake SQLAlchemy engine
engine = create_engine(
    f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/'
    f'{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}'
)

# Load churn predictions from Snowflake
query = "SELECT * FROM CHURN_PREDICTIONS;"
df = pd.read_sql(query, engine)

st.write("✅ Predictions loaded successfully.")

# Select a customer ID to view details
customer_id = st.selectbox("Select Customer ID", df.index)

customer = df.loc[customer_id]
st.subheader(f"📌 Customer ID: {customer_id}")
st.write(customer)

# Show churn probability
st.metric("Churn Probability", f"{customer['predicted_churn_prob']:.2%}")

# Add a bar chart of features for this customer
st.subheader("Customer Features")
st.bar_chart(customer[['tenure', 'monthlycharges', 'totalcharges']])
