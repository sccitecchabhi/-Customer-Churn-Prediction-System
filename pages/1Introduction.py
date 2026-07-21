import streamlit as st

st.set_page_config(
    page_title="Introduction",
    page_icon="🏠",
    layout="wide"
)

st.title("🏦 Customer Churn Prediction System")

st.markdown("---")

st.header("📌 Project Overview")

st.write("""
Customer Churn Prediction is a Machine Learning project that predicts
whether a customer is likely to leave the bank or continue using its services.

The prediction is based on customer information such as:

- Credit Score
- Geography
- Gender
- Age
- Tenure
- Balance
- Number of Products
- Has Credit Card
- Is Active Member
- Estimated Salary
""")

st.markdown("---")

st.header("🎯 Objective")

st.write("""
The objective of this project is to identify customers who are likely
to churn so that the bank can take preventive actions and improve
customer retention.
""")

st.markdown("---")

st.header("📂 Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Dataset Name**

    Customer Churn Modelling Dataset
    """)

with col2:
    st.info("""
    **Target Variable**

    Exited
    """)

st.markdown("---")

st.header("🤖 Machine Learning Algorithms Used")

st.success("✔ Decision Tree")
st.success("✔ K-Nearest Neighbors (KNN)")
st.success("✔ Naive Bayes")
st.success("✔ Random Forest")

st.markdown("---")

st.header("📊 Project Workflow")

st.write("""
1. Data Collection

2. Data Cleaning

3. Exploratory Data Analysis (EDA)

4. Feature Engineering

5. Model Training

6. Model Evaluation

7. Prediction
""")

st.markdown("---")

st.header("🛠 Technologies Used")

st.write("""
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-Learn
- Streamlit
""")

st.markdown("---")

st.success("✅ Use the sidebar to open the EDA and Prediction pages.")