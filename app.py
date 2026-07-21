import streamlit as st

st.title("👨‍💻 Meet the Developer")

col1, col2 = st.columns([1,2])

with col1:
    st.image("profile.jpg", width=220)

with col2:

    st.markdown("## Hi, I'm Abhinay👋")

    st.markdown("""
### 🚀 Aspiring Data Scientist

I'm an enthusiastic Computer Science student with a strong passion for
**Data Science, Machine Learning, Artificial Intelligence, and Data Analytics**.

I enjoy transforming raw data into meaningful insights and building
interactive dashboards, predictive models, and intelligent applications
using Python.

### 💡 My Interests
- 📊 Data Analysis & Visualization
- 🤖 Machine Learning
- 🧠 Artificial Intelligence
- 🐍 Python Development
- 📈 Business Intelligence

### 🛠️ Tech Stack
`Python` • `Pandas` • `NumPy` • `Matplotlib`
`Seaborn` • `Scikit-Learn` • `Streamlit`
`SQL` • `Power BI`

> *"Turning Data into Decisions and Ideas into Reality."* ✨
""")

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Projects", "1")
c2.metric("Skills", "Data Science")
c3.metric("Focus", "Machine Learning")
c4.metric("Status", "Aspiring DS")


st.success("Thank you for visiting my Customer Churn Analysis Dashboard! ❤️")




