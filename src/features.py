# Single definition of the model's inputs, shared by training, the
# prediction form and the insights page, so they can never drift apart.

NUMERIC_FEATURES = ["duration", "credit_amount", "installment_rate"]

CATEGORICAL_OPTIONS = {
    "checking_status": ["< 0 DM", "0 to 200 DM", ">= 200 DM", "no checking account"],
    "credit_history": ["no credits taken", "all credits paid back",
                       "credits paid back duly", "past delays", "critical account"],
    "savings_status": ["< 100 DM", "100 to 500 DM", "500 to 1000 DM",
                       ">= 1000 DM", "unknown / no savings"],
    "employment": ["unemployed", "< 1 year", "1 to 4 years", "4 to 7 years", ">= 7 years"],
}

FEATURE_LABELS = {
    "duration": "Loan duration (months)",
    "credit_amount": "Credit amount",
    "installment_rate": "Installment rate (1 = low, 4 = high)",
    "checking_status": "Checking account status",
    "credit_history": "Credit history",
    "savings_status": "Savings",
    "employment": "Employment tenure",
}

FEATURES = NUMERIC_FEATURES + list(CATEGORICAL_OPTIONS)