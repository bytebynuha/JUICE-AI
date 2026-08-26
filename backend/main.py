from pathlib import Path
import shutil
import uuid

import pandas as pd

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.reconciliation import reconcile


# ============================================================
# JUICE APP
# ============================================================

app = FastAPI(
    title="JUICE API",
    description="Joint Unified Intelligence for Commerce & Expenses",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = (
    BASE_DIR
    / "data"
    / "raw"
)

UPLOAD_DIR = (
    BASE_DIR
    / "data"
    / "uploads"
)

REPORT_DIR = (
    BASE_DIR
    / "data"
    / "reports"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Welcome to JUICE",
        "status": "online",
        "service": (
            "Joint Unified Intelligence "
            "for Commerce & Expenses"
        ),
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "JUICE Backend",
    }


# ============================================================
# NORMAL RECONCILIATION
# ============================================================

@app.post("/reconcile")
def run_reconciliation():

    razorpay_file = (
        DATA_DIR
        / "razorpay.csv"
    )

    bank_file = (
        DATA_DIR
        / "bank.csv"
    )

    ledger_file = (
        DATA_DIR
        / "ledger.csv"
    )

    if not razorpay_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Razorpay file not found.",
        )

    if not bank_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Bank file not found.",
        )

    if not ledger_file.exists():

        raise HTTPException(
            status_code=404,
            detail="Ledger file not found.",
        )

    try:

        result = reconcile(
            razorpay_file,
            bank_file,
            ledger_file,
        )

        return result

    except Exception as exc:

        print(
            "RECONCILIATION ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Reconciliation failed: "
                f"{str(exc)}"
            ),
        )


# ============================================================
# FILE READING
# ============================================================

def read_financial_file(
    file_path: Path,
):
    """
    Read CSV, XLS or XLSX.
    """

    extension = (
        file_path
        .suffix
        .lower()
    )

    if extension == ".csv":

        return pd.read_csv(
            file_path
        )

    if extension in [".xls", ".xlsx"]:

        return pd.read_excel(
            file_path
        )

    raise ValueError(
        "Unsupported file format."
    )


# ============================================================
# PREPROCESSING
# ============================================================

def preprocess_dataframe(
    dataframe: pd.DataFrame,
):
    """
    Clean a financial dataframe.

    Steps:

    1. Remove completely empty rows.
    2. Remove completely empty columns.
    3. Normalize column names.
    4. Remove whitespace.
    5. Remove duplicate rows.
    6. Fill missing values.
    """

    df = dataframe.copy()

    original_rows = len(df)

    # --------------------------------------------------------
    # Normalize column names
    # --------------------------------------------------------

    df.columns = [
        str(column)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        for column in df.columns
    ]

    # --------------------------------------------------------
    # Remove empty rows
    # --------------------------------------------------------

    df = df.dropna(
        axis=0,
        how="all",
    )

    # --------------------------------------------------------
    # Remove empty columns
    # --------------------------------------------------------

    df = df.dropna(
        axis=1,
        how="all",
    )

    # --------------------------------------------------------
    # Clean text
    # --------------------------------------------------------

    for column in df.columns:

        if df[column].dtype == "object":

            df[column] = (
                df[column]
                .apply(
                    lambda value:
                    value.strip()
                    if isinstance(
                        value,
                        str,
                    )
                    else value
                )
            )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    before_duplicates = len(df)

    df = df.drop_duplicates()

    duplicates_removed = (
        before_duplicates
        - len(df)
    )

    # --------------------------------------------------------
    # Fill missing values
    # --------------------------------------------------------

    missing_before = int(
        df.isna()
        .sum()
        .sum()
    )

    for column in df.columns:

        if pd.api.types.is_numeric_dtype(
            df[column]
        ):

            df[column] = (
                df[column]
                .fillna(0)
            )

        else:

            df[column] = (
                df[column]
                .fillna("UNKNOWN")
            )

    missing_after = int(
        df.isna()
        .sum()
        .sum()
    )

    return (
        df,
        {
            "original_rows": original_rows,
            "cleaned_rows": len(df),
            "duplicates_removed": (
                duplicates_removed
            ),
            "missing_values_before": (
                missing_before
            ),
            "missing_values_after": (
                missing_after
            ),
        },
    )


