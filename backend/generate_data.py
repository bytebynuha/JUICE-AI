import csv
import random
from pathlib import Path
from datetime import datetime, timedelta


random.seed(42)

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_data():
    razorpay = []
    bank = []
    ledger = []

    start_date = datetime(2026, 8, 1)

    for i in range(1, 101):
        transaction_id = f"TXN{i:04d}"
        amount = random.choice([
            499,
            799,
            999,
            1499,
            1999,
            2499,
            4999,
            9999
        ])

        transaction_date = (
            start_date + timedelta(days=random.randint(0, 20))
        ).strftime("%Y-%m-%d")

        razorpay.append({
            "transaction_id": transaction_id,
            "reference": transaction_id,
            "amount": amount,
            "date": transaction_date,
            "status": "SUCCESS",
        })

        ledger.append({
            "transaction_id": transaction_id,
            "reference": transaction_id,
            "amount": amount,
            "date": transaction_date,
            "status": "RECORDED",
        })

        bank_amount = amount

        # Create realistic exceptions
        if i % 20 == 0:
            bank_amount = amount - 100

        # Missing bank transactions
        if i % 25 == 0:
            continue

        # Reference mismatch
        bank_reference = transaction_id

        if i % 15 == 0:
            bank_reference = f"PAY-{i:04d}"

        bank.append({
            "transaction_id": transaction_id,
            "reference": bank_reference,
            "amount": bank_amount,
            "date": transaction_date,
            "status": "SETTLED",
        })

    # Add a duplicate bank transaction
    bank.append({
        "transaction_id": "TXN0030",
        "reference": "TXN0030-DUP",
        "amount": 999,
        "date": "2026-08-10",
        "status": "SETTLED",
    })

    write_csv(
        DATA_DIR / "razorpay.csv",
        razorpay
    )

    write_csv(
        DATA_DIR / "bank.csv",
        bank
    )

    write_csv(
        DATA_DIR / "ledger.csv",
        ledger
    )

    print("JUICE synthetic data generated successfully.")
    print(f"Location: {DATA_DIR}")


def write_csv(path, rows):
    if not rows:
        return

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    generate_data()