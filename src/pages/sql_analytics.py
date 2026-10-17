import pandas as pd
import streamlit as st

from src.connect_db import engine

st.title("SQL Analytics Dashboard")
st.markdown("Business insights queried live from PostgreSQL.")

QUERIES = [
    ("Default risk by checking account status",
     """SELECT checking_status, AVG(default_status) AS default_rate
        FROM loans GROUP BY checking_status ORDER BY default_rate DESC""",
     "checking_status"),
    ("Default risk by housing type",
     """SELECT c.housing, AVG(l.default_status) AS default_rate
        FROM customers c JOIN loans l ON c.customer_id = l.customer_id
        GROUP BY c.housing ORDER BY default_rate DESC""",
     "housing"),
    ("Average loan amount by employment tenure",
     """SELECT employment, AVG(credit_amount) AS avg_credit_amount
        FROM loans GROUP BY employment ORDER BY avg_credit_amount DESC""",
     "employment"),
    ("Highest-risk loan purposes",
     """SELECT purpose, AVG(default_status) AS risk_rate
        FROM loans GROUP BY purpose ORDER BY risk_rate DESC""",
     "purpose"),
]

for title, query, x_column in QUERIES:
    st.subheader(title)
    try:
        result = pd.read_sql(query, engine)
        st.dataframe(result, use_container_width=True, hide_index=True)
        st.bar_chart(result, x=x_column, y=result.columns[1])
    except Exception as e:
        st.error(f"Query failed: {e}")