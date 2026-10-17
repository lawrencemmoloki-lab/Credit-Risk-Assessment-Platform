import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).parent.parent.parent
MODEL_PATH = ROOT_DIR / "src" / "model.joblib"
METRICS_PATH = ROOT_DIR / "src" / "metrics.json"

st.title("Model Insights")

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    st.error(f"Model file not found at {MODEL_PATH}.")
    st.stop()

classifier = model.named_steps["classifier"]
preprocessor = model.named_steps["preprocess"]

feature_names = [name.split("__", 1)[-1]
                 for name in preprocessor.get_feature_names_out()]
importance = pd.DataFrame(
    {"Feature": feature_names, "Importance": classifier.feature_importances_}
).sort_values("Importance", ascending=False)

st.markdown("### Feature Importance")
st.bar_chart(importance.set_index("Feature"))

if METRICS_PATH.exists():
    metrics = json.loads(METRICS_PATH.read_text())
    col1, col2, col3 = st.columns(3)
    col1.metric("Test AUC", f"{metrics['auc']:.3f}")
    col2.metric("Test Gini", f"{metrics['gini']:.3f}")
    col3.metric("Test rows", metrics["test_rows"])
    st.caption(f"Trained {metrics['trained_at']} on: {', '.join(metrics['features'])}")

st.markdown("### Model")
st.write("scikit-learn `Pipeline`: OneHotEncoder on categorical features, "
         "then RandomForestClassifier (300 trees).")