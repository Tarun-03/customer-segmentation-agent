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
    Returns business-friendly customer segment summaries by combining
    cluster statistics, persona names, customer counts, characteristics,
    and recommended banking products.
    """

    summary = _load_cluster_summary()
    personas = _load_personas()
    customers = _load_clustered_customers()

    merged = summary.merge(personas, on="cluster", how="left")

    persona_profiles = {
        "Priority Customers": {
            "characteristics": [
                "High annual income",
                "Strong account balance",
                "High investment activity",
                "Frequent banking transactions",
                "Active digital banking usage"
            ],
            "recommended_products": [
                "Wealth Management",
                "Premium Savings Account",
                "Investment Advisory",
                "Premium Credit Card"
            ]
        },
        "Regular Customers": {
            "characteristics": [
                "Moderate income",
                "Stable banking activity",
                "Average account balance",
                "Consistent monthly transactions"
            ],
            "recommended_products": [
                "Cashback Credit Card",
                "Personal Loan",
                "Savings Booster Plan",
                "Insurance Products"
            ]
        },
        "Dormant Customers": {
            "characteristics": [
                "Low banking activity",
                "Low transaction frequency",
                "Limited digital engagement",
                "Low investment participation"
            ],
            "recommended_products": [
                "Reactivation Campaign",
                "Welcome Back Rewards",
                "Fee Waiver Offers",
                "Digital Banking Awareness"
            ]
        },
        "Young Professionals": {
            "characteristics": [
                "Growing income",
                "Increasing transaction frequency",
                "High digital banking adoption",
                "Early investment potential"
            ],
            "recommended_products": [
                "Salary Account",
                "Starter Credit Card",
                "SIP Investment Plan",
                "Mobile Banking Benefits"
            ]
        }
    }

    results = []

    for _, row in merged.iterrows():

        cluster = int(row["cluster"])
        persona = row["persona"]

        customer_count = len(
            customers[customers["cluster"] == cluster]
        )

        profile = persona_profiles.get(
            persona,
            {
                "characteristics": [
                    "Customer segment identified through clustering."
                ],
                "recommended_products": [
                    "Personalized Banking Services"
                ]
            }
        )

        results.append({
            "cluster": cluster,
            "persona": persona,
            "customer_count": customer_count,

            "average_income": round(row["average_income"], 2),
            "average_balance": round(row["average_balance"], 2),
            "average_credit_score": round(row["average_credit_score"], 2),
            "average_transactions": round(row["average_transactions"], 2),
            "average_investment": round(row["average_investment"], 2),
            "average_digital_score": round(row["average_digital_score"], 2),

            "characteristics": profile["characteristics"],

            "recommended_products": profile["recommended_products"],

            "business_value": (
                "High"
                if persona == "Priority Customers"
                else "Medium"
                if persona in ["Regular Customers", "Young Professionals"]
                else "Low"
            )
        })

    return {
        "number_of_segments": len(results),
        "segments": results
    }



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
    Customer Strategy Tool

    Identifies customers requiring retention efforts while also recommending
    next-best banking actions such as upgrades, cross-selling, investment
    opportunities, and personalized engagement.
    """

    df = _load_clustered_customers()
    personas = _load_personas()

    if cluster is not None:
        df = df[df["cluster"] == cluster]

    cluster_avgs = df.groupby("cluster")[
        [
            "account_tenure",
            "monthly_transactions",
            "digital_banking_score",
            "annual_income",
            "account_balance",
            "credit_score",
            "investment_amount"
        ]
    ].transform("mean")

    strategies = []

    for _, row in df.iterrows():

        persona = personas.loc[
            personas["cluster"] == row["cluster"],
            "persona"
        ].iloc[0]

        reasons = []
        recommendations = []

        risk_level = "Low"
        upgrade_potential = "Low"

        # ---------------- Retention Rules ---------------- #

        if row["monthly_transactions"] < cluster_avgs.loc[row.name, "monthly_transactions"] * 0.7:
            reasons.append("Monthly transactions are significantly below the cluster average.")
            recommendations.append("Offer cashback or transaction reward campaigns.")
            risk_level = "Medium"

        if row["digital_banking_score"] < cluster_avgs.loc[row.name, "digital_banking_score"]:
            reasons.append("Digital banking engagement is below average.")
            recommendations.append("Promote digital banking features and mobile app benefits.")
            risk_level = "High"

        if row["account_tenure"] < cluster_avgs.loc[row.name, "account_tenure"]:
            reasons.append("Customer relationship is relatively new.")
            recommendations.append("Provide loyalty rewards and onboarding incentives.")

        # ---------------- Upgrade Rules ---------------- #

        if (
            row["annual_income"] > cluster_avgs.loc[row.name, "annual_income"]
            and row["credit_score"] >= 750
            and row["account_balance"] > cluster_avgs.loc[row.name, "account_balance"]
        ):
            upgrade_potential = "High"
            recommendations.extend([
                "Offer Premium Savings Account",
                "Offer Premium Credit Card",
                "Invite to Wealth Management Program"
            ])

        elif (
            row["annual_income"] > cluster_avgs.loc[row.name, "annual_income"]
        ):
            upgrade_potential = "Medium"
            recommendations.append("Recommend Salary Upgrade Banking Package")

        # ---------------- Investment Opportunity ---------------- #

        if (
            row["investment_amount"] <
            cluster_avgs.loc[row.name, "investment_amount"]
            and row["annual_income"] >
            cluster_avgs.loc[row.name, "annual_income"]
        ):
            recommendations.append(
                "Recommend Mutual Funds or Fixed Deposit investment plans."
            )

        # ---------------- Loan Opportunity ---------------- #

        if (
            row["credit_score"] >= 760
            and row["annual_income"] >
            cluster_avgs.loc[row.name, "annual_income"]
        ):
            recommendations.append(
                "Eligible for pre-approved Personal Loan or Home Loan."
            )

        # ---------------- Insurance ---------------- #

        if row["age"] > 45:
            recommendations.append(
                "Recommend retirement and insurance products."
            )

        strategies.append({
            "customer_id": int(row["customer_id"]),
            "cluster": int(row["cluster"]),
            "persona": persona,

            "risk_level": risk_level,

            "upgrade_potential": upgrade_potential,

            "next_best_actions": list(dict.fromkeys(recommendations)),

            "reasons": reasons if reasons else [
                "Customer demonstrates healthy banking behaviour."
            ]
        })

    high_risk = sum(
        1 for customer in strategies
        if customer["risk_level"] == "High"
    )

    return {
        "strategy_type": "Customer Strategy",
        "scope": "all_customers" if cluster is None else f"cluster_{cluster}",
        "customers_analyzed": len(strategies),
        "high_risk_customers": high_risk,
        "customer_strategies": strategies
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