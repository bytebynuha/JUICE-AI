from pathlib import Path
import pandas as pd
import re


# ============================================================
# JUICE DATA PREPROCESSOR
# ============================================================
#
# This file:
# 1. Reads CSV / XLS / XLSX files
# 2. Cleans column names
# 3. Removes empty rows and columns
# 4. Cleans transaction IDs
# 5. Cleans references
# 6. Cleans amounts
# 7. Removes duplicate transactions
# 8. Checks required columns
# 9. Saves a cleaned CSV
#
# The cleaned CSV is then given to reconciliation.py
# ============================================================


# ------------------------------------------------------------
# SUPPORTED FILE TYPES
# ------------------------------------------------------------

SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xls",
    ".xlsx",
}


# ------------------------------------------------------------
# REQUIRED COLUMNS
# ------------------------------------------------------------

REQUIRED_COLUMNS = [
    "transaction_id",
    "reference",
    "amount",
]


# ------------------------------------------------------------
# COLUMN NAME NORMALIZATION
# ------------------------------------------------------------

def normalize_column_name(column):
    """
    Turns messy column names into a standard format.

    Examples:

        "Transaction ID"  -> "transaction_id"
        "Transaction-ID"  -> "transaction_id"
        "Txn ID"          -> "transaction_id"
        "Amount (INR)"    -> "amount"
        "Reference ID"    -> "reference"
    """

    column = str(column).strip().lower()

    # Remove brackets
    column = re.sub(r"[\(\)\[\]\{\}]", "", column)

    # Replace separators with spaces
    column = re.sub(r"[-_/]+", " ", column)

    # Remove extra spaces
    column = re.sub(r"\s+", " ", column).strip()

    # Common aliases
    aliases = {
        "transaction id": "transaction_id",
        "transactionid": "transaction_id",
        "txn id": "transaction_id",
        "txnid": "transaction_id",
        "transaction": "transaction_id",

        "reference id": "reference",
        "referenceid": "reference",
        "ref id": "reference",
        "ref": "reference",

        "amount inr": "amount",
        "amount rs": "amount",
        "amount rupees": "amount",
        "transaction amount": "amount",
        "payment amount": "amount",
    }

    if column in aliases:
        return aliases[column]

    # Standard snake_case conversion
    column = column.replace(" ", "_")

    return column


# ------------------------------------------------------------
# CLEAN TEXT
# ------------------------------------------------------------

def clean_text(value):
    """
    Cleans text values.

    Example:

        "  txn001  " -> "txn001"
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


# ------------------------------------------------------------
# CLEAN TRANSACTION ID
# ------------------------------------------------------------

def clean_transaction_id(value):
    """
    Cleans transaction IDs while keeping their identity.

    Example:

        " txn001 " -> "txn001"
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


# ------------------------------------------------------------
# CLEAN REFERENCE
# ------------------------------------------------------------

def clean_reference(value):
    """
    Cleans reference values.

    References are converted to uppercase so that:

        pay_123
        PAY_123
        Pay_123

    are treated as the same reference.
    """

    if pd.isna(value):
        return ""

    return str(value).strip().upper()


# ------------------------------------------------------------
# CLEAN AMOUNT
# ------------------------------------------------------------

def clean_amount(value):
    """
    Converts messy currency values into numbers.

    Examples:

        ₹5,000       -> 5000.0
        Rs. 5000     -> 5000.0
        5,000.50     -> 5000.50
        "₹ 1,200"    -> 1200.0
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    # Remove currency symbols and text
    value = value.replace("₹", "")
    value = value.replace("Rs.", "")
    value = value.replace("Rs", "")
    value = value.replace("INR", "")
    value = value.replace("inr", "")

    # Remove commas
    value = value.replace(",", "")

    # Keep only numbers, decimal point and minus sign
    value = re.sub(r"[^0-9.\-]", "", value)

    if value == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


# ------------------------------------------------------------
# READ FILE
# ------------------------------------------------------------

def read_financial_file(file_path):
    """
    Reads CSV, XLS or XLSX files.

    Parameters
    ----------
    file_path : str or Path

    Returns
    -------
    pandas.DataFrame
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = file_path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. "
            "Please upload a CSV, XLS or XLSX file."
        )

    try:

        if extension == ".csv":
            dataframe = pd.read_csv(
                file_path
            )

        elif extension == ".xls":
            dataframe = pd.read_excel(
                file_path,
                engine="xlrd"
            )

        elif extension == ".xlsx":
            dataframe = pd.read_excel(
                file_path,
                engine="openpyxl"
            )

        else:
            raise ValueError(
                "Unsupported file format."
            )

    except Exception as error:

        raise ValueError(
            f"Could not read the uploaded file: {error}"
        )

    return dataframe


# ------------------------------------------------------------
# REMOVE COMPLETELY EMPTY ROWS / COLUMNS
# ------------------------------------------------------------

