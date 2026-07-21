import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="EDA",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Exploratory Data Analysis")

# ----------------------------
# Load Dataset
# ----------------------------

@st.cache_data
def load_data():
    return pd.read_csv("cleaned_data.csv")

df = load_data()

st.success("Dataset Loaded Successfully ✅")

# ----------------------------
# Sidebar
# ----------------------------

eda = st.sidebar.radio(
    "EDA Sections",
    [
        "Dataset",
        "Data Cleaning",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Multivariate Analysis"
    ]
)

# ====================================
# Dataset
# ====================================

if eda=="Dataset":

    st.header("Dataset Overview")

    c1,c2,c3,c4=st.columns(4)

    c1.metric("Rows",df.shape[0])
    c2.metric("Columns",df.shape[1])
    c3.metric("Missing",df.isnull().sum().sum())
    c4.metric("Duplicate",df.duplicated().sum())

    st.markdown("---")

    st.subheader("First 10 Rows")

    st.dataframe(df.head(10),use_container_width=True)

    st.markdown("---")

    st.subheader("Last 10 Rows")

    st.dataframe(df.tail(10),use_container_width=True)

    st.markdown("---")

    st.subheader("Dataset Information")

    info = pd.DataFrame({
        "Column":df.columns,
        "Data Type":df.dtypes.astype(str),
        "Missing":df.isnull().sum().values,
        "Unique":df.nunique().values
    })

    st.dataframe(info,use_container_width=True)

    st.markdown("---")

    st.subheader("Statistical Summary")

    st.dataframe(df.describe().T,use_container_width=True)

# ====================================
# Data Cleaning
# ====================================

