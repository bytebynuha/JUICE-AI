import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Investigator
  const [selectedException, setSelectedException] = useState(null);

  // Exception filter
  const [severityFilter, setSeverityFilter] = useState("ALL");

  // AI Summary
  const [aiSummaryOpen, setAiSummaryOpen] = useState(false);

  // Orb finance tips
  const [orbTipIndex, setOrbTipIndex] = useState(0);
  const [orbHovered, setOrbHovered] = useState(false);

  const financeTips = [
    {
      title: "Watch the cash gap",
      text: "A high transaction volume does not always mean healthy cash flow. Compare settlements with actual bank inflows.",
    },
    {
      title: "Investigate large mismatches",
      text: "Large value discrepancies should usually be reviewed before smaller operational exceptions.",
    },
    {
      title: "Track recurring exceptions",
      text: "Repeated exceptions can reveal a process problem rather than isolated transaction errors.",
    },
    {
      title: "Match rate matters",
      text: "A strong reconciliation rate reduces the amount of financial activity that needs manual investigation.",
    },
    {
      title: "Look beyond the amount",
      text: "Reference IDs, dates, settlement timing and transaction patterns can help explain discrepancies.",
    },
    {
      title: "Human review still matters",
      text: "AI can highlight risk and evidence, but important accounting decisions should remain under human control.",
    },
  ];

  useEffect(() => {
    if (!orbHovered) {
      return undefined;
    }

    const interval = setInterval(() => {
      setOrbTipIndex((current) => (current + 1) % financeTips.length);
    }, 3200);

    return () => clearInterval(interval);
  }, [orbHovered, financeTips.length]);

  const handleOrbEnter = () => {
    setOrbTipIndex((current) => (current + 1) % financeTips.length);
    setOrbHovered(true);
  };

  const handleOrbLeave = () => {
    setOrbHovered(false);
  };

  // =====================================================
  // RUN RECONCILIATION
  // =====================================================

  const runReconciliation = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/reconcile",
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Reconciliation failed.");
      }

      const data = await response.json();

      setResult(data);
      setSeverityFilter("ALL");
      setSelectedException(null);
      setAiSummaryOpen(false);
    } catch (err) {
      console.error(err);

      setError(
        "JUICE couldn't connect to the financial engine. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  // =====================================================
  // HELPERS
  // =====================================================

  const formatMoney = (value) => {
    return Number(value || 0).toLocaleString("en-IN", {
      maximumFractionDigits: 2,
    });
  };

  const getSeverityClass = (severity) => {
    return severity?.toLowerCase() || "low";
  };

  // IMPORTANT:
  // These variables fix the previous AI Summary crash.
  const exceptions = result?.exception_details || [];
  const exceptionCount = exceptions.length;

  const highCount = exceptions.filter(
    (exception) => exception.severity === "HIGH"
  ).length;

  const mediumCount = exceptions.filter(
    (exception) => exception.severity === "MEDIUM"
  ).length;

  const lowCount = exceptions.filter(
    (exception) => exception.severity === "LOW"
  ).length;

  // =====================================================
  // FILTER EXCEPTIONS
  // =====================================================

  const filteredExceptions = exceptions.filter((exception) => {
    if (severityFilter === "ALL") {
      return true;
    }

    return exception.severity === severityFilter;
  });

  const getFilterCount = (severity) => {
    if (severity === "ALL") {
      return exceptions.length;
    }

    return exceptions.filter(
      (exception) => exception.severity === severity
    ).length;
  };

  // =====================================================
  // AI RISK ANALYSIS
  // =====================================================

  const getAIRiskLevel = () => {
    if (!result) {
      return {
        level: "WAITING",
        className: "waiting",
      };
    }

    const matchRate = Number(result.match_rate || 0);
    const exposure = Number(result.financial_exposure || 0);

    if (
      highCount > 0 ||
      matchRate < 80 ||
      exposure >= 100000
    ) {
      return {
        level: "HIGH RISK",
        className: "high",
      };
    }

    if (
      matchRate < 95 ||
      exceptionCount > 0 ||
      exposure > 0
    ) {
      return {
        level: "MODERATE",
        className: "medium",
      };
    }

    return {
      level: "LOW RISK",
      className: "low",
    };
  };

  const getAIHeadline = () => {
    if (!result) {
      return "Run a reconciliation to activate JUICE intelligence.";
    }

    const risk = getAIRiskLevel();

    if (risk.className === "high") {
      return "Immediate financial review recommended.";
    }

    if (risk.className === "medium") {
      return "Your financial controls need some attention.";
    }

    return "Your financial controls look healthy.";
  };

  const getAIDescription = () => {
    if (!result) {
      return "JUICE will analyze transaction matching, exception severity, and financial exposure after reconciliation.";
    }

    if (highCount > 0) {
      return `JUICE detected ${highCount} high-severity ${
        highCount === 1 ? "exception" : "exceptions"
      }. These should be reviewed before accounting records are changed.`;
    }

    if (exceptionCount > 0) {
      return `JUICE detected ${exceptionCount} ${
        exceptionCount === 1 ? "exception" : "exceptions"
      } with ₹${formatMoney(
        result.financial_exposure
      )} in associated financial exposure.`;
    }

    return "JUICE found no unresolved financial discrepancies in the current reconciliation.";
  };

  const getAITopPriority = () => {
    if (!result || exceptions.length === 0) {
      return "No immediate action required";
    }

    const high = exceptions.find(
      (exception) => exception.severity === "HIGH"
    );

    if (high) {
      return high.type.replaceAll("_", " ");
    }

    const largest = [...exceptions].sort(
      (a, b) =>
        Number(b.financial_impact || 0) -
        Number(a.financial_impact || 0)
    )[0];

    return largest?.type?.replaceAll("_", " ") || "Review exceptions";
  };

  // =====================================================
  // FINANCIAL CHART DATA
  // =====================================================

  const getSeverityExposure = (severity) => {
    return exceptions
      .filter((exception) => exception.severity === severity)
      .reduce(
        (total, exception) =>
          total + Number(exception.financial_impact || 0),
        0
      );
  };

  const highExposure = getSeverityExposure("HIGH");
  const mediumExposure = getSeverityExposure("MEDIUM");
  const lowExposure = getSeverityExposure("LOW");

  const maxSeverityExposure = Math.max(
    highExposure,
    mediumExposure,
    lowExposure,
    1
  );

  // =====================================================
  // EXCEPTION TYPE DATA
  // =====================================================

  const getExceptionTypeCount = (type) => {
    return exceptions.filter(
      (exception) => exception.type === type
    ).length;
  };

  const missingBankCount =
    getExceptionTypeCount("MISSING_FROM_BANK");

  const missingLedgerCount =
    getExceptionTypeCount("MISSING_FROM_LEDGER");

  const amountMismatchCount =
    getExceptionTypeCount("AMOUNT_MISMATCH");

  const referenceMismatchCount =
    getExceptionTypeCount("REFERENCE_MISMATCH");

  const duplicateCount =
    getExceptionTypeCount("DUPLICATE_TRANSACTION");

  const maxExceptionTypeCount = Math.max(
    missingBankCount,
    missingLedgerCount,
    amountMismatchCount,
    referenceMismatchCount,
    duplicateCount,
    1
  );

  const exceptionExposure = Number(
    result?.financial_exposure || 0
  );

  const matchedTransactionCount = Number(
    result?.matched || 0
  );

  const totalTransactions = Number(
    result?.total_transactions || 0
  );

  const averageTransactionValue =
    totalTransactions > 0
      ? exceptionExposure / totalTransactions
      : 0;

  const currentTip = financeTips[orbTipIndex];

  // =====================================================
  // RENDER
  // =====================================================

  return (
    <div className="juice-app">

      {/* =================================================
          NAVBAR
      ================================================= */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-mark">
            <span>✦</span>
          </div>

          <div className="brand-copy">

            <div className="brand-name">
              JUICE
            </div>

            <div className="brand-description">
              Joint Unified Intelligence for Commerce & Expenses
            </div>

          </div>

        </div>

        <div className="nav-right">

          <div className="system-status">
            <span className="status-dot"></span>
            System online
          </div>

          <div className="profile">
            VC
          </div>

        </div>

      </nav>

      {/* =================================================
          MAIN
      ================================================= */}

      <main className="dashboard">

        {/* =================================================
            HERO
        ================================================= */}

        <section className="hero-section">

          <div className="hero-copy">

            <div className="eyebrow">
              ✦ AI FINANCE CONTROLLER
            </div>

            <h1>
              Your finances,
              <br />
              <span>finally intelligent.</span>
            </h1>

            <p>
              JUICE brings your payment, settlement,
              bank, and ledger data together to
              reconcile transactions and surface
              financial risk.
            </p>

            <button
              className="primary-button"
              onClick={runReconciliation}
              disabled={loading}
            >
              <span>
                {loading
                  ? "JUICE is working..."
                  : "Start Reconciliation →"}
              </span>
            </button>

            {error && (
              <div className="error-box">
                ⚠ {error}
              </div>
            )}

          </div>

          {/* =================================================
              AI ORB
          ================================================= */}

          <div className="hero-visual">

            <div className="orb-decoration orb-decoration-one"></div>
            <div className="orb-decoration orb-decoration-two"></div>

            <div className="orb-glow"></div>

            <div
              className={`ai-orb ${
                orbHovered ? "orb-active" : ""
              }`}
              onMouseEnter={handleOrbEnter}
              onMouseLeave={handleOrbLeave}
            >
              <div className="orb-inner-glow"></div>

              <span>✦</span>

              <div className="orb-label">
                JUICE AI
              </div>
            </div>

            {/* =================================================
                HOVER FINANCE TIP
            ================================================= */}

            <div
              className={`orb-hover-message ${
                orbHovered ? "show" : ""
              }`}
            >
              <div className="orb-tip-tag">
                ✦ FINANCE TIP
              </div>

              <strong>
                {currentTip.title}
              </strong>

              <p>
                {currentTip.text}
              </p>

              <div className="tip-progress">
                <span
                  key={orbTipIndex}
                ></span>
              </div>
            </div>

            {/* =================================================
                FLOATING CARDS
            ================================================= */}

            <div className="floating-card card-one">
              <span>Transactions</span>

              <strong>
                {result
                  ? result.total_transactions
                  : "1,000"}
              </strong>

              <small>
                Records processed
              </small>
            </div>

            <div className="floating-card card-two">

              <span>Match rate</span>

              <strong>
                {result
                  ? `${result.match_rate}%`
                  : "—"}
              </strong>

              <small>
                Reconciliation health
              </small>

            </div>

            <div className="floating-card card-three">

              <span>AI status</span>

              <strong>
                Ready ✦
              </strong>

              <small>
                Intelligence active
              </small>

            </div>

          </div>

        </section>

        {/* =================================================
            PROCESSING
        ================================================= */}

        {loading && (
          <section className="processing-card">

            <div className="processing-orb">
              <span>✦</span>
            </div>

            <div className="processing-content">

              <div className="processing-title">
                JUICE is reconciling your financial data
              </div>

              <div className="processing-text">
                Comparing payment, bank, settlement,
                and ledger records...
              </div>

              <div className="processing-progress">
                <span></span>
              </div>

            </div>

            <div className="processing-spinner"></div>

          </section>
        )}

        {/* =================================================
            RESULTS
        ================================================= */}

        {result && (
          <>

            {/* =================================================
                SECTION HEADER
            ================================================= */}

            <section className="section-header">

              <div>

                <div className="eyebrow">
                  RECONCILIATION COMPLETE ✦
                </div>

                <h2>
                  Financial control snapshot
                </h2>

              </div>

              <div className="success-pill">
                <span></span>
                Reconciled
              </div>

            </section>

            {/* =================================================
                METRICS
            ================================================= */}

            <section className="metrics-grid">

              <div className="metric-card">

                <div className="metric-label">
                  Total transactions
                </div>

                <div className="metric-value">
                  {result.total_transactions}
                </div>

                <div className="metric-description">
                  Records processed
                </div>

              </div>

              <div className="metric-card green">

                <div className="metric-label">
                  Matched
                </div>

                <div className="metric-value">
                  {result.matched}
                </div>

                <div className="metric-description">
                  Successfully reconciled
                </div>

              </div>

              <div className="metric-card orange">

                <div className="metric-label">
                  Exceptions
                </div>

                <div className="metric-value">
                  {result.exceptions}
                </div>

                <div className="metric-description">
                  Require attention
                </div>

              </div>

              <div className="metric-card purple">

                <div className="metric-label">
                  Match rate
                </div>

                <div className="metric-value">
                  {result.match_rate}%
                </div>

                <div className="metric-description">
                  Reconciliation performance
                </div>

              </div>

            </section>

            {/* =================================================
                EXPOSURE
            ================================================= */}

            <section className="exposure-section">

              <div className="exposure-content">

                <div className="eyebrow">
                  FINANCIAL EXPOSURE
                </div>

                <div className="exposure-number-wrap">

                  <span className="currency-symbol">
                    ₹
                  </span>

                  <h2 className="exposure-number">
                    {formatMoney(
                      result.financial_exposure
                    )}
                  </h2>

                </div>

                <p>
                  Total financial value associated
                  with detected exceptions.
                </p>

                <div className="exposure-meta">
                  <span>
                    {exceptionCount}{" "}
                    {exceptionCount === 1
                      ? "exception"
                      : "exceptions"}
                  </span>

                  <span className="meta-divider">
                    /
                  </span>

                  <span>
                    Human review recommended
                  </span>
                </div>

              </div>

              <div className="exposure-visual">

                <div className="exposure-ring ring-one"></div>
                <div className="exposure-ring ring-two"></div>

                <div className="exposure-orb">
                  <span>₹</span>
                </div>

                <div className="jackpot-spark spark-one">
                  ✦
                </div>

                <div className="jackpot-spark spark-two">
                  ✦
                </div>

                <div className="jackpot-spark spark-three">
                  ✦
                </div>

              </div>

            </section>

            {/* =================================================
                FINANCIAL CHARTS
            ================================================= */}

            <section className="charts-section">

              <div className="charts-header">

                <div>

                  <div className="eyebrow">
                    📈 FINANCIAL ANALYTICS
                  </div>

                  <h2>
                    Risk at a glance.
                  </h2>

                  <p>
                    JUICE visualizes where your
                    financial exposure is coming from.
                  </p>

                </div>

                <div className="chart-status">
                  LIVE DATA
                </div>

              </div>

              {/* SUMMARY */}

              <div className="chart-summary-grid">

                <div className="chart-summary-card">

                  <div className="chart-summary-label">
                    Exception exposure
                  </div>

                  <div className="chart-summary-value">
                    ₹{formatMoney(exceptionExposure)}
                  </div>

                  <div className="chart-summary-subtext">
                    Across detected issues
                  </div>

                </div>

                <div className="chart-summary-card">

                  <div className="chart-summary-label">
                    Matched transactions
                  </div>

                  <div className="chart-summary-value">
                    {matchedTransactionCount}
                  </div>

                  <div className="chart-summary-subtext">
                    Successfully reconciled
                  </div>

                </div>

                <div className="chart-summary-card">

                  <div className="chart-summary-label">
                    Avg. exposure / transaction
                  </div>

                  <div className="chart-summary-value">
                    ₹{formatMoney(averageTransactionValue)}
                  </div>

                  <div className="chart-summary-subtext">
                    Based on processed records
                  </div>

                </div>

              </div>

              {/* CHARTS */}

              <div className="financial-chart-grid">

                {/* SEVERITY */}

                <div className="chart-card">

                  <div className="chart-card-header">

                    <div>
                      <div className="chart-card-title">
                        Exposure by severity
                      </div>

                      <div className="chart-card-subtitle">
                        Where financial risk is concentrated
                      </div>
                    </div>

                    <div className="chart-icon">
                      ◉
                    </div>

                  </div>

                  <div className="severity-chart">

                    <div className="chart-row">

                      <div className="chart-row-label">
                        <span className="chart-dot high"></span>
                        High
                      </div>

                      <div className="bar-area">

                        <div className="bar-track">
                          <div
                            className="bar-fill high"
                            style={{
                              width: `${
                                (highExposure /
                                  maxSeverityExposure) *
                                100
                              }%`,
                            }}
                          ></div>
                        </div>

                        <strong>
                          ₹{formatMoney(highExposure)}
                        </strong>

                      </div>

                    </div>

                    <div className="chart-row">

                      <div className="chart-row-label">
                        <span className="chart-dot medium"></span>
                        Medium
                      </div>

                      <div className="bar-area">

                        <div className="bar-track">
                          <div
                            className="bar-fill medium"
                            style={{
                              width: `${
                                (mediumExposure /
                                  maxSeverityExposure) *
                                100
                              }%`,
                            }}
                          ></div>
                        </div>

                        <strong>
                          ₹{formatMoney(mediumExposure)}
                        </strong>

                      </div>

                    </div>

                    <div className="chart-row">

                      <div className="chart-row-label">
                        <span className="chart-dot low"></span>
                        Low
                      </div>

                      <div className="bar-area">

                        <div className="bar-track">
                          <div
                            className="bar-fill low"
                            style={{
                              width: `${
                                (lowExposure /
                                  maxSeverityExposure) *
                                100
                              }%`,
                            }}
                          ></div>
                        </div>

                        <strong>
                          ₹{formatMoney(lowExposure)}
                        </strong>

                      </div>

                    </div>

                  </div>

                </div>

                {/* TYPE DISTRIBUTION */}

                <div className="chart-card">

                  <div className="chart-card-header">

                    <div>

                      <div className="chart-card-title">
                        Exception distribution
                      </div>

                      <div className="chart-card-subtitle">
                        Types of issues detected
                      </div>

                    </div>

                    <div className="chart-icon">
                      ◫
                    </div>

                  </div>

                  <div className="exception-type-chart">

                    {[
                      [
                        "Missing from bank",
                        missingBankCount,
                      ],
                      [
                        "Missing from ledger",
                        missingLedgerCount,
                      ],
                      [
                        "Amount mismatch",
                        amountMismatchCount,
                      ],
                      [
                        "Reference mismatch",
                        referenceMismatchCount,
                      ],
                      [
                        "Duplicate transaction",
                        duplicateCount,
                      ],
                    ].map(([label, count]) => (

                      <div
                        className="type-chart-row"
                        key={label}
                      >

                        <div className="type-chart-info">

                          <span>
                            {label}
                          </span>

                          <strong>
                            {count}
                          </strong>

                        </div>

                        <div className="type-bar-track">

                          <div
                            className="type-bar-fill"
                            style={{
                              width: `${
                                (count /
                                  maxExceptionTypeCount) *
                                100
                              }%`,
                            }}
                          ></div>

                        </div>

                      </div>

                    ))}

                  </div>

                </div>

              </div>

              {/* RISK HEALTH */}

              <div className="risk-health-card">

                <div className="risk-health-left">

                  <div className="risk-ring">

                    <div className="risk-ring-inner">

                      <strong>
                        {result.match_rate}%
                      </strong>

                      <span>
                        match rate
                      </span>

                    </div>

                  </div>

                </div>

                <div className="risk-health-content">

                  <div className="eyebrow">
                    FINANCIAL HEALTH
                  </div>

                  <h3>
                    {result.match_rate >= 95
                      ? "Excellent reconciliation health"
                      : result.match_rate >= 80
                      ? "Moderate reconciliation risk"
                      : "High reconciliation risk"}
                  </h3>

                  <p>
                    {result.match_rate >= 95
                      ? "Most transactions are successfully reconciled. Continue monitoring the remaining exceptions."
                      : result.match_rate >= 80
                      ? "Most transactions are under control, but some exceptions require investigation."
                      : "A significant portion of transactions require attention. Review high-severity exceptions first."}
                  </p>

                </div>

              </div>

            </section>

            {/* =================================================
                AI RISK SUMMARY
            ================================================= */}

            <section className="ai-section ai-risk-section">

              <div className="ai-section-header">

                <div>

                  <div className="eyebrow">
                    ✦ JUICE INTELLIGENCE
                  </div>

                  <h2>
                    Your financial AI has something
                    to say.
                  </h2>

                  <p className="ai-section-description">
                    JUICE analyzes your reconciliation
                    results and identifies the areas
                    that deserve the most attention.
                  </p>

                </div>

                <div className="ai-badge">
                  AI
                </div>

              </div>

              <div className="ai-risk-card">

                <div className="ai-risk-top">

                  <div className="mini-orb">
                    ✦
                  </div>

                  <div className="ai-risk-heading">

                    <span>
                      CURRENT RISK ASSESSMENT
                    </span>

                    <h3>
                      {getAIHeadline()}
                    </h3>

                  </div>

                  <div
                    className={`ai-risk-level ${
                      getAIRiskLevel().className
                    }`}
                  >
                    {getAIRiskLevel().level}
                  </div>

                </div>

                <div className="ai-risk-description">
                  {getAIDescription()}
                </div>

                <div className="ai-summary-grid">

                  <div className="ai-summary-stat">

                    <span>
                      Match rate
                    </span>

                    <strong>
                      {result.match_rate}%
                    </strong>

                    <div className="ai-mini-track">

                      <div
                        className="ai-mini-fill"
                        style={{
                          width: `${Math.min(
                            Math.max(
                              Number(
                                result.match_rate || 0
                              ),
                              0
                            ),
                            100
                          )}%`,
                        }}
                      ></div>

                    </div>

                  </div>

                  <div className="ai-summary-stat">

                    <span>
                      Exceptions
                    </span>

                    <strong>
                      {result.exceptions}
                    </strong>

                    <small>
                      Require review
                    </small>

                  </div>

                  <div className="ai-summary-stat">

                    <span>
                      Exposure
                    </span>

                    <strong>
                      ₹
                      {formatMoney(
                        result.financial_exposure
                      )}
                    </strong>

                    <small>
                      Financial impact
                    </small>

                  </div>

                  <div className="ai-summary-stat">

                    <span>
                      Top priority
                    </span>

                    <strong className="priority-value">
                      {getAITopPriority()}
                    </strong>

                    <small>
                      AI identified
                    </small>

                  </div>

                </div>

                <div className="ai-recommendation">

                  <div className="ai-recommendation-icon">
                    ✦
                  </div>

                  <div>

                    <div className="ai-recommendation-label">
                      AI RECOMMENDATION
                    </div>

                    <p>
                      {result.exceptions === 0
                        ? "No corrective action is currently required. Continue monitoring future reconciliation runs."
                        : getAIRiskLevel().className ===
                          "high"
                        ? "Prioritize high-severity exceptions first. Verify settlement records and supporting evidence before making accounting changes."
                        : "Review the identified exceptions, starting with the transactions carrying the highest financial impact."}
                    </p>

                  </div>

                </div>

                <button
                  className="ai-details-button"
                  onClick={() =>
                    setAiSummaryOpen(!aiSummaryOpen)
                  }
                >
                  {aiSummaryOpen
                    ? "Hide AI analysis ↑"
                    : "View detailed AI analysis →"}
                </button>

                {aiSummaryOpen && (
                  <div className="ai-detailed-analysis">

                    <div className="ai-analysis-item">

                      <span className="analysis-number">
                        01
                      </span>

                      <div>

                        <strong>
                          Transaction integrity
                        </strong>

                        <p>
                          {result.match_rate >= 95
                            ? "Most transactions successfully matched across the financial systems."
                            : "A portion of transactions could not be fully reconciled and should be investigated."}
                        </p>

                      </div>

                    </div>

                    <div className="ai-analysis-item">

                      <span className="analysis-number">
                        02
                      </span>

                      <div>

                        <strong>
                          Exception concentration
                        </strong>

                        <p>
                          {highCount > 0
                            ? `${highCount} high-severity ${
                                highCount === 1
                                  ? "exception requires"
                                  : "exceptions require"
                              } priority review.`
                            : "No high-severity exceptions were detected."}
                        </p>

                      </div>

                    </div>

                    <div className="ai-analysis-item">

                      <span className="analysis-number">
                        03
                      </span>

                      <div>

                        <strong>
                          Financial exposure
                        </strong>

                        <p>
                          ₹
                          {formatMoney(
                            result.financial_exposure
                          )}{" "}
                          is currently associated with
                          detected exceptions.
                        </p>

                      </div>

                    </div>

                    <div className="ai-analysis-item">

                      <span className="analysis-number">
                        04
                      </span>

                      <div>

                        <strong>
                          Recommended workflow
                        </strong>

                        <p>
                          Investigate the highest-risk
                          exceptions, verify supporting
                          evidence, and perform human
                          review before changing
                          accounting records.
                        </p>

                      </div>

                    </div>

                  </div>
                )}

              </div>

              <div className="ai-safety-note">

                <span>
                  🛡
                </span>

                <div>

                  <strong>
                    Intelligence, not autonomous accounting.
                  </strong>

                  <p>
                    JUICE analyzes financial data and
                    suggests actions. Final accounting
                    decisions remain under human control.
                  </p>

                </div>

              </div>

            </section>

            {/* =================================================
                PRIORITY EXCEPTIONS
            ================================================= */}

            <section className="exceptions-section">

              <div className="section-header">

                <div>

                  <div className="eyebrow">
                    PRIORITY EXCEPTIONS
                  </div>

                  <h2>
                    What needs your attention?
                  </h2>

                </div>

                <div className="exception-count">
                  Showing{" "}
                  <strong>
                    {filteredExceptions.length}
                  </strong>{" "}
                  of{" "}
                  <strong>
                    {exceptions.length}
                  </strong>{" "}
                  exceptions
                </div>

              </div>

              {/* FILTERS */}

              <div className="exception-filters">

                <button
                  className={
                    severityFilter === "ALL"
                      ? "filter-button active"
                      : "filter-button"
                  }
                  onClick={() =>
                    setSeverityFilter("ALL")
                  }
                >
                  All
                  <span>
                    {getFilterCount("ALL")}
                  </span>
                </button>

                <button
                  className={
                    severityFilter === "HIGH"
                      ? "filter-button high active"
                      : "filter-button high"
                  }
                  onClick={() =>
                    setSeverityFilter("HIGH")
                  }
                >
                  High
                  <span>
                    {getFilterCount("HIGH")}
                  </span>
                </button>

                <button
                  className={
                    severityFilter === "MEDIUM"
                      ? "filter-button medium active"
                      : "filter-button medium"
                  }
                  onClick={() =>
                    setSeverityFilter("MEDIUM")
                  }
                >
                  Medium
                  <span>
                    {getFilterCount("MEDIUM")}
                  </span>
                </button>

                <button
                  className={
                    severityFilter === "LOW"
                      ? "filter-button low active"
                      : "filter-button low"
                  }
                  onClick={() =>
                    setSeverityFilter("LOW")
                  }
                >
                  Low
                  <span>
                    {getFilterCount("LOW")}
                  </span>
                </button>

              </div>

              {/* EMPTY */}

              {filteredExceptions.length === 0 ? (

                <div className="all-clear">

                  <div className="clear-orb">
                    ✦
                  </div>

                  <h3>
                    All clear! 🍹
                  </h3>

                  <p>
                    JUICE couldn't find any unresolved
                    exceptions matching this filter.
                  </p>

                </div>

              ) : (

                <div className="exception-list">

                  {filteredExceptions
                    .slice(0, 8)
                    .map((exception, index) => (

                      <div
                        className="exception-row"
                        key={`${exception.transaction_id}-${index}`}
                        onClick={() =>
                          setSelectedException(exception)
                        }
                        role="button"
                        tabIndex={0}
                        onKeyDown={(event) => {

                          if (
                            event.key === "Enter" ||
                            event.key === " "
                          ) {
                            event.preventDefault();

                            setSelectedException(
                              exception
                            );
                          }

                        }}
                      >

                        <div className="exception-left">

                          <div
                            className={`severity-dot ${getSeverityClass(
                              exception.severity
                            )}`}
                          ></div>

                          <div className="exception-main">

                            <div className="transaction-id">
                              {exception.transaction_id}
                            </div>

                            <div className="exception-type">
                              {exception.type?.replaceAll(
                                "_",
                                " "
                              )}
                            </div>

                            <div className="exception-reason">
                              {exception.reason}
                            </div>

                          </div>

                        </div>

                        <div className="exception-right">

                          <div
                            className={`severity-label ${getSeverityClass(
                              exception.severity
                            )}`}
                          >
                            {exception.severity}
                          </div>

                          <strong>
                            ₹
                            {formatMoney(
                              exception.financial_impact
                            )}
                          </strong>

                          <span>
                            {exception.confidence}% confidence
                          </span>

                        </div>

                      </div>

                    ))}

                </div>

              )}

              {filteredExceptions.length > 8 && (
                <div className="exception-footer">
                  Showing the first{" "}
                  <strong>8</strong> of{" "}
                  <strong>
                    {filteredExceptions.length}
                  </strong>{" "}
                  matching exceptions.
                </div>
              )}

            </section>

            {/* =================================================
                INVESTIGATOR
            ================================================= */}

            {selectedException && (

              <div
                className="investigator-overlay"
                onClick={(event) => {

                  if (
                    event.target ===
                    event.currentTarget
                  ) {
                    setSelectedException(null);
                  }

                }}
              >

                <div className="investigator-modal">

                  <div className="investigator-header">

                    <div>

                      <div className="eyebrow">
                        ✦ JUICE INVESTIGATOR
                      </div>

                      <h2>
                        Exception investigation
                      </h2>

                    </div>

                    <button
                      className="close-investigator"
                      onClick={() =>
                        setSelectedException(null)
                      }
                      aria-label="Close investigator"
                    >
                      ×
                    </button>

                  </div>

                  <div className="investigator-transaction">

                    <span>
                      Transaction ID
                    </span>

                    <strong>
                      {selectedException.transaction_id}
                    </strong>

                  </div>

                  <div className="investigator-summary">

                    <div className="investigator-stat">

                      <span>
                        Severity
                      </span>

                      <strong
                        className={`investigator-severity ${getSeverityClass(
                          selectedException.severity
                        )}`}
                      >
                        {selectedException.severity}
                      </strong>

                    </div>

                    <div className="investigator-stat">

                      <span>
                        Financial impact
                      </span>

                      <strong>
                        ₹
                        {formatMoney(
                          selectedException.financial_impact
                        )}
                      </strong>

                    </div>

                    <div className="investigator-stat">

                      <span>
                        Confidence
                      </span>

                      <strong>
                        {selectedException.confidence}%
                      </strong>

                    </div>

                  </div>

                  <div className="investigator-block">

                    <div className="investigator-block-title">
                      What happened
                    </div>

                    <p>
                      {selectedException.reason}
                    </p>

                  </div>

                  <div className="investigator-block">

                    <div className="investigator-block-title">
                      Evidence
                    </div>

                    <div className="evidence-grid">

                      {selectedException.evidence ? (

                        Object.entries(
                          selectedException.evidence
                        ).map(([key, value]) => (

                          <div
                            className="evidence-item"
                            key={key}
                          >

                            <span>
                              {key.replaceAll(
                                "_",
                                " "
                              )}
                            </span>

                            <strong>
                              {typeof value ===
                              "boolean"
                                ? value
                                  ? "Yes"
                                  : "No"
                                : String(value)}
                            </strong>

                          </div>

                        ))

                      ) : (

                        <div className="evidence-item">
                          No additional evidence available.
                        </div>

                      )}

                    </div>

                  </div>

                  <div className="investigator-block">

                    <div className="confidence-header">

                      <div className="investigator-block-title">
                        AI confidence
                      </div>

                      <strong>
                        {selectedException.confidence}%
                      </strong>

                    </div>

                    <div className="confidence-track">

                      <div
                        className="confidence-fill"
                        style={{
                          width: `${Math.min(
                            Math.max(
                              Number(
                                selectedException.confidence ||
                                  0
                              ),
                              0
                            ),
                            100
                          )}%`,
                        }}
                      ></div>

                    </div>

                  </div>

                  <div className="recommendation-box">

                    <div className="recommendation-icon">
                      ✦
                    </div>

                    <div>

                      <div className="investigator-block-title">
                        Recommended action
                      </div>

                      <p>
                        {selectedException.recommendation ||
                          "Review this transaction manually before taking action."}
                      </p>

                    </div>

                  </div>

                  <div className="safety-note">

                    <span>
                      🛡
                    </span>

                    <div>

                      <strong>
                        Human review required
                      </strong>

                      <p>
                        JUICE provides financial
                        intelligence and recommendations.
                        It does not automatically modify
                        accounting records or move money.
                      </p>

                    </div>

                  </div>

                </div>

              </div>

            )}

          </>
        )}

      </main>

    </div>
  );
}

export default App;