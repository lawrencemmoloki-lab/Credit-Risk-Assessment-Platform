# Trains the default-risk model directly from PostgreSQL and stores it with
# its test metrics. Run from the repository root:  python -m src.train_model
import json
from datetime import datetime, timezone

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from src.connect_db import engine
from src.features import CATEGORICAL_OPTIONS, FEATURES


def train():
    df = pd.read_sql(f"SELECT {', '.join(FEATURES)}, default_status FROM loans", engine)

    X, y = df[FEATURES], df["default_status"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("preprocess", ColumnTransformer(
            [("categorical", OneHotEncoder(handle_unknown="ignore"),
              list(CATEGORICAL_OPTIONS))],
            remainder="passthrough",
        )),
        ("classifier", RandomForestClassifier(n_estimators=300, random_state=42)),
    ])
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)
    print(classification_report(y_test, model.predict(X_test)))
    print(f"AUC:  {auc:.3f}")
    print(f"Gini: {2 * auc - 1:.3f}")

    joblib.dump(model, "src/model.joblib")
    with open("src/metrics.json", "w") as f:
        json.dump({
            "auc": round(auc, 3),
            "gini": round(2 * auc - 1, 3),
            "test_rows": len(y_test),
            "default_rate": round(float(y_test.mean()), 3),
            "features": FEATURES,
            "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }, f, indent=2)
    print("Saved src/model.joblib and src/metrics.json")
    return model


if __name__ == "__main__":
    train()