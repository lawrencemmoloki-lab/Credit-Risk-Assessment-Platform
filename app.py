
import streamlit as st

st.set_page_config(
    page_title="Credit Risk Intelligence System",
    page_icon="📊",
    layout="wide",
)

navigation = st.navigation({
    "Credit Risk Intelligence System": [
        st.Page("src/pages/home.py", title="Home", default=True),
        st.Page("src/pages/predict.py", title="Predict Risk"),
        st.Page("src/pages/sql_analytics.py", title="SQL Analytics"),
        st.Page("src/pages/model_insights.py", title="Model Insights"),
    ]
})

navigation.run()
