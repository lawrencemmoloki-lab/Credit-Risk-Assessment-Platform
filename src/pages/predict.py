from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from src.features import CATEGORICAL_OPTIONS, FEATURE_LABELS, FEATURES

ROOT_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = ROOT_DIR / "src" / "model.joblib"

st.title("Credit Risk Prediction")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error(f"Model file not found at {MODEL_PATH}. "
             "Run `python -m src.train_model` and commit src/model.joblib.")
    st.stop()

st.markdown("Enter an applicant's details to estimate the probability of "
            "default. The form uses exactly the features the model was trained on.")

applicant = {
    "duration": st.slider(FEATURE_LABELS["duration"], 4, 72, 12),
    "credit_amount": st.number_input(FEATURE_LABELS["credit_amount"],
                                     250, 20_000, 5_000, step=250),
    "installment_rate": st.slider(FEATURE_LABELS["installment_rate"], 1, 4, 2),
}
for feature, options in CATEGORICAL_OPTIONS.items():
    applicant[feature] = st.selectbox(FEATURE_LABELS[feature], options)

if st.button("Predict risk", type="primary"):
    X = pd.DataFrame([applicant])[FEATURES]
    probability = float(model.predict_proba(X)[0, 1])

    if probability < 0.3:
        st.success(f"🟢 LOW RISK — default probability {probability * 100:.1f}%")
    elif probability < 0.7:
        st.warning(f"🟠 MEDIUM RISK — default probability {probability * 100:.1f}%")
    else:
        st.error(f"🔴 HIGH RISK — default probability {probability * 100:.1f}%")
    st.progress(int(probability * 100))
    st.caption("Risk bands (low < 30%, medium 30–70%, high > 70%) are "
               "illustrative policy thresholds, not part of the model.")