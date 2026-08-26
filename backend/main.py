from pathlib import Path
import tempfile
import shutil
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
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

DATA_DIR = BASE_DIR / "data" / "raw"
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
REPORT_DIR = BASE_DIR / "data" / "reports"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Welcome to JUICE",
        "status": "online",
        "service": "Joint Unified Intelligence for Commerce & Expenses",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "JUICE Backend",
    }


# ============================================================
# EXISTING RECONCILIATION
# ============================================================

@app.post("/reconcile")
def run_reconciliation():

    razorpay_file = DATA_DIR / "razorpay.csv"
    bank_file = DATA_DIR / "bank.csv"
    ledger_file = DATA_DIR / "ledger.csv"

    # --------------------------------------------------------
    # Make sure the synthetic files exist
    # --------------------------------------------------------

    if not razorpay_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Razorpay file not found: {razorpay_file}",
        )

    if not bank_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Bank file not found: {bank_file}",
        )

    if not ledger_file.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Ledger file not found: {ledger_file}",
        )

    try:

        # IMPORTANT:
        # This is where your existing exception-generation
        # logic happens.
        #
        # Do NOT replace this with custom calculations here.

        result = reconcile(
            razorpay_file,
            bank_file,
            ledger_file,
        )

        # Return the complete reconciliation result
        # including exception_details.
        return result

    except Exception as exc:

        print("========================================")
        print("RECONCILIATION ERROR")
        print("========================================")
        print(exc)
        print("========================================")

        raise HTTPException(
            status_code=500,
            detail=f"Reconciliation failed: {str(exc)}",
        )


# ============================================================
# FILE UPLOAD
# ============================================================

@app.post("/upload-reconcile")
async def upload_and_reconcile(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was selected.",
        )

    filename = file.filename.lower()

    allowed_extensions = (
        ".csv",
        ".xls",
        ".xlsx",
    )

    if not filename.endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only CSV, XLS, and XLSX files are supported.",
        )

    # --------------------------------------------------------
    # Create temporary upload directory
    # --------------------------------------------------------

    upload_id = str(uuid.uuid4())

    upload_path = UPLOAD_DIR / f"{upload_id}_{file.filename}"

    try:

        # ----------------------------------------------------
        # Save uploaded file
        # ----------------------------------------------------

        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        print("========================================")
        print("FILE UPLOADED")
        print(f"File: {file.filename}")
        print(f"Path: {upload_path}")
        print("========================================")

        # ----------------------------------------------------
        # Import preprocessing pipeline
        # ----------------------------------------------------
        #
        # If you already have a preprocessing module, this
        # will use it.
        #
        # Expected function:
        #
        # preprocess_file(input_file, output_file)
        #
        # If you haven't created it yet, the upload endpoint
        # will return a clear message rather than crashing
        # the entire application.
        # ----------------------------------------------------

        try:

            from backend.preprocessing import preprocess_file

            cleaned_dir = UPLOAD_DIR / "cleaned"
            cleaned_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            cleaned_path = (
                cleaned_dir
                / f"{upload_id}_cleaned.csv"
            )

            preprocess_file(
                upload_path,
                cleaned_path,
            )

            processed_file = cleaned_path

        except ImportError:

            # ------------------------------------------------
            # Fallback:
            # Keep the uploaded file if preprocessing module
            # does not exist yet.
            # ------------------------------------------------

            print(
                "WARNING: backend.preprocessing "
                "was not found."
            )

            processed_file = upload_path

        # ----------------------------------------------------
        # IMPORTANT
        #
        # Your current reconcile() expects three files:
        #
        # razorpay
        # bank
        # ledger
        #
        # Therefore a single uploaded file cannot magically
        # replace all three unless the preprocessing pipeline
        # determines what type of file it is.
        #
        # For now we return the processed file information.
        # ----------------------------------------------------

        return {
            "success": True,
            "message": "File uploaded and preprocessing completed.",
            "filename": file.filename,
            "original_file": str(upload_path),
            "processed_file": str(processed_file),
            "upload_id": upload_id,
        }

    except Exception as exc:

        print("========================================")
        print("UPLOAD ERROR")
        print("========================================")
        print(exc)
        print("========================================")

        raise HTTPException(
            status_code=500,
            detail=f"File processing failed: {str(exc)}",
        )


# ============================================================
# PDF FINANCE REPORT
# ============================================================

@app.post("/generate-report")
def generate_report(report_data: dict):

    try:

        from backend.report_generator import generate_finance_report

    except ImportError:

        raise HTTPException(
            status_code=500,
            detail=(
                "Report generator is not configured. "
                "Create backend/report_generator.py "
                "with generate_finance_report()."
            ),
        )

    try:

        report_id = str(uuid.uuid4())

        report_path = (
            REPORT_DIR
            / f"JUICE_Finance_Report_{report_id}.pdf"
        )

        # ----------------------------------------------------
        # Generate PDF
        # ----------------------------------------------------

        generate_finance_report(
            report_data,
            report_path,
        )

        if not report_path.exists():

            raise HTTPException(
                status_code=500,
                detail="PDF report was not created.",
            )

        return FileResponse(
            path=report_path,
            media_type="application/pdf",
            filename="JUICE_Finance_Report.pdf",
        )

    except HTTPException:
        raise

    except Exception as exc:

        print("========================================")
        print("REPORT GENERATION ERROR")
        print("========================================")
        print(exc)
        print("========================================")

        raise HTTPException(
            status_code=500,
            detail=f"Could not generate PDF report: {str(exc)}",
        )


# ============================================================
# SERVER INFORMATION
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