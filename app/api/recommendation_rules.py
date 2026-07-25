def get_personalized_recommendations(customer):

    recommendations = []
    warnings = []

    # Student
    if customer["job"] == "student":
        recommendations.extend([
            "Student Savings Account",
            "Zero Balance Account",
            "Education Loan",
            "Build Credit History"
        ])

    # Low credit score
    if customer["credit_score"] < 650:
        recommendations.extend([
            "Secured Credit Card",
            "Credit Score Improvement Program"
        ])

        warnings.append(
            "Premium credit card approval may be difficult until your credit score improves."
        )

    # Excellent credit score
    elif customer["credit_score"] >= 800:
        recommendations.extend([
            "Platinum Credit Card",
            "Instant Personal Loan"
        ])

    # High income
    if customer["annual_income"] >= 150000:
        recommendations.extend([
            "Wealth Management",
            "Tax Saving Investments",
            "Relationship Manager"
        ])

    # Low balance
    if customer["account_balance"] < 10000:
        recommendations.extend([
            "Emergency Savings Plan",
            "Budget Tracking"
        ])

    # Digital customer
    if customer["digital_banking_score"] >= 80:
        recommendations.extend([
            "UPI Cashback Rewards",
            "Mobile Banking Premium"
        ])

    # Traditional customer
    elif customer["digital_banking_score"] < 40:
        recommendations.extend([
            "Branch Banking Assistance",
            "SMS Banking Alerts"
        ])

    # Long-term customer
    if customer["account_tenure"] >= 10:
        recommendations.append(
            "Loyal Customer Benefits"
        )

    # Cross-selling opportunity
    if customer["number_of_products"] <= 1:
        recommendations.extend([
            "Credit Card",
            "Insurance",
            "Fixed Deposit"
        ])

    recommendations = list(dict.fromkeys(recommendations))

    return {
        "personalized_recommendations": recommendations,
        "warnings": warnings
    }