# ============================================================
# SAVE PROCESSED FILE
# ============================================================

def save_processed_file(
    dataframe: pd.DataFrame,
    output_path: Path,
):

    dataframe.to_csv(
        output_path,
        index=False,
    )


# ============================================================
# VALIDATE UPLOAD
# ============================================================

def validate_upload(
    uploaded_file: UploadFile,
    label: str,
):

    if not uploaded_file:

        raise HTTPException(
            status_code=400,
            detail=(
                f"{label} was not uploaded."
            ),
        )

    if not uploaded_file.filename:

        raise HTTPException(
            status_code=400,
            detail=(
                f"No {label} file was selected."
            ),
        )

    extension = (
        Path(
            uploaded_file.filename
        )
        .suffix
        .lower()
    )

    allowed = {
        ".csv",
        ".xls",
        ".xlsx",
    }

    if extension not in allowed:

        raise HTTPException(
            status_code=400,
            detail=(
                f"{label} must be "
                "CSV, XLS, or XLSX."
            ),
        )


# ============================================================
# SAVE UPLOAD
# ============================================================

async def save_upload(
    uploaded_file: UploadFile,
    destination: Path,
):

    with destination.open("wb") as buffer:

        shutil.copyfileobj(
            uploaded_file.file,
            buffer,
        )


# ============================================================
# UPLOAD + PREPROCESS + RECONCILE
# ============================================================

