# ETL: raw UCI german.data -> decoded, readable tables in PostgreSQL.
# Run from the repository root:  python -m src.load_data
import pandas as pd

from src.connect_db import engine

COLUMNS = [
    "checking_status", "duration", "credit_history", "purpose", "credit_amount",
    "savings_status", "employment", "installment_rate", "personal_status",
    "other_debtors", "residence_since", "property", "age",
    "other_installment_plans", "housing", "existing_credits", "job",
    "num_dependents", "own_telephone", "foreign_worker", "default_status",
]

# Human-readable labels for the UCI codes (raw file uses A11, A12, ...).
DECODE = {
    "checking_status": {"A11": "< 0 DM", "A12": "0 to 200 DM", "A13": ">= 200 DM",
                        "A14": "no checking account"},
    "credit_history": {"A30": "no credits taken", "A31": "all credits paid back",
                       "A32": "credits paid back duly", "A33": "past delays",
                       "A34": "critical account"},
    "purpose": {"A40": "new car", "A41": "used car", "A42": "furniture",
                "A43": "radio/television", "A44": "domestic appliances",
                "A45": "repairs", "A46": "education", "A47": "vacation",
                "A48": "retraining", "A49": "business", "A410": "other"},
    "savings_status": {"A61": "< 100 DM", "A62": "100 to 500 DM",
                       "A63": "500 to 1000 DM", "A64": ">= 1000 DM",
                       "A65": "unknown / no savings"},
    "employment": {"A71": "unemployed", "A72": "< 1 year", "A73": "1 to 4 years",
                   "A74": "4 to 7 years", "A75": ">= 7 years"},
    "housing": {"A151": "rent", "A152": "own", "A153": "provided free"},
    "job": {"A171": "unemployed / non-resident", "A172": "unskilled resident",
            "A173": "skilled employee", "A174": "management / self-employed"},
}

LOAN_COLUMNS = [
    "checking_status", "duration", "credit_history", "purpose",
    "credit_amount", "savings_status", "employment", "installment_rate",
    "default_status",
]


def run_etl():
    df = pd.read_csv("data/german.data", sep=" ", header=None, names=COLUMNS)

    # UCI encodes the target as 1 = good, 2 = bad; we store 0 = repaid, 1 = defaulted.
    df["default_status"] = df["default_status"].map({1: 0, 2: 1})

    for column, mapping in DECODE.items():
        df[column] = df[column].map(mapping)

    # Customers: applicant attributes. Protected attributes (personal_status,
    # foreign_worker) are deliberately not stored or modelled.
    customers_df = df[["age", "housing", "job"]].copy()
    customers_df.insert(0, "customer_id", range(1, len(df) + 1))

    loans_df = df[LOAN_COLUMNS].copy()
    loans_df.insert(0, "customer_id", customers_df["customer_id"].values)

    print("Uploading customers...")
    customers_df.to_sql("customers", engine, if_exists="replace", index=False)
    print("Uploading loans...")
    loans_df.to_sql("loans", engine, if_exists="replace", index=False)
    print(f"Uploaded {len(customers_df)} customers and {len(loans_df)} loans.")


if __name__ == "__main__":
    run_etl()