elif eda=="Data Cleaning":

    st.header("Data Cleaning")

    st.subheader("Missing Values")

    st.dataframe(df.isnull().sum())

    st.success(f"Total Missing Values : {df.isnull().sum().sum()}")

    st.markdown("---")

    st.subheader("Duplicate Values")

    st.write(df.duplicated().sum())

    st.markdown("---")

    st.subheader("Check Spaces")

    object_cols=df.select_dtypes(include="object").columns

    for col in object_cols:

        df[col]=df[col].str.strip()

    st.success("Leading & Trailing Spaces Removed")

    st.markdown("---")

    st.subheader("Gender Validation")

    valid_gender=["Male","Female"]

    invalid=df[~df["Gender"].isin(valid_gender)]

    if len(invalid)==0:

        st.success("No Invalid Gender Found ✅")

    else:

        st.dataframe(invalid)

    st.markdown("---")

    st.subheader("Business Rules")

    rules={
        "Age":(0,120),
        "IsActiveMember":(0,1),
        "NumOfProducts":(0,100)
    }

    result=[]

    for col,(low,high) in rules.items():

        invalid=df[~df[col].between(low,high)]

        result.append([col,len(invalid)])

    st.dataframe(
        pd.DataFrame(result,
        columns=["Column","Invalid Values"]),
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("Outlier Boxplots")

    axes = df.select_dtypes(include="number").plot(
        kind="box",
        subplots=True,
        layout=(-1, 3),
        figsize=(15, 8)
    )

    plt.tight_layout()
    st.pyplot(plt.gcf())   # Display the current figure
    plt.close()

# ====================================
# Univariate Analysis
# ====================================

elif eda=="Univariate Analysis":

    st.header("📊 Univariate Analysis")

    chart = st.selectbox(
        "Select Analysis",
        [
            "Geography",
            "Gender",
            "Surname",
            "CreditScore",
            "Age",
            "Tenure",
            "Balance",
            "EstimatedSalary",
            "NumOfProducts",
            "HasCrCard",
            "IsActiveMember",
            "Exited"
        ]
    )

    # -------------------------
    # Geography
    # -------------------------

    if chart=="Geography":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.countplot(data=df,x="Geography",ax=ax)

            ax.bar_label(ax.containers[0])

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(6,6))

            df["Geography"].value_counts().plot(
                kind="pie",
                autopct="%1.1f%%",
                ax=ax
            )

            st.pyplot(fig)

        st.info("""
France has the highest number of customers,
followed by Germany and Spain.
""")

    # -------------------------
    # Gender
    # -------------------------

    elif chart=="Gender":

        fig,ax=plt.subplots(figsize=(6,4))

        sns.countplot(data=df,x="Gender",ax=ax)

        ax.bar_label(ax.containers[0])

        st.pyplot(fig)

        st.write(df["Gender"].value_counts())

    # -------------------------
    # Surname
    # -------------------------

    elif chart=="Surname":

        st.metric("Unique Surnames",df["Surname"].nunique())

        fig,ax=plt.subplots(figsize=(10,5))

        df["Surname"].value_counts().head(10).plot(
            kind="bar",
            ax=ax
        )

        ax.bar_label(ax.containers[0])

        st.pyplot(fig)

    # -------------------------
    # Credit Score
    # -------------------------

    elif chart=="CreditScore":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.histplot(df["CreditScore"],kde=True,ax=ax)

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.boxplot(x=df["CreditScore"],ax=ax)

            st.pyplot(fig)

        st.metric("Median",df["CreditScore"].median())

        st.metric("Skewness",round(df["CreditScore"].skew(),2))

        st.success("""
Distribution : Approximately Symmetric

Outliers : Present but valid.
""")

    # -------------------------
    # Age
    # -------------------------

    elif chart=="Age":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.histplot(df["Age"],kde=True,ax=ax)

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.boxplot(x=df["Age"],ax=ax)

            st.pyplot(fig)

        st.metric("Skewness",round(df["Age"].skew(),2))

        st.success("""
Right Skewed Distribution

Older customers are fewer in number.

Age outliers are valid.
""")

    # -------------------------
    # Tenure
    # -------------------------

    elif chart=="Tenure":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.countplot(data=df,x="Tenure",ax=ax)

            ax.bar_label(ax.containers[0])

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(6,4))

            df["Tenure"].value_counts().sort_index().plot(
                kind="bar",
                ax=ax
            )

            ax.bar_label(ax.containers[0])

            st.pyplot(fig)

        st.info("""
Most customers have tenure between
1 and 9 years.
""")

    # -------------------------
    # Balance
    # -------------------------

    elif chart=="Balance":

        st.metric("Maximum Balance",round(df["Balance"].max(),2))

        st.metric("Minimum Balance",round(df["Balance"].min(),2))

        fig,ax=plt.subplots(figsize=(7,4))

        sns.histplot(df["Balance"],bins=30,ax=ax)

        st.pyplot(fig)

    # -------------------------
    # Estimated Salary
    # -------------------------

    elif chart=="EstimatedSalary":

        fig,ax=plt.subplots(figsize=(7,4))

        sns.histplot(df["EstimatedSalary"],bins=30,ax=ax)

        st.pyplot(fig)

        st.success("Estimated Salary is approximately uniformly distributed.")

    # -------------------------
    # Num Of Products
    # -------------------------

    elif chart=="NumOfProducts":

        fig,ax=plt.subplots(figsize=(6,4))

        df["NumOfProducts"].value_counts().plot(
            kind="bar",
            ax=ax
        )

        ax.bar_label(ax.containers[0])

        st.pyplot(fig)

    # -------------------------
    # Credit Card
    # -------------------------

    elif chart=="HasCrCard":

        fig,ax=plt.subplots(figsize=(6,4))

        df["HasCrCard"].value_counts().plot(
            kind="bar",
            ax=ax
        )

        ax.bar_label(ax.containers[0])

        st.pyplot(fig)

    # -------------------------
    # Active Member
    # -------------------------

    elif chart=="IsActiveMember":

        fig,ax=plt.subplots(figsize=(6,4))

        df["IsActiveMember"].value_counts().plot(
            kind="bar",
            ax=ax
        )

        ax.bar_label(ax.containers[0])

        st.pyplot(fig)

    # -------------------------
    # Exited
    # -------------------------

    elif chart=="Exited":

        fig,ax=plt.subplots(figsize=(6,6))

        df["Exited"].value_counts().plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        st.pyplot(fig)

        st.warning("Target column is imbalanced.")

# ====================================
# Bivariate Analysis
# ====================================

