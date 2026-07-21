import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Prediction",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Customer Churn Prediction")

st.markdown("---")

# ===============================
# Load Models
# ===============================

MODELS = {
    "Decision Tree": "models/DecisionTree.pkl",
    "KNN Classifier": "models/KNNClassifier.pkl",
    "Naive Bayes": "models/NaiveBayes.pkl",
    "Random Forest": "models/RandomForest.pkl"
}

model_name = st.selectbox(
    "Select Machine Learning Model",
    list(MODELS.keys())
)

model = joblib.load(MODELS[model_name])

st.success(f"✅ {model_name} Loaded Successfully")

st.markdown("---")

st.header("📝 Customer Information")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=650,
            help="Customer credit score"
        )

        geography = st.selectbox(
            "Country",
            ["France", "Germany", "Spain"]
        )

        gender = st.radio(
            "Gender",
            ["Male", "Female"],
            horizontal=True
        )

        age = st.slider(
            "Age",
            18,
            100,
            35
        )

        tenure = st.slider(
            "Years with Bank",
            0,
            10,
            5
        )

    with col2:

        balance = st.number_input(
            "Account Balance",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

        products = st.selectbox(
            "Number of Products",
            [1,2,3,4]
        )

        card = st.radio(
            "Has Credit Card?",
            [1,0],
            format_func=lambda x: "Yes" if x==1 else "No",
            horizontal=True
        )

        active = st.radio(
            "Active Member?",
            [1,0],
            format_func=lambda x: "Yes" if x==1 else "No",
            horizontal=True
        )

        salary = st.number_input(
            "Estimated Salary",
            min_value=0.0,
            value=100000.0,
            step=1000.0
        )

    predict = st.form_submit_button(
        "🔮 Predict Customer Churn",
        use_container_width=True
    )

# ============================================
# Prediction
# ============================================

if predict:

    input_data = pd.DataFrame({
        "CreditScore":[credit_score],
        "Geography":[geography],
        "Gender":[gender],
        "Age":[age],
        "Tenure":[tenure],
        "Balance":[balance],
        "NumOfProducts":[products],
        "HasCrCard":[card],
        "IsActiveMember":[active],
        "EstimatedSalary":[salary]
    })

    st.subheader("Input Data")

    st.dataframe(input_data, use_container_width=True)

    prediction = model.predict(input_data)[0]

    st.markdown("---")

    st.header("Prediction Result")

    if prediction == 1:

        st.error("❌ Customer is likely to Exit (Churn).")

    else:

        st.success("✅ Customer is likely to Stay.")

    # =====================================
    # Probability (if available)
    # =====================================

    if hasattr(model, "predict_proba"):

        probability = model.predict_proba(input_data)[0]

        stay_prob = probability[0] * 100
        exit_prob = probability[1] * 100

        st.markdown("---")

        st.subheader("Prediction Probability")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Stay Probability",
                f"{stay_prob:.2f}%"
            )
            st.progress(min(int(stay_prob), 100))

        with col2:
            st.metric(
                "Exit Probability",
                f"{exit_prob:.2f}%"
            )
            st.progress(min(int(exit_prob), 100))

    st.markdown("---")

    st.subheader("Prediction Summary")

    summary = pd.DataFrame({
        "Feature": input_data.columns,
        "Value": input_data.iloc[0].values
    })

    st.dataframe(summary, use_container_width=True)

    st.success("Prediction Completed Successfully ✅")