from reconciliation import reconcile


result = reconcile(
    "../data/raw/razorpay.csv",
    "../data/raw/bank.csv",
    "../data/raw/ledger.csv",
)


print("\n========== JUICE RECONCILIATION ==========")

print(
    f"Total transactions: "
    f"{result['total_transactions']}"
)

print(
    f"Matched: "
    f"{result['matched']}"
)

print(
    f"Exceptions: "
    f"{result['exceptions']}"
)

print(
    f"Match rate: "
    f"{result['match_rate']}%"
)

print(
    f"Financial exposure: "
    f"₹{result['financial_exposure']:,.2f}"
)

print("\n========== EXCEPTIONS ==========")

for exception in result["exception_details"]:
    print(
        f"{exception['transaction_id']} | "
        f"{exception['type']} | "
        f"{exception['severity']} | "
        f"₹{exception['financial_impact']:,.2f}"
    )