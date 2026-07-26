import pandas as pd
from functools import lru_cache
from typing import Optional

DATA_DIR = "data/processed"

# ---------- Data loaders (cached so we don't re-read CSVs on every call) ----------

@lru_cache()
def _load_clustered_customers():
    return pd.read_csv(f"{DATA_DIR}/clustered_customers.csv")


@lru_cache()
def _load_cluster_summary():
    return pd.read_csv(f"{DATA_DIR}/cluster_summary.csv")


@lru_cache()
def _load_personas():
    return pd.read_csv(f"{DATA_DIR}/customer_personas.csv")


@lru_cache()
def _load_recommendations():
    return pd.read_csv(f"{DATA_DIR}/customer_recommendations.csv")


# ---------- EDA Tool ----------

def eda_tool(cluster: Optional[int] = None):
    """
    Performs exploratory data analysis.
    If cluster is provided, scopes the EDA to that cluster only.
    """
    df = _load_clustered_customers()

    if cluster is not None:
        df = df[df["cluster"] == cluster]

    numeric_cols = [
        "age", "annual_income", "credit_score", "account_balance",
        "digital_banking_score", "monthly_transactions", "investment_amount",
        "avg_transaction_amount", "account_tenure", "number_of_products"
    ]

    return {
        "scope": "all_customers" if cluster is None else f"cluster_{cluster}",
        "row_count": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "summary_stats": df[numeric_cols].describe().round(2).to_dict(),
        "correlations": df[numeric_cols].corr().round(2).to_dict()
    }


# ---------- Segmentation Tool ----------

def segmentation_tool():
    """
    Returns each cluster merged with its persona name and summary stats.
    """
    summary = _load_cluster_summary()
    personas = _load_personas()

    merged = summary.merge(personas, on="cluster", how="left")

    return merged.to_dict(orient="records")


def get_customer_segment(customer_id: int):
    """
    Looks up a single customer's cluster and persona.
    """
    df = _load_clustered_customers()
    personas = _load_personas()

    row = df[df["customer_id"] == customer_id]

    if row.empty:
        return {"error": f"Customer {customer_id} not found"}

    cluster = int(row.iloc[0]["cluster"])
    persona_row = personas[personas["cluster"] == cluster]
    persona = persona_row.iloc[0]["persona"] if not persona_row.empty else "Unknown"

    return {
        "customer_id": customer_id,
        "cluster": cluster,
        "persona": persona,
        "profile": row.iloc[0].to_dict()
    }


# ---------- Explainability Tool ----------

def explainability_tool(customer_id: int):
    """
    Explains why a customer belongs to their assigned cluster by comparing
    their key features against the cluster average.
    """
    df = _load_clustered_customers()
    summary = _load_cluster_summary()
    personas = _load_personas()

    row = df[df["customer_id"] == customer_id]

    if row.empty:
        return {"error": f"Customer {customer_id} not found"}

    customer = row.iloc[0]
    cluster = int(customer["cluster"])
    cluster_avg = summary[summary["cluster"] == cluster].iloc[0]
    persona_row = personas[personas["cluster"] == cluster]
    persona = persona_row.iloc[0]["persona"] if not persona_row.empty else "Unknown"

    comparisons = {
        "income": (customer["annual_income"], cluster_avg["average_income"]),
        "balance": (customer["account_balance"], cluster_avg["average_balance"]),
        "credit_score": (customer["credit_score"], cluster_avg["average_credit_score"]),
        "transactions": (customer["monthly_transactions"], cluster_avg["average_transactions"]),
        "investment": (customer["investment_amount"], cluster_avg["average_investment"]),
        "digital_score": (customer["digital_banking_score"], cluster_avg["average_digital_score"])
    }

    explanation = []
    for feature, (customer_val, cluster_val) in comparisons.items():
        direction = "above" if customer_val >= cluster_val else "below"
        explanation.append(
            f"{feature.replace('_', ' ')} is {direction} the cluster average "
            f"({customer_val:.2f} vs {cluster_val:.2f})"
        )

    return {
        "customer_id": customer_id,
        "cluster": cluster,
        "persona": persona,
        "explanation": explanation
    }


# ---------- Retention Tool ----------

def retention_tool(cluster: Optional[int] = None):
    """
    Flags customers at risk of disengagement based on low tenure,
    low transaction frequency, and low digital engagement relative
    to their own cluster's average.
    """
    df = _load_clustered_customers()
    personas = _load_personas()

    if cluster is not None:
        df = df[df["cluster"] == cluster]

    cluster_avgs = df.groupby("cluster")[
        ["account_tenure", "monthly_transactions", "digital_banking_score"]
    ].transform("mean")

    at_risk_mask = (
        (df["account_tenure"] < cluster_avgs["account_tenure"]) &
        (df["monthly_transactions"] < cluster_avgs["monthly_transactions"] * 0.7) &
        (df["digital_banking_score"] < cluster_avgs["digital_banking_score"])
    )

    at_risk = df[at_risk_mask].merge(personas, on="cluster", how="left")

    results = []
    for _, row in at_risk.iterrows():
        results.append({
            "customer_id": int(row["customer_id"]),
            "cluster": int(row["cluster"]),
            "persona": row["persona"],
            "account_tenure": row["account_tenure"],
            "monthly_transactions": row["monthly_transactions"],
            "digital_banking_score": row["digital_banking_score"],
            "recommended_action": (
                "Re-engagement outreach: highlight digital banking features "
                "and offer a loyalty incentive tied to transaction frequency"
            )
        })

    return {
        "at_risk_count": len(results),
        "at_risk_customers": results
    }

def feature_engineering_tool():
    """
    Explains the feature engineering pipeline used before K-Means clustering.
    """

    return {
        "title": "Feature Engineering Pipeline",

        "input_features": [
            "Age",
            "Annual Income",
            "Credit Score",
            "Account Balance",
            "Digital Banking Score",
            "Monthly Transactions",
            "Investment Amount",
            "Average Transaction Amount",
            "Account Tenure",
            "Number of Products"
        ],

        "transformations": [
            "Handled missing values",
            "Selected numerical banking features",
            "Scaled numerical features using StandardScaler",
            "Prepared feature matrix for K-Means clustering"
        ],

        "model_input": "Standardized numerical feature matrix",

        "output": "Cluster labels representing customer personas",

        "purpose":
            "Prepared customer banking attributes for K-Means clustering "
            "by cleaning, selecting and scaling the most relevant financial features."
    }