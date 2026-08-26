from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.reconciliation import reconcile


app = FastAPI(
    title="JUICE API",
    description="Joint Unified Intelligence for Commerce & Expenses",
    version="1.0.0",
)


# Allow our frontend to communicate with the backend
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


# Project data location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"


@app.get("/")
def root():
    return {
        "message": "Welcome to JUICE",
        "status": "online",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "JUICE Backend",
    }


@app.post("/reconcile")
def run_reconciliation():

    razorpay_file = DATA_DIR / "razorpay.csv"
    bank_file = DATA_DIR / "bank.csv"
    ledger_file = DATA_DIR / "ledger.csv"

    result = reconcile(
        razorpay_file,
        bank_file,
        ledger_file,
    )

    return result