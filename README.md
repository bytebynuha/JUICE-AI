# JUICE AI — Joint Unified Intelligence for Commerce and Expenses

Intelligent Finance Controller

> **Find the mismatch. Quantify the risk. Control the money.**

JUICE AI is an intelligent finance controller designed to simplify and automate financial reconciliation workflows.

It transforms fragmented transaction data from payment systems, bank statements, and internal ledgers into a single, auditable reconciliation workflow — helping finance teams identify discrepancies, understand financial exposure, investigate exceptions, and generate reports without manually comparing thousands of spreadsheet rows.

---

## 🚀 Why JUICE?

Modern businesses generate financial data across multiple systems.

A single transaction may appear in:

- Payment gateway records
- Bank statements
- Internal accounting ledgers

These sources don't always agree.

A transaction might be:

- Missing from one system
- Recorded with a different amount
- Referenced differently
- Duplicated
- Present in one system but absent in another

Traditional reconciliation often means manually comparing spreadsheets, filtering rows, identifying discrepancies, and calculating the potential financial impact.

**JUICE changes that workflow.**

Instead of asking:

> **"Which transactions don't match?"**

JUICE helps finance teams answer:

> **"What doesn't match, why doesn't it match, and how much financial exposure does it represent?"**

---

# 🎯 Project Objective

JUICE aims to turn financial reconciliation from a repetitive spreadsheet task into an intelligent financial control loop.

### The JUICE workflow

