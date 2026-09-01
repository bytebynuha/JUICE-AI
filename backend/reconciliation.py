import pandas as pd
import time
from collections import Counter


# ============================================================
# NORMALIZE REFERENCE
# ============================================================

def normalize_reference(reference):
    """
    Convert a transaction reference into a consistent format.

    Example:

        " abc-123 "
        "ABC-123"

    both become:

        "ABC-123"
    """

    if pd.isna(reference):
        return ""

    return str(reference).strip().upper()


# ============================================================
# SAFE AMOUNT CONVERSION
# ============================================================

def safe_amount(value):
    """
    Convert an amount into a float safely.

    Handles:
    - integers
    - floats
    - strings
    - missing values
    - commas
    - currency symbols
    """

    if pd.isna(value):
        return 0.0

    if isinstance(value, str):
        value = (
            value
            .replace(",", "")
            .replace("₹", "")
            .replace("$", "")
            .strip()
        )

    try:
        return float(value)

    except (ValueError, TypeError):
        return 0.0


# ============================================================
# VALIDATE DATA
# ============================================================

def validate_columns(dataframe, filename):

    required_columns = [
        "transaction_id",
        "reference",
        "amount",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{filename} is missing required columns: "
            f"{', '.join(missing_columns)}"
        )


# ============================================================
# BUILD EXCEPTION SUMMARY
# ============================================================

def build_exception_summary(exceptions):
    """
    Create a breakdown of reconciliation exceptions.

    This information is useful for:
    - dashboard metrics
    - AI explanations
    - PDF reports
    - Buildathon evaluation
    """

    type_counter = Counter()
    severity_counter = Counter()

    exposure_by_type = Counter()
    exposure_by_severity = Counter()

    for exception in exceptions:

        exception_type = exception.get(
            "type",
            "UNKNOWN"
        )

        severity = exception.get(
            "severity",
            "UNKNOWN"
        )

        financial_impact = safe_amount(
            exception.get(
                "financial_impact",
                0
            )
        )

        type_counter[
            exception_type
        ] += 1

        severity_counter[
            severity
        ] += 1

        exposure_by_type[
            exception_type
        ] += financial_impact

        exposure_by_severity[
            severity
        ] += financial_impact

    return {

        "by_type":
            dict(type_counter),

        "by_severity":
            dict(severity_counter),

        "exposure_by_type":
            {
                key: round(value, 2)
                for key, value
                in exposure_by_type.items()
            },

        "exposure_by_severity":
            {
                key: round(value, 2)
                for key, value
                in exposure_by_severity.items()
            },
    }


# ============================================================
# BUILD AI CONTROLLER EVIDENCE
# ============================================================

def build_ai_controller_evidence(
    total_transactions,
    matched,
    exceptions,
    exception_summary,
    financial_exposure,
    processing_time
):
    """
    Convert raw reconciliation results into structured
    evidence that an AI controller can explain.

    IMPORTANT:
    This function does NOT invent conclusions.

    It only summarizes facts produced by the
    reconciliation engine.
    """

    match_rate = (
        matched
        /
        total_transactions
        *
        100

        if total_transactions
        else 0
    )

    exception_count = len(
        exceptions
    )

    exceptions_by_type = (
        exception_summary["by_type"]
    )

    exceptions_by_severity = (
        exception_summary["by_severity"]
    )

    # --------------------------------------------------------
    # Identify the most common exception
    # --------------------------------------------------------

    most_common_exception = None

    if exceptions_by_type:

        most_common_exception = max(
            exceptions_by_type,
            key=exceptions_by_type.get
        )

    # --------------------------------------------------------
    # Identify highest financial exposure category
    # --------------------------------------------------------

    highest_exposure_type = None

    exposure_by_type = (
        exception_summary[
            "exposure_by_type"
        ]
    )

    if exposure_by_type:

        highest_exposure_type = max(
            exposure_by_type,
            key=exposure_by_type.get
        )

    # --------------------------------------------------------
    # Processing throughput
    # --------------------------------------------------------

    transactions_per_second = (

        total_transactions
        /
        processing_time

        if processing_time > 0
        else 0
    )

    # --------------------------------------------------------
    # Controller evidence
    # --------------------------------------------------------

    return {

        "match_rate":
            round(
                match_rate,
                2
            ),

        "exception_rate":
            round(
                (
                    exception_count
                    /
                    total_transactions
                    *
                    100
                )
                if total_transactions
                else 0,
                2
            ),

        "total_transactions":
            total_transactions,

        "matched_transactions":
            matched,

        "unresolved_exceptions":
            exception_count,

        "financial_exposure":
            round(
                financial_exposure,
                2
            ),

        "exceptions_by_type":
            exceptions_by_type,

        "exceptions_by_severity":
            exceptions_by_severity,

        "exposure_by_type":
            exposure_by_type,

        "exposure_by_severity":
            exception_summary[
                "exposure_by_severity"
            ],

        "most_common_exception_type":
            most_common_exception,

        "highest_exposure_exception_type":
            highest_exposure_type,

        "processing_time_seconds":
            round(
                processing_time,
                4
            ),

        "transactions_per_second":
            round(
                transactions_per_second,
                2
            ),

        "ground_truth_available":
            False,

        "accuracy_note":
            (
                "Precision, recall and F1 score "
                "require a labelled ground-truth "
                "dataset and are not inferred from "
                "the reconciliation results alone."
            ),
    }


