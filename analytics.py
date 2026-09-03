def safe_float(value, default=0.0) -> float:
    try:
        return float(value) if value not in (None, "", "null") else default
    except (TypeError, ValueError):
        return default

def extract_amount(item):
    return (
        safe_float(item.get("amount")) or
        0.0
    )

def categorize_expense(item):
    category = item.get("category") or item.get("description", "").lower()

    if not category or not isinstance(category, str):
        return "Uncategorized"

    category = category.lower()

    if any(word in category for word in ["food", "restaurant", "zomato", "swiggy", "cafe"]):
        return "Food & Dining"
    if any(word in category for word in ["fuel", "petrol", "uber", "ola", "transport"]):
        return "Transport"
    if any(word in category for word in ["rent", "electricity", "internet", "water"]):
        return "Bills & Utilities"
    if any(word in category for word in ["shopping", "flipkart", "amazon", "myntra"]):
        return "Shopping"
    if any(word in category for word in ["movie", "netflix", "spotify"]):
        return "Entertainment"
    if any(word in category for word in ["health", "doctor", "medicine"]):
        return "Healthcare"

    return "Other"

def analyze_finances(income, expenses):

    income_amounts = [extract_amount(i) for i in income]
    expense_amounts = [extract_amount(e) for e in expenses]

    total_income = sum(income_amounts)
    total_expenses = sum(expense_amounts)
    savings = total_income - total_expenses
    savings_rate = (savings / total_income * 100) if total_income > 0 else 0

    expenses_with_amount = [
        {"description": e.get("description") or "No description", "amount": extract_amount(e)}
        for e in expenses
    ]
    expenses_with_amount.sort(key=lambda x: x["amount"], reverse=True)
    top_expenses = expenses_with_amount[:5]

    category_totals = {}
    for e in expenses:
        cat = categorize_expense(e)
        category_totals[cat] = category_totals.get(cat, 0) + extract_amount(e)

    category_breakdown = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    insights = []
    if total_expenses > total_income:
        insights.append("Warning: You are spending more than you earn!")
    elif savings_rate < 20:
        insights.append("Try saving at least 20% of your income.")
    else:
        insights.append("Good job! You are saving well.")

    if any(cat[0] == "Food & Dining" and cat[1] > total_expenses * 0.3 for cat in category_breakdown):
        insights.append("Food expenses are high. Consider cooking at home more often.")

    if not income:
        insights.append("No income recorded yet.")
    if not expenses:
        insights.append("No expenses recorded yet.")

    return {
        "summary": {
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "net_savings": round(savings, 2),
            "savings_rate_percent": round(savings_rate, 1)
        },
        "top_expenses": top_expenses,
        "category_breakdown": [
            {"category": cat, "amount": round(amount, 2)}
            for cat, amount in category_breakdown
        ],
        "insights": insights
    }