elif eda=="Bivariate Analysis":

    st.header("📈 Bivariate Analysis")

    option = st.selectbox(
        "Select Analysis",
        [
            "Correlation Heatmap",
            "CreditScore vs Age",
            "Age vs Exited",
            "Tenure vs Exited",
            "Balance vs Exited",
            "EstimatedSalary vs Exited",
            "CreditScore vs Gender",
            "Gender vs Exited",
            "Geography vs Exited",
            "HasCrCard vs Exited",
            "IsActiveMember vs Exited",
            "Gender vs Geography",
            "Geography vs HasCrCard"
        ]
    )

    # ---------------------------------
    # Correlation Heatmap
    # ---------------------------------

    if option=="Correlation Heatmap":

        corr=df.corr(numeric_only=True)

        fig,ax=plt.subplots(figsize=(12,8))

        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # CreditScore vs Age
    # ---------------------------------

    elif option=="CreditScore vs Age":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.scatterplot(
                data=df,
                x="CreditScore",
                y="Age",
                ax=ax
            )

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.regplot(
                data=df,
                x="CreditScore",
                y="Age",
                scatter_kws={"alpha":0.4},
                line_kws={"color":"red"},
                ax=ax
            )

            st.pyplot(fig)

        st.metric(
            "Correlation",
            round(df[["CreditScore","Age"]].corr().iloc[0,1],3)
        )

        st.info(
            "There is no significant linear relationship between CreditScore and Age."
        )

    # ---------------------------------
    # Age vs Exited
    # ---------------------------------

    elif option=="Age vs Exited":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.boxplot(
                data=df,
                x="Exited",
                y="Age",
                ax=ax
            )

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.histplot(
                data=df,
                x="Age",
                hue="Exited",
                kde=True,
                bins=30,
                ax=ax
            )

            st.pyplot(fig)

        st.success("""
Customers who exited are generally older than customers who stayed.

Age appears to be an important factor influencing churn.
""")

    # ---------------------------------
    # Tenure vs Exited
    # ---------------------------------

    elif option=="Tenure vs Exited":

        c1,c2=st.columns(2)

        with c1:

            fig,ax=plt.subplots(figsize=(6,4))

            sns.boxplot(
                data=df,
                x="Exited",
                y="Tenure",
                ax=ax
            )

            st.pyplot(fig)

        with c2:

            fig,ax=plt.subplots(figsize=(7,4))

            sns.countplot(
                data=df,
                x="Tenure",
                hue="Exited",
                ax=ax
            )

            st.pyplot(fig)

        st.info(
            "Tenure alone does not strongly differentiate customers who churn."
        )

    # ---------------------------------
    # Balance vs Exited
    # ---------------------------------

    elif option=="Balance vs Exited":

        fig,ax=plt.subplots(figsize=(6,4))

        sns.boxplot(
            data=df,
            x="Exited",
            y="Balance",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # EstimatedSalary vs Exited
    # ---------------------------------

    elif option=="EstimatedSalary vs Exited":

        fig,ax=plt.subplots(figsize=(6,4))

        sns.boxplot(
            data=df,
            x="Exited",
            y="EstimatedSalary",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # CreditScore vs Gender
    # ---------------------------------

    elif option=="CreditScore vs Gender":

        fig,ax=plt.subplots(figsize=(6,4))

        sns.boxplot(
            data=df,
            x="Gender",
            y="CreditScore",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # Gender vs Exited
    # ---------------------------------

    elif option=="Gender vs Exited":

        fig,ax=plt.subplots(figsize=(6,4))

        sns.countplot(
            data=df,
            x="Gender",
            hue="Exited",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # Geography vs Exited
    # ---------------------------------

    elif option=="Geography vs Exited":

        fig,ax=plt.subplots(figsize=(6,4))

        sns.countplot(
            data=df,
            x="Geography",
            hue="Exited",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # HasCrCard vs Exited
    # ---------------------------------

    elif option=="HasCrCard vs Exited":

        ct=pd.crosstab(df["HasCrCard"],df["Exited"])

        fig,ax=plt.subplots(figsize=(6,4))

        ct.plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # IsActiveMember vs Exited
    # ---------------------------------

    elif option=="IsActiveMember vs Exited":

        ct=pd.crosstab(df["IsActiveMember"],df["Exited"])

        fig,ax=plt.subplots(figsize=(6,4))

        sns.heatmap(
            ct,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # Gender vs Geography
    # ---------------------------------

    elif option=="Gender vs Geography":

        fig,ax=plt.subplots(figsize=(6,4))

        pd.crosstab(
            df["Gender"],
            df["Geography"],
            normalize="index"
        ).plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

        st.pyplot(fig)

    # ---------------------------------
    # Geography vs HasCrCard
    # ---------------------------------

    elif option=="Geography vs HasCrCard":

        ct=pd.crosstab(
            df["Geography"],
            df["HasCrCard"]
        )

        fig,ax=plt.subplots(figsize=(6,4))

        sns.heatmap(
            ct,
            annot=True,
            fmt="d",
            cmap="Blues",
            ax=ax
        )

        st.pyplot(fig)

# ====================================
# Multivariate Analysis
# ====================================

elif eda=="Multivariate Analysis":

    st.header("📊 Multivariate Analysis")

    option = st.selectbox(
        "Select Analysis",
        [
            "Gender - Geography - Exited",
            "Gender - NumOfProducts - Exited",
            "Gender - Tenure - Exited",
            "Outlier Detection",
            "EDA Summary"
        ]
    )

    # ---------------------------------
    # Gender Geography Exited
    # ---------------------------------

    if option=="Gender - Geography - Exited":

        fig,ax=plt.subplots(figsize=(10,5))

        plot=df.groupby(
            ["Gender","Geography","Exited"]
        )["Exited"].count().unstack()

        plot.plot(kind="bar",ax=ax)

        ax.bar_label(ax.containers[0])
        ax.bar_label(ax.containers[1])

        st.pyplot(fig)

        st.success("""

• Male customers from Germany exited slightly more.

• Male customers from France stayed the most.

• Female customers from France also stayed in high numbers.

""")

    # ---------------------------------

    elif option=="Gender - NumOfProducts - Exited":

        fig,ax=plt.subplots(figsize=(10,5))

        df.groupby(
            ["Gender","NumOfProducts","Exited"]
        )["Exited"].count().unstack().plot(
            kind="bar",
            ax=ax
        )

        st.pyplot(fig)

        st.info("""

Customers having 1 product are more likely to churn.

Customers with 2 products mostly stayed.

""")

    # ---------------------------------

    elif option=="Gender - Tenure - Exited":

        fig,ax=plt.subplots(figsize=(10,5))

        df.groupby(
            ["Gender","Tenure","Exited"]
        )["Exited"].count().unstack().plot(
            kind="bar",
            ax=ax
        )

        st.pyplot(fig)

        st.info("""

Male and Female customers between
1-9 years tenure are mostly retained.

""")

    # ---------------------------------
    # Outlier Detection
    # ---------------------------------

    elif option=="Outlier Detection":

        st.subheader("IQR Outlier Detection")

        numeric=df.select_dtypes(include="number")

        result=[]

        for col in numeric.columns:

            data=df[col]

            Q1=data.quantile(.25)

            Q3=data.quantile(.75)

            IQR=Q3-Q1

            lower=Q1-1.5*IQR

            upper=Q3+1.5*IQR

            outlier=data[
                (data<lower)|
                (data>upper)
            ]

            result.append(
                [
                    col,
                    len(outlier)
                ]
            )

        out=pd.DataFrame(
            result,
            columns=[
                "Column",
                "Outliers"
            ]
        )

        st.dataframe(
            out,
            use_container_width=True
        )

    # ---------------------------------
    # Final Summary
    # ---------------------------------

    elif option=="EDA Summary":

        st.subheader("Business Insights")

        st.success("""

✔ France has the highest number of customers.

✔ Male customers are slightly more than females.

✔ Credit Score is approximately symmetric.

✔ Age is right skewed.

✔ Customers between 40-50 years are more likely to churn.

✔ Tenure has very little impact on churn.

✔ Most customers own 1 or 2 products.

✔ More than 70% customers have Credit Card.

✔ Dataset is imbalanced.

✔ Age is one of the strongest indicators of churn.

✔ Numerical variables have very weak correlation.

✔ Germany contributes relatively higher churn.

""")

# ====================================
# Download Dataset
# ====================================

st.sidebar.markdown("---")

csv=df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    "📥 Download Cleaned Dataset",
    csv,
    "cleaned_data.csv",
    "text/csv"
)

st.sidebar.markdown("---")

st.sidebar.success("EDA Completed Successfully ✅")