# ============================================================
# RECONCILIATION ENGINE
# ============================================================

def reconcile(
    razorpay_file,
    bank_file,
    ledger_file
):

    # ========================================================
    # START TIMER
    # ========================================================

    start_time = time.perf_counter()

    # ========================================================
    # LOAD DATA
    # ========================================================

    razorpay = pd.read_csv(
        razorpay_file
    )

    bank = pd.read_csv(
        bank_file
    )

    ledger = pd.read_csv(
        ledger_file
    )

    # ========================================================
    # VALIDATE STRUCTURE
    # ========================================================

    validate_columns(
        razorpay,
        "Razorpay file"
    )

    validate_columns(
        bank,
        "Bank file"
    )

    validate_columns(
        ledger,
        "Ledger file"
    )

    # ========================================================
    # CLEAN BASIC DATA
    # ========================================================

    for dataframe in [
        razorpay,
        bank,
        ledger
    ]:

        # ----------------------------------------------------
        # Clean transaction IDs
        # ----------------------------------------------------

        dataframe[
            "transaction_id"
        ] = (
            dataframe[
                "transaction_id"
            ]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        # ----------------------------------------------------
        # Normalize references
        # ----------------------------------------------------

        dataframe[
            "normalized_reference"
        ] = (
            dataframe[
                "reference"
            ]
            .apply(
                normalize_reference
            )
        )

        # ----------------------------------------------------
        # Safely convert amounts
        # ----------------------------------------------------

        dataframe[
            "amount"
        ] = (
            dataframe[
                "amount"
            ]
            .apply(
                safe_amount
            )
        )

    # ========================================================
    # DETECT DUPLICATE BANK TRANSACTIONS
    # ========================================================

    duplicate_ids = (
        bank[
            bank.duplicated(
                subset=[
                    "transaction_id"
                ],
                keep=False
            )
        ][
            "transaction_id"
        ]
        .unique()
        .tolist()
    )

    # ========================================================
    # STORAGE
    # ========================================================

    exceptions = []

    matched = 0

    matched_transaction_ids = []

    exception_transaction_ids = set()

    # ========================================================
    # PROCESS EACH RAZORPAY TRANSACTION
    # ========================================================

    for _, payment in razorpay.iterrows():

        transaction_id = (
            payment[
                "transaction_id"
            ]
        )

        payment_amount = safe_amount(
            payment[
                "amount"
            ]
        )

        # ====================================================
        # FIND BANK TRANSACTION
        # ====================================================

        bank_matches = bank[
            bank[
                "transaction_id"
            ]
            ==
            transaction_id
        ]

        # ====================================================
        # FIND LEDGER TRANSACTION
        # ====================================================

        ledger_matches = ledger[
            ledger[
                "transaction_id"
            ]
            ==
            transaction_id
        ]

        # ====================================================
        # MISSING FROM BANK
        # ====================================================

        if bank_matches.empty:

            exceptions.append({

                "transaction_id":
                    transaction_id,

                "type":
                    "MISSING_FROM_BANK",

                "severity":
                    "HIGH",

                "financial_impact":
                    payment_amount,

                "confidence":
                    99,

                "reason":
                    (
                        "Transaction exists in "
                        "Razorpay but not in bank."
                    ),

                "evidence": {

                    "razorpay_amount":
                        payment_amount,

                    "bank_record_found":
                        False,

                    "ledger_record_found":
                        not ledger_matches.empty,
                },

                "recommendation":
                    (
                        "Verify whether the payment "
                        "has been settled or is still "
                        "pending."
                    ),
            })

            exception_transaction_ids.add(
                transaction_id
            )

            continue

        # ====================================================
        # BANK RECORD EXISTS
        # ====================================================

        bank_record = (
            bank_matches.iloc[0]
        )

        bank_amount = safe_amount(
            bank_record[
                "amount"
            ]
        )

        # ====================================================
        # MISSING FROM LEDGER
        # ====================================================

        if ledger_matches.empty:

            exceptions.append({

                "transaction_id":
                    transaction_id,

                "type":
                    "MISSING_FROM_LEDGER",

                "severity":
                    "HIGH",

                "financial_impact":
                    payment_amount,

                "confidence":
                    99,

                "reason":
                    (
                        "Transaction exists in "
                        "Razorpay and bank but "
                        "not in ledger."
                    ),

                "evidence": {

                    "razorpay_amount":
                        payment_amount,

                    "bank_amount":
                        bank_amount,

                    "ledger_record_found":
                        False,
                },

                "recommendation":
                    (
                        "Verify the merchant ledger "
                        "and determine whether the "
                        "transaction needs to be "
                        "recorded."
                    ),
            })

            exception_transaction_ids.add(
                transaction_id
            )

            continue

        # ====================================================
        # LEDGER RECORD EXISTS
        # ====================================================

        ledger_record = (
            ledger_matches.iloc[0]
        )

        ledger_amount = safe_amount(
            ledger_record[
                "amount"
            ]
        )

        # ====================================================
        # AMOUNT MISMATCH
        # ====================================================

        if (
            payment_amount != bank_amount
            or
            payment_amount != ledger_amount
        ):

            bank_difference = (
                payment_amount
                -
                bank_amount
            )

            ledger_difference = (
                payment_amount
                -
                ledger_amount
            )

            exceptions.append({

                "transaction_id":
                    transaction_id,

                "type":
                    "AMOUNT_MISMATCH",

                "severity":
                    "MEDIUM",

                "financial_impact":
                    max(
                        abs(
                            bank_difference
                        ),
                        abs(
                            ledger_difference
                        )
                    ),

                "confidence":
                    85,

                "reason":
                    (
                        f"Razorpay amount is "
                        f"₹{payment_amount:.2f}, "
                        f"bank amount is "
                        f"₹{bank_amount:.2f}, "
                        f"and ledger amount is "
                        f"₹{ledger_amount:.2f}."
                    ),

                "evidence": {

                    "razorpay_amount":
                        payment_amount,

                    "bank_amount":
                        bank_amount,

                    "ledger_amount":
                        ledger_amount,

                    "razorpay_bank_difference":
                        round(
                            bank_difference,
                            2
                        ),

                    "razorpay_ledger_difference":
                        round(
                            ledger_difference,
                            2
                        ),

                    "razorpay_reference":
                        str(
                            payment[
                                "reference"
                            ]
                        ),

                    "bank_reference":
                        str(
                            bank_record[
                                "reference"
                            ]
                        ),

                    "ledger_reference":
                        str(
                            ledger_record[
                                "reference"
                            ]
                        ),
                },

                "recommendation":
                    (
                        "Review the settlement or "
                        "fee breakdown before "
                        "modifying accounting "
                        "records."
                    ),
            })

            exception_transaction_ids.add(
                transaction_id
            )

            continue

        # ====================================================
        # REFERENCE MISMATCH
        # ====================================================

        razorpay_reference = (
            normalize_reference(
                payment[
                    "reference"
                ]
            )
        )

        bank_reference = (
            normalize_reference(
                bank_record[
                    "reference"
                ]
            )
        )

        if (
            razorpay_reference
            != bank_reference
        ):

            exceptions.append({

                "transaction_id":
                    transaction_id,

                "type":
                    "REFERENCE_MISMATCH",

                "severity":
                    "LOW",

                "financial_impact":
                    0,

                "confidence":
                    97,

                "reason":
                    (
                        "Transaction amounts match "
                        "but references are different."
                    ),

                "evidence": {

                    "razorpay_reference":
                        razorpay_reference,

                    "bank_reference":
                        bank_reference,

                    "amounts_match":
                        True,
                },

                "recommendation":
                    (
                        "Verify whether both "
                        "references represent "
                        "the same financial "
                        "transaction."
                    ),
            })

            exception_transaction_ids.add(
                transaction_id
            )

            continue

        # ====================================================
        # SUCCESSFULLY MATCHED
        # ====================================================

        matched += 1

        matched_transaction_ids.append(
            transaction_id
        )

    # ========================================================
    # DUPLICATE BANK TRANSACTIONS
    # ========================================================

    for transaction_id in duplicate_ids:

        duplicate_records = bank[
            bank[
                "transaction_id"
            ]
            ==
            transaction_id
        ]

        duplicate_amount = safe_amount(
            duplicate_records.iloc[0][
                "amount"
            ]
        )

        exceptions.append({

            "transaction_id":
                transaction_id,

            "type":
                "DUPLICATE_TRANSACTION",

            "severity":
                "HIGH",

            "financial_impact":
                duplicate_amount,

            "confidence":
                99,

            "reason":
                (
                    "Multiple bank records use "
                    "the same transaction ID."
                ),

            "evidence": {

                "duplicate_count":
                    len(
                        duplicate_records
                    ),

                "bank_amount":
                    duplicate_amount,
            },

            "recommendation":
                (
                    "Review the duplicate bank "
                    "records and determine which "
                    "transaction is valid."
                ),
        })

        exception_transaction_ids.add(
            transaction_id
        )

    # ========================================================
    # SUMMARY METRICS
    # ========================================================

    total_transactions = len(
        razorpay
    )

    total_bank_records = len(
        bank
    )

    total_ledger_records = len(
        ledger
    )

    total_exposure = sum(
        safe_amount(
            exception[
                "financial_impact"
            ]
        )
        for exception in exceptions
    )

    match_rate = (

        matched
        /
        total_transactions
        *
        100

        if total_transactions
        else 0
    )

    exception_rate = (

        len(exceptions)
        /
        total_transactions
        *
        100

        if total_transactions
        else 0
    )

    # ========================================================
    # EXCEPTION SUMMARY
    # ========================================================

    exception_summary = (
        build_exception_summary(
            exceptions
        )
    )

    # ========================================================
    # PROCESSING TIME
    # ========================================================

    processing_time = (
        time.perf_counter()
        -
        start_time
    )

    transactions_per_second = (

        total_transactions
        /
        processing_time

        if processing_time > 0
        else 0
    )

    # ========================================================
    # AI CONTROLLER EVIDENCE
    # ========================================================

    ai_controller_evidence = (
        build_ai_controller_evidence(
            total_transactions=
                total_transactions,

            matched=
                matched,

            exceptions=
                exceptions,

            exception_summary=
                exception_summary,

            financial_exposure=
                total_exposure,

            processing_time=
                processing_time,
        )
    )

    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print(
        "========================================"
    )

    print(
        "JUICE RECONCILIATION COMPLETE"
    )

    print(
        f"Razorpay transactions: "
        f"{total_transactions}"
    )

    print(
        f"Bank transactions: "
        f"{total_bank_records}"
    )

    print(
        f"Ledger transactions: "
        f"{total_ledger_records}"
    )

    print(
        f"Matched: "
        f"{matched}"
    )

    print(
        f"Exceptions: "
        f"{len(exceptions)}"
    )

    print(
        f"Match rate: "
        f"{match_rate:.2f}%"
    )

    print(
        f"Exception rate: "
        f"{exception_rate:.2f}%"
    )

    print(
        f"Financial exposure: "
        f"₹{total_exposure:,.2f}"
    )

    print(
        f"Processing time: "
        f"{processing_time:.4f} seconds"
    )

    print(
        f"Throughput: "
        f"{transactions_per_second:.2f} "
        f"transactions/sec"
    )

    print(
        "========================================"
    )

    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        # ----------------------------------------------------
        # Basic metrics
        # ----------------------------------------------------

        "total_transactions":
            total_transactions,

        "matched":
            matched,

        "exceptions":
            len(exceptions),

        "match_rate":
            round(
                match_rate,
                2
            ),

        "exception_rate":
            round(
                exception_rate,
                2
            ),

        "financial_exposure":
            round(
                total_exposure,
                2
            ),

        # ----------------------------------------------------
        # Source record counts
        # ----------------------------------------------------

        "source_record_counts": {

            "razorpay":
                total_transactions,

            "bank":
                total_bank_records,

            "ledger":
                total_ledger_records,
        },

        # ----------------------------------------------------
        # Transaction evidence
        # ----------------------------------------------------

        "matched_transaction_ids":
            matched_transaction_ids,

        "exception_transaction_ids":
            list(
                exception_transaction_ids
            ),

        # ----------------------------------------------------
        # Exception analysis
        # ----------------------------------------------------

        "exception_summary":
            exception_summary,

        # ----------------------------------------------------
        # Performance
        # ----------------------------------------------------

        "performance": {

            "processing_time_seconds":
                round(
                    processing_time,
                    4
                ),

            "transactions_per_second":
                round(
                    transactions_per_second,
                    2
                ),
        },

        # ----------------------------------------------------
        # AI-ready evidence
        # ----------------------------------------------------

        "ai_controller_evidence":
            ai_controller_evidence,

        # ----------------------------------------------------
        # Detailed exceptions
        # ----------------------------------------------------

        "exception_details":
            exceptions,
    }