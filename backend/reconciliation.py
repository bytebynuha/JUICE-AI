import pandas as pd


def normalize_reference(reference):
    if pd.isna(reference):
        return ""

    return str(reference).strip().upper()


def reconcile(
    razorpay_file,
    bank_file,
    ledger_file
):
    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    razorpay = pd.read_csv(razorpay_file)
    bank = pd.read_csv(bank_file)
    ledger = pd.read_csv(ledger_file)

    # -----------------------------------------------------
    # NORMALIZE REFERENCE FIELDS
    # -----------------------------------------------------

    for dataframe in [razorpay, bank, ledger]:
        dataframe["normalized_reference"] = (
            dataframe["reference"]
            .apply(normalize_reference)
        )

    # -----------------------------------------------------
    # DETECT DUPLICATE BANK TRANSACTIONS
    # -----------------------------------------------------

    duplicate_ids = (
        bank[
            bank.duplicated(
                subset=["transaction_id"],
                keep=False
            )
        ]["transaction_id"]
        .unique()
        .tolist()
    )

    exceptions = []
    matched = 0

    # -----------------------------------------------------
    # PROCESS EACH RAZORPAY TRANSACTION
    # -----------------------------------------------------

    for _, payment in razorpay.iterrows():

        transaction_id = payment["transaction_id"]
        payment_amount = float(payment["amount"])

        # Find transaction in bank
        bank_matches = bank[
            bank["transaction_id"] == transaction_id
        ]

        # Find transaction in ledger
        ledger_matches = ledger[
            ledger["transaction_id"] == transaction_id
        ]

        # -------------------------------------------------
        # MISSING FROM BANK
        # -------------------------------------------------

        if bank_matches.empty:

            exceptions.append({
                "transaction_id": transaction_id,
                "type": "MISSING_FROM_BANK",
                "severity": "HIGH",
                "financial_impact": payment_amount,

                "confidence": 99,

                "reason": (
                    "Transaction exists in Razorpay "
                    "but not in bank."
                ),

                "evidence": {
                    "razorpay_amount": payment_amount,
                    "bank_record_found": False,
                    "ledger_record_found": (
                        not ledger_matches.empty
                    ),
                },

                "recommendation": (
                    "Verify whether the payment has been "
                    "settled or is still pending."
                ),
            })

            continue

        # Bank record exists
        bank_record = bank_matches.iloc[0]
        bank_amount = float(bank_record["amount"])

        # -------------------------------------------------
        # MISSING FROM LEDGER
        # -------------------------------------------------

        if ledger_matches.empty:

            exceptions.append({
                "transaction_id": transaction_id,
                "type": "MISSING_FROM_LEDGER",
                "severity": "HIGH",
                "financial_impact": payment_amount,

                "confidence": 99,

                "reason": (
                    "Transaction exists in Razorpay "
                    "and bank but not in ledger."
                ),

                "evidence": {
                    "razorpay_amount": payment_amount,
                    "bank_amount": bank_amount,
                    "ledger_record_found": False,
                },

                "recommendation": (
                    "Verify the merchant ledger and "
                    "determine whether the transaction "
                    "needs to be recorded."
                ),
            })

            continue

        # Ledger record exists
        ledger_record = ledger_matches.iloc[0]
        ledger_amount = float(ledger_record["amount"])

        # -------------------------------------------------
        # AMOUNT MISMATCH
        # -------------------------------------------------

        if (
            payment_amount != bank_amount
            or payment_amount != ledger_amount
        ):

            difference = payment_amount - bank_amount

            exceptions.append({
                "transaction_id": transaction_id,
                "type": "AMOUNT_MISMATCH",
                "severity": "MEDIUM",
                "financial_impact": abs(difference),

                "confidence": 85,

                "reason": (
                    f"Razorpay amount is "
                    f"₹{payment_amount:.2f}, "
                    f"while bank amount is "
                    f"₹{bank_amount:.2f}."
                ),

                "evidence": {
                    "razorpay_amount": payment_amount,
                    "bank_amount": bank_amount,
                    "ledger_amount": ledger_amount,

                    "razorpay_reference": str(
                        payment["reference"]
                    ),

                    "bank_reference": str(
                        bank_record["reference"]
                    ),

                    "ledger_reference": str(
                        ledger_record["reference"]
                    ),
                },

                "recommendation": (
                    "Review the settlement or fee "
                    "breakdown before modifying "
                    "accounting records."
                ),
            })

            continue

        # -------------------------------------------------
        # REFERENCE MISMATCH
        # -------------------------------------------------

        razorpay_reference = normalize_reference(
            payment["reference"]
        )

        bank_reference = normalize_reference(
            bank_record["reference"]
        )

        if razorpay_reference != bank_reference:

            exceptions.append({
                "transaction_id": transaction_id,
                "type": "REFERENCE_MISMATCH",
                "severity": "LOW",
                "financial_impact": 0,

                "confidence": 97,

                "reason": (
                    "Transaction amounts match but "
                    "references are different."
                ),

                "evidence": {
                    "razorpay_reference": (
                        razorpay_reference
                    ),
                    "bank_reference": (
                        bank_reference
                    ),
                    "amounts_match": True,
                },

                "recommendation": (
                    "Verify whether both references "
                    "represent the same financial "
                    "transaction."
                ),
            })

            continue

        # -------------------------------------------------
        # SUCCESSFULLY MATCHED
        # -------------------------------------------------

        matched += 1

    # -----------------------------------------------------
    # DUPLICATE TRANSACTIONS
    # -----------------------------------------------------

    for transaction_id in duplicate_ids:

        duplicate_records = bank[
            bank["transaction_id"] == transaction_id
        ]

        duplicate_amount = float(
            duplicate_records.iloc[0]["amount"]
        )

        exceptions.append({
            "transaction_id": transaction_id,
            "type": "DUPLICATE_TRANSACTION",
            "severity": "HIGH",
            "financial_impact": duplicate_amount,

            "confidence": 99,

            "reason": (
                "Multiple bank records use the "
                "same transaction ID."
            ),

            "evidence": {
                "duplicate_count": len(
                    duplicate_records
                ),
                "bank_amount": duplicate_amount,
            },

            "recommendation": (
                "Review the duplicate bank records "
                "and determine which transaction "
                "is valid."
            ),
        })

    # -----------------------------------------------------
    # SUMMARY METRICS
    # -----------------------------------------------------

    total_transactions = len(razorpay)

    total_exposure = sum(
        exception["financial_impact"]
        for exception in exceptions
    )

    match_rate = (
        matched / total_transactions * 100
        if total_transactions
        else 0
    )

    # -----------------------------------------------------
    # RETURN RESULTS
    # -----------------------------------------------------

    return {
        "total_transactions": total_transactions,

        "matched": matched,

        "exceptions": len(exceptions),

        "match_rate": round(
            match_rate,
            2
        ),

        "financial_exposure": round(
            total_exposure,
            2
        ),

        "exception_details": exceptions,
    }