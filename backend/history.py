import sqlite3
from pathlib import Path
from datetime import datetime


# ============================================================
# DATABASE LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_FILE = BASE_DIR / "juice_history.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_history_database():

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS upload_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            uploaded_at TEXT NOT NULL,

            razorpay_filename TEXT,

            bank_filename TEXT,

            ledger_filename TEXT,

            total_transactions INTEGER DEFAULT 0,

            matched INTEGER DEFAULT 0,

            exceptions INTEGER DEFAULT 0,

            match_rate REAL DEFAULT 0,

            financial_exposure REAL DEFAULT 0

        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE A NEW UPLOAD
# ============================================================

def save_upload_history(
    razorpay_filename,
    bank_filename,
    ledger_filename,
    result,
):

    connection = sqlite3.connect(DATABASE_FILE)

    cursor = connection.cursor()

    uploaded_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO upload_history (
            uploaded_at,
            razorpay_filename,
            bank_filename,
            ledger_filename,
            total_transactions,
            matched,
            exceptions,
            match_rate,
            financial_exposure
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            uploaded_at,

            razorpay_filename,

            bank_filename,

            ledger_filename,

            result.get(
                "total_transactions",
                0
            ),

            result.get(
                "matched",
                0
            ),

            result.get(
                "exceptions",
                0
            ),

            result.get(
                "match_rate",
                0
            ),

            result.get(
                "financial_exposure",
                0
            ),
        ),
    )

    connection.commit()

    connection.close()


# ============================================================
# GET ALL UPLOAD HISTORY
# ============================================================

def get_upload_history():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            uploaded_at,
            razorpay_filename,
            bank_filename,
            ledger_filename,
            total_transactions,
            matched,
            exceptions,
            match_rate,
            financial_exposure

        FROM upload_history

        ORDER BY uploaded_at DESC
        """
    )

    records = cursor.fetchall()

    connection.close()

    history = []

    for record in records:

        history.append(
            dict(record)
        )

    return history