@app.post("/upload-reconcile")
async def upload_and_reconcile(

    razorpay_file: UploadFile = File(...),

    bank_file: UploadFile = File(...),

    ledger_file: UploadFile = File(...),

):

    # --------------------------------------------------------
    # Validate all three files
    # --------------------------------------------------------

    validate_upload(
        razorpay_file,
        "Razorpay file",
    )

    validate_upload(
        bank_file,
        "Bank file",
    )

    validate_upload(
        ledger_file,
        "Ledger file",
    )

    # --------------------------------------------------------
    # Unique upload folder
    # --------------------------------------------------------

    upload_id = uuid.uuid4().hex

    upload_folder = (
        UPLOAD_DIR
        / upload_id
    )

    upload_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed_folder = (
        upload_folder
        / "processed"
    )

    processed_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:

        # ====================================================
        # SAVE ORIGINAL FILES
        # ====================================================

        razorpay_original = (
            upload_folder
            / (
                "razorpay_original"
                + Path(
                    razorpay_file.filename
                ).suffix.lower()
            )
        )

        bank_original = (
            upload_folder
            / (
                "bank_original"
                + Path(
                    bank_file.filename
                ).suffix.lower()
            )
        )

        ledger_original = (
            upload_folder
            / (
                "ledger_original"
                + Path(
                    ledger_file.filename
                ).suffix.lower()
            )
        )

        await save_upload(
            razorpay_file,
            razorpay_original,
        )

        await save_upload(
            bank_file,
            bank_original,
        )

        await save_upload(
            ledger_file,
            ledger_original,
        )

        print(
            "========================================"
        )

        print(
            "THREE FILES UPLOADED"
        )

        print(
            "Razorpay:",
            razorpay_file.filename,
        )

        print(
            "Bank:",
            bank_file.filename,
        )

        print(
            "Ledger:",
            ledger_file.filename,
        )

        print(
            "========================================"
        )

        # ====================================================
        # READ FILES
        # ====================================================

        razorpay_df = read_financial_file(
            razorpay_original
        )

        bank_df = read_financial_file(
            bank_original
        )

        ledger_df = read_financial_file(
            ledger_original
        )

        # ====================================================
        # PREPROCESS
        # ====================================================

        (
            razorpay_clean,
            razorpay_stats,
        ) = preprocess_dataframe(
            razorpay_df
        )

        (
            bank_clean,
            bank_stats,
        ) = preprocess_dataframe(
            bank_df
        )

        (
            ledger_clean,
            ledger_stats,
        ) = preprocess_dataframe(
            ledger_df
        )

        # ====================================================
        # SAVE CLEAN FILES
        # ====================================================

        processed_razorpay = (
            processed_folder
            / "razorpay.csv"
        )

        processed_bank = (
            processed_folder
            / "bank.csv"
        )

        processed_ledger = (
            processed_folder
            / "ledger.csv"
        )

        save_processed_file(
            razorpay_clean,
            processed_razorpay,
        )

        save_processed_file(
            bank_clean,
            processed_bank,
        )

        save_processed_file(
            ledger_clean,
            processed_ledger,
        )

        print(
            "========================================"
        )

        print(
            "PREPROCESSING COMPLETE"
        )

        print(
            "Razorpay:",
            razorpay_stats,
        )

        print(
            "Bank:",
            bank_stats,
        )

        print(
            "Ledger:",
            ledger_stats,
        )

        print(
            "========================================"
        )

        # ====================================================
        # RECONCILIATION
        # ====================================================

        result = reconcile(
            processed_razorpay,
            processed_bank,
            processed_ledger,
        )

        # ====================================================
        # ADD PREPROCESSING INFORMATION
        # ====================================================

        result["upload_id"] = (
            upload_id
        )

        result["source"] = (
            "user_uploaded_files"
        )

        result["preprocessing"] = {

            "status": "completed",

            "files_processed": 3,

            "razorpay": razorpay_stats,

            "bank": bank_stats,

            "ledger": ledger_stats,

        }

        print(
            "========================================"
        )

        print(
            "RECONCILIATION COMPLETE"
        )

        print(
            "Exceptions:",
            result.get(
                "exceptions",
                0,
            ),
        )

        print(
            "Financial exposure:",
            result.get(
                "financial_exposure",
                0,
            ),
        )

        print(
            "========================================"
        )

        return result

    except HTTPException:
        raise

    except Exception as exc:

        print(
            "========================================"
        )

        print(
            "UPLOAD / PROCESSING ERROR"
        )

        print(
            repr(exc)
        )

        print(
            "========================================"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "JUICE could not process "
                "the uploaded files: "
                f"{str(exc)}"
            ),
        )


# ============================================================
# PDF FINANCE REPORT
# ============================================================

@app.post("/generate-report")
def generate_report(
    report_data: dict,
):

    try:

        from backend.report_generator import (
            generate_finance_report
        )

    except ImportError:

        raise HTTPException(
            status_code=500,
            detail=(
                "Report generator is not "
                "configured."
            ),
        )

    try:

        report_id = uuid.uuid4().hex

        report_path = (
            REPORT_DIR
            / (
                "JUICE_Finance_Report_"
                f"{report_id}.pdf"
            )
        )

        generate_finance_report(
            report_data,
            report_path,
        )

        if not report_path.exists():

            raise HTTPException(
                status_code=500,
                detail=(
                    "PDF report was not created."
                ),
            )

        return FileResponse(
            path=report_path,
            media_type="application/pdf",
            filename=(
                "JUICE_Finance_Report.pdf"
            ),
        )

    except HTTPException:
        raise

    except Exception as exc:

        print(
            "REPORT GENERATION ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Could not generate "
                f"PDF report: {str(exc)}"
            ),
        )


# ============================================================
# STATUS
# ============================================================

@app.get("/api/status")
def api_status():

    return {
        "service": "JUICE",
        "status": "online",
        "reconciliation": True,
        "file_upload": True,
        "pdf_reports": True,
    }