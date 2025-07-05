# import pandas as pd
# import snowflake.connector
# from sqlalchemy import create_engine
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix
# import shap

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report, confusion_matrix

# -------------------------------
# Snowflake connection parameters
# -------------------------------
SNOWFLAKE_USER = "ss"
SNOWFLAKE_PASSWORD = "Savv1234567890"
SNOWFLAKE_ACCOUNT = "mdrgqzk-uz88701"  # e.g., 'xy12345.us-east-1'
SNOWFLAKE_DATABASE = 'TELECOM_DB'
SNOWFLAKE_SCHEMA = 'CHURN_SCHEMA'
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"

# SQLAlchemy engine to connect to Snowflake
engine = create_engine(
    f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/'
    f'{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}?warehouse={SNOWFLAKE_WAREHOUSE}'
)

# ----------------------------------
# 1) Load data from Snowflake
# ----------------------------------
query = "SELECT * FROM CUSTOMER_DATA;"
df = pd.read_sql(query, engine)
print("\n✅ Data loaded successfully. Sample:\n")
print(df.head())
print("\nColumns in dataframe:", df.columns.tolist())

# ----------------------------------
# 2) Explore churn distribution
# ----------------------------------
print("\n✅ Churn distribution:\n")
print(df['churn'].value_counts())
sns.countplot(data=df, x='churn')
plt.title("Churn Distribution")
plt.show()

# ----------------------------------
# 3) Prepare data
# ----------------------------------
df['churn_label'] = df['churn'].map({'No': 0, 'Yes': 1})
features = ['tenure', 'monthlycharges', 'totalcharges', 'seniorcitizen']
X = df[features]
y = df['churn_label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.3, random_state=42
)

# ----------------------------------
# 4) Train Random Forest model
# ----------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

print("\n✅ Model performance:")
print("ROC AUC Score:", roc_auc_score(y_test, y_prob))
print(classification_report(y_test, y_pred))

sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# ----------------------------------
# 5) Feature importance
# ----------------------------------
importances = model.feature_importances_
fi_df = pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values(by='Importance', ascending=False)
print("\n✅ Feature importance:\n", fi_df)

plt.figure(figsize=(8,5))
plt.barh(fi_df['Feature'], fi_df['Importance'])
plt.xlabel("Importance")
plt.title("Feature Importance")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# ----------------------------------
# 6) Overwrite predictions directly to Snowflake table
# ----------------------------------
results_df = X_test.copy()
results_df['predicted_churn_prob'] = y_prob
results_df['actual_churn'] = y_test.values

# Truncate existing data in the table
with engine.connect() as conn:
    conn.execute(text("TRUNCATE TABLE CHURN_SCHEMA.CHURN_PREDICTIONS;"))
    print("\n✅ Table CHURN_PREDICTIONS truncated successfully.")

# Insert new predictions
results_df.to_sql(
    'CHURN_PREDICTIONS',
    con=engine,
    index=False,
    if_exists='append',
    method='multi'
)
print("\n✅ Predictions written directly to CHURN_SCHEMA.CHURN_PREDICTIONS table in Snowflake.")