def remove_empty_data(dataframe):
    """
    Removes rows and columns that are completely empty.
    """

    dataframe = dataframe.dropna(
        axis=0,
        how="all"
    )

    dataframe = dataframe.dropna(
        axis=1,
        how="all"
    )

    return dataframe


# ------------------------------------------------------------
# VALIDATE REQUIRED COLUMNS
# ------------------------------------------------------------

def validate_columns(dataframe):
    """
    Makes sure the cleaned dataset contains:

        transaction_id
        reference
        amount
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if missing_columns:

        raise ValueError(
            "The uploaded file is missing required "
            f"columns: {', '.join(missing_columns)}. "
            "JUICE needs transaction ID, reference and amount "
            "information."
        )


# ------------------------------------------------------------
# CLEAN DATAFRAME
# ------------------------------------------------------------

def clean_dataframe(dataframe):
    """
    Cleans a financial dataframe.
    """

    if dataframe is None:
        raise ValueError(
            "No data was provided."
        )

    if dataframe.empty:
        raise ValueError(
            "The uploaded file is empty."
        )

    # --------------------------------------------------------
    # CLEAN COLUMN NAMES
    # --------------------------------------------------------

    dataframe.columns = [
        normalize_column_name(column)
        for column in dataframe.columns
    ]

    # --------------------------------------------------------
    # REMOVE EMPTY ROWS / COLUMNS
    # --------------------------------------------------------

    dataframe = remove_empty_data(
        dataframe
    )

    # --------------------------------------------------------
    # VALIDATE REQUIRED COLUMNS
    # --------------------------------------------------------

    validate_columns(
        dataframe
    )

    # --------------------------------------------------------
    # CLEAN TRANSACTION IDS
    # --------------------------------------------------------

    dataframe["transaction_id"] = (
        dataframe["transaction_id"]
        .apply(clean_transaction_id)
    )

    # --------------------------------------------------------
    # CLEAN REFERENCES
    # --------------------------------------------------------

    dataframe["reference"] = (
        dataframe["reference"]
        .apply(clean_reference)
    )

    # --------------------------------------------------------
    # CLEAN AMOUNTS
    # --------------------------------------------------------

    dataframe["amount"] = (
        dataframe["amount"]
        .apply(clean_amount)
    )

    # --------------------------------------------------------
    # REMOVE ROWS WITHOUT TRANSACTION ID
    # --------------------------------------------------------

    dataframe = dataframe[
        dataframe["transaction_id"] != ""
    ]

    # --------------------------------------------------------
    # REMOVE INVALID AMOUNTS
    # --------------------------------------------------------

    dataframe = dataframe[
        dataframe["amount"].notna()
    ]

    # --------------------------------------------------------
    # REMOVE DUPLICATE TRANSACTIONS
    # --------------------------------------------------------

    dataframe = dataframe.drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )

    # --------------------------------------------------------
    # RESET INDEX
    # --------------------------------------------------------

    dataframe = dataframe.reset_index(
        drop=True
    )

    return dataframe


# ------------------------------------------------------------
# PREPROCESS ONE FILE
# ------------------------------------------------------------

def preprocess_file(
    input_file,
    output_file
):
    """
    Reads, cleans and saves one financial file.

    Example:

        preprocess_file(
            "bank.xlsx",
            "cleaned_bank.csv"
        )
    """

    dataframe = read_financial_file(
        input_file
    )

    original_rows = len(
        dataframe
    )

    cleaned_dataframe = clean_dataframe(
        dataframe
    )

    cleaned_dataframe.to_csv(
        output_file,
        index=False
    )

    cleaned_rows = len(
        cleaned_dataframe
    )

    return {
        "input_file": str(input_file),
        "output_file": str(output_file),
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "duplicates_or_invalid_rows_removed": (
            original_rows - cleaned_rows
        ),
    }


# ------------------------------------------------------------
# PREPROCESS THREE JUICE FILES
# ------------------------------------------------------------

def preprocess_financial_files(
    razorpay_file,
    bank_file,
    ledger_file,
    output_directory
):
    """
    Preprocesses all three financial files:

        Razorpay
        Bank
        Ledger

    and produces clean CSV files.
    """

    output_directory = Path(
        output_directory
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    cleaned_razorpay = (
        output_directory /
        "razorpay_cleaned.csv"
    )

    cleaned_bank = (
        output_directory /
        "bank_cleaned.csv"
    )

    cleaned_ledger = (
        output_directory /
        "ledger_cleaned.csv"
    )

    razorpay_info = preprocess_file(
        razorpay_file,
        cleaned_razorpay
    )

    bank_info = preprocess_file(
        bank_file,
        cleaned_bank
    )

    ledger_info = preprocess_file(
        ledger_file,
        cleaned_ledger
    )

    return {
        "razorpay_file": str(
            cleaned_razorpay
        ),

        "bank_file": str(
            cleaned_bank
        ),

        "ledger_file": str(
            cleaned_ledger
        ),

        "preprocessing": {
            "razorpay": razorpay_info,
            "bank": bank_info,
            "ledger": ledger_info,
        },
    }