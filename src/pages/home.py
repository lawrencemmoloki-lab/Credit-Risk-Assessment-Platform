import pandas as pd
import streamlit as st

from src.connect_db import engine

st.title("Credit Risk Intelligence System")
st.caption("Loan-level data served live from PostgreSQL (Supabase).")


@st.cache_data(ttl=600, show_spinner="Loading loans from PostgreSQL...")
def fetch_loans():
    return pd.read_sql("SELECT * FROM loans", engine)


try:
    df = fetch_loans()
except Exception:
    st.error("Could not load data from the database. Please try again shortly.")
    st.stop()

st.markdown("## Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Loans", f"{len(df):,}")
col2.metric("Default Rate", f"{df['default_status'].mean() * 100:.1f}%")
col3.metric("Avg Credit Amount", f"{df['credit_amount'].mean():,.0f}")

st.markdown("### Risk Distribution")
risk_counts = df["default_status"].value_counts().rename(
    index={0: "Repaid", 1: "Defaulted"})
st.bar_chart(risk_counts)