```text
                 FINANCIAL DATA
                       │
                       ▼
                ┌─────────────┐
                │    Upload   │
                └──────┬──────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Preprocessing  │
              │  & Normalization │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Reconciliation   │
              │     Engine       │
              └────────┬─────────┘
                       │
                 ┌─────┴─────┐
                 ▼           ▼
              MATCHED     EXCEPTIONS
                 │           │
                 │           ▼
                 │    ┌──────────────┐
                 │    │ Risk &       │
                 │    │ Exposure     │
                 │    └──────┬───────┘
                 │           │
                 │           ▼
                 │    ┌──────────────┐
                 │    │ AI-Assisted  │
                 │    │ Investigation│
                 │    └──────┬───────┘
                 │           │
                 └─────┬─────┘
                       ▼
                ┌─────────────┐
                │ Finance     │
                │ Report      │
                └─────────────┘

✨ Key Features
1. 📂 Financial Data Upload

Upload financial datasets and reconcile transaction records.

Supported formats:

.CSV
.XLS
.XLSX
2. 🧹 Data Preprocessing & Normalization

Financial datasets frequently contain inconsistent structures.

JUICE prepares uploaded data before reconciliation by handling:

Different column naming conventions
Missing values
Duplicate records
Data normalization
Transaction-level cleanup

This ensures that the reconciliation engine receives structured and comparable information.

3. ⚖️ Deterministic Reconciliation Engine

At the core of JUICE is a rule-based reconciliation engine.

Rather than allowing an AI model to arbitrarily decide whether financial records match, the financial matching logic remains deterministic and auditable.

The system identifies discrepancies such as:

Exception Type	Description
Amount Mismatch	Transaction references match but amounts differ
Duplicate	Multiple records represent the same transaction
Reference Mismatch	Transaction identifiers don't correspond
Missing Transaction	An expected transaction is absent from another source

This creates a clear separation between:

Financial Truth → Deterministic Logic

and

Financial Understanding → AI Assistance

4. 📊 Reconciliation Dashboard

After processing, JUICE provides an overview of the financial batch.

The dashboard displays:

Total transactions
Matched transactions
Exceptions
Match rate
Financial exposure
Risk indicators

Instead of manually searching through thousands of rows, finance teams can immediately understand the state of the reconciliation.

5. 🚨 Exception Management

JUICE doesn't simply report that reconciliation failed.

It categorizes and surfaces individual exceptions so they can be investigated.

Users can:

Filter exceptions
Review transaction details
Identify exception types
Investigate individual records
Prioritize financial risk
6. 💰 Financial Exposure

Not every exception represents the same level of risk.

JUICE calculates the financial exposure associated with unresolved discrepancies.

For example:

       10 Exceptions
             │
             ▼
    ₹250,000 Exposure

This allows finance teams to prioritize financially significant issues, rather than treating every exception equally.

7. 🤖 AI-Assisted Investigation

JUICE uses AI where it provides the most value — interpretation and investigation.

The AI layer is designed to help transform raw reconciliation exceptions into information that is easier for finance teams to understand and act upon.

The underlying reconciliation decision remains deterministic.

AI explains the financial problem.

The reconciliation engine establishes the financial result.

8. 🕒 Reconciliation History

Completed reconciliation workflows can be recorded and reviewed through the history functionality.

This provides a foundation for:

Reviewing previous uploads
Tracking reconciliation runs
Comparing previous results
Maintaining operational visibility
9. 📄 Finance Reports

JUICE can generate a PDF finance report from reconciliation results.

The report provides a shareable representation of the reconciliation outcome for downstream review.

🧠 System Architecture
                         ┌──────────────────────┐
                         │       JUICE AI       │
                         │  Finance Controller  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │   Dashboard / UI     │
                         └──────────┬───────────┘
                                    │
                              HTTP / REST
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌───────────────┐   ┌───────────────┐   ┌──────────────┐
        │ Preprocessing │   │Reconciliation │   │   Reporting  │
        │ & Normalizing │   │    Engine     │   │    Engine    │
        └───────┬───────┘   └───────┬───────┘   └──────┬───────┘
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    │
                                    ▼
                             ┌─────────────┐
                             │   SQLite    │
                             │   History   │
                             └─────────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ AI Investigation│
                           │  & Explanation  │
                           └─────────────────┘

🛠️ Technology Stack
Frontend
React
Vite
JavaScript
CSS
Responsive UI
Backend
Python
FastAPI
Uvicorn
Data Processing
Python
Pandas
CSV / Excel processing
Database
SQLite
Reporting
ReportLab
PDF generation
AI
AI-assisted exception interpretation and investigation
📁 Project Structure
JUICE-AI/
│
├── backend/
│   ├── main.py
│   ├── preprocessing.py
│   ├── reconciliation.py
│   ├── report.py
│   ├── report_generator.py
│   ├── history.py
│   ├── generate_data.py
│   ├── test_reconciliation.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── ...
│   │
│   ├── package.json
│   └── ...
│
├── data/
│
├── sample_data_upload/
│
├── README.md
└── ...
⚙️ Getting Started
Prerequisites

Make sure you have:

Python 3.10+
Node.js 18+
npm
Git
1. Clone the Repository
git clone https://github.com/bytebynuha/JUICE-AI.git

Navigate into the project:

cd JUICE-AI
🐍 Backend Setup

Install Python dependencies:

pip install -r backend/requirements.txt

Start the backend:

python -m uvicorn backend.main:app --reload --port 8000

The backend will be available at:

http://127.0.0.1:8000
Health Check

Open:

http://127.0.0.1:8000/health

A healthy backend should return:

{
  "status": "healthy",
  "service": "JUICE Backend"
}
⚛️ Frontend Setup

Open a second terminal.

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5174
🔄 How JUICE Works
Step 1 — Upload

Upload the financial dataset.

Step 2 — Preprocess

JUICE normalizes and prepares the uploaded data.

Step 3 — Reconcile

The reconciliation engine compares transaction records.

Step 4 — Analyze

The dashboard displays:

Total Transactions
        ↓
Matched Transactions
        ↓
Exceptions
        ↓
Match Rate
        ↓
Financial Exposure

Step 5 — Investigate

Review individual exceptions and identify the underlying discrepancy.

Step 6 — Report

Generate a PDF report containing the reconciliation results.

Step 7 — History

Review previous reconciliation workflows.

📊 Reconciliation Output

A typical reconciliation run produces metrics such as:

┌─────────────────────────────────────────┐
│        FINANCIAL CONTROL SNAPSHOT       │
├─────────────────────────────────────────┤
│                                         │
│  Total Transactions       50+           │
│  Matched                  XX            │
│  Exceptions               XX            │
│  Match Rate               XX%           │
│  Financial Exposure      ₹XX,XXX        │
│                                         │
└─────────────────────────────────────────┘

The actual values depend on the uploaded dataset.

🔎 Exception Intelligence

JUICE focuses on turning exceptions into actionable information.

Instead of simply returning:

RECONCILIATION FAILED

the system provides structured exception information:

Transaction
    │
    ├── Reference
    ├── Expected Amount
    ├── Actual Amount
    ├── Exception Type
    └── Financial Impact

This makes investigation significantly more practical for finance operations.

🏗️ Engineering Principles

Financial systems require a different approach to AI.

JUICE follows three core principles.

1. Deterministic Where Accuracy Matters

Financial matching should be reproducible.

Given the same input, the reconciliation engine should produce the same result.

2. AI Where Understanding Matters

AI is most useful when it helps a human understand a complex exception rather than inventing financial facts.

3. Human-in-the-Loop

JUICE is designed to assist finance professionals, not blindly replace financial judgment.

The system surfaces:

WHAT HAPPENED
      ↓
WHY IT HAPPENED
      ↓
HOW SIGNIFICANT IT IS
      ↓
WHAT NEEDS ATTENTION
🧩 Build Challenges & Technical Obstacles
Challenge 1 — Inconsistent Financial Data

Different financial systems can represent transactions differently.

Solution

A dedicated preprocessing layer normalizes uploaded datasets before they reach the reconciliation engine.

Challenge 2 — Financial Accuracy vs AI Flexibility

Using an AI model directly for financial reconciliation can introduce ambiguity.

Solution

The core reconciliation engine is deterministic and rule-based.

AI is positioned around the financial result rather than replacing the source of truth.

Challenge 3 — Actionable Exception Management

Simply identifying mismatches isn't enough.

Solution

JUICE categorizes exceptions and surfaces them at transaction level, together with financial exposure and investigation context.

Challenge 4 — End-to-End Integration

The application needed to reliably connect:

Upload
  ↓
Preprocess
  ↓
Reconcile
  ↓
Dashboard
  ↓
Investigate
  ↓
History
  ↓
Report
Solution

The frontend and backend were separated into clear responsibilities and connected through REST APIs.

Challenge 5 — Measuring Financial Risk

Counting exceptions alone doesn't tell a finance team how serious the problem is.

Solution

JUICE calculates financial exposure associated with unresolved discrepancies, allowing teams to prioritize exceptions based on potential financial impact.

🎯 Impact

JUICE is designed to help finance teams move from:

Manual Spreadsheet Comparison
              ↓
      Find Discrepancies
              ↓
       Understand Risk
              ↓
      Prepare Reports

to:

              JUICE
                │
                ▼
        Automated Processing
                │
                ▼
        Reconciliation
                │
                ▼
      Exception Detection
                │
                ▼
       Risk Quantification
                │
                ▼
        Investigation
                │
                ▼
          Reporting

The goal is simple:

Spend less time finding financial problems and more time resolving them.

🚀 Future Scope

JUICE provides a foundation for a broader AI-powered finance operations platform.

Potential future extensions include:

Automated reconciliation scheduling
Larger transaction volumes
Streaming transaction reconciliation
Additional payment provider integrations
Bank API integrations
ERP and accounting integrations
Automated exception prioritization
Historical anomaly detection
Role-based finance workflows
Approval and escalation workflows
Automated finance-agent actions
Advanced audit trails
Cloud deployment
Continuous financial monitoring

The long-term vision is to evolve from:

A tool that finds financial exceptions

into:

An intelligent financial control agent that continuously monitors, investigates, and helps resolve financial operations.

🏆 Razorpay AI Buildathon

JUICE was developed as a solution for the Razorpay AI Buildathon — AI Finance Controller challenge.

The project focuses on closing a finance-operations loop around reconciliation:

DATA
 ↓
RECONCILIATION
 ↓
EXCEPTION DETECTION
 ↓
RISK QUANTIFICATION
 ↓
INVESTIGATION
 ↓
REPORTING

Rather than using AI simply as a chatbot, JUICE integrates intelligence directly into a practical finance workflow.

The objective is to combine:

Automation
Deterministic reconciliation
Exception intelligence
Financial risk visibility
Human oversight

into one finance-control experience.

💡 Vision

Financial operations shouldn't require people to spend their time hunting through rows and spreadsheets to discover what went wrong.

Finance teams should be able to see:

What happened.

What doesn't match.

How much is at risk.

What needs attention.

JUICE is built around that idea.

⚡ Find the mismatch. Quantify the risk. Control the money.
👨‍💻 Project Information

Project: JUICE AI
Category: AI Finance Controller
Built for: Razorpay AI Buildathon

GitHub Repository:

https://github.com/bytebynuha/JUICE-AI.git


This project was created as a buildathon project and is intended for demonstration and evaluation purposes.