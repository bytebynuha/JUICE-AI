import { useState } from "react";
import "./App.css";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedException, setSelectedException] = useState(null);

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
    } catch (error) {
      console.error(error);

      setError(
        "JUICE couldn't connect to the financial engine. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatMoney = (value) => {
    return Number(value || 0).toLocaleString("en-IN", {
      maximumFractionDigits: 2,
    });
  };

  const getSeverityClass = (severity) => {
    return severity?.toLowerCase() || "low";
  };

  return (
    <div className="juice-app">

      {/* =====================================================
          BACKGROUND DECORATION
      ===================================================== */}

      <div className="background-decoration">
        <div className="bg-orb bg-orb-one"></div>
        <div className="bg-orb bg-orb-two"></div>
        <div className="bg-orb bg-orb-three"></div>

        <div className="grid-pattern"></div>

        <div className="floating-shape shape-one">✦</div>
        <div className="floating-shape shape-two">◇</div>
        <div className="floating-shape shape-three">✦</div>
      </div>


      {/* =====================================================
          NAVBAR
      ===================================================== */}

      <nav className="navbar">

        <div className="brand">

          {/* JUICE LOGO */}
          <div className="juice-logo">

            <div className="logo-straw"></div>

            <div className="logo-glass">

              <div className="logo-liquid">
                <span className="logo-bubble bubble-one"></span>
                <span className="logo-bubble bubble-two"></span>
                <span className="logo-bubble bubble-three"></span>
              </div>

              <div className="logo-shine"></div>

            </div>

            <div className="logo-spark">✦</div>

          </div>


          <div className="brand-text">

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
            <span>System online</span>
          </div>

          <div className="profile">
            VC
          </div>

        </div>

      </nav>


      {/* =====================================================
          MAIN
      ===================================================== */}

      <main className="dashboard">


        {/* =====================================================
            HERO
        ===================================================== */}

        <section className="hero-section">

          <div className="hero-copy">

            <div className="eyebrow">
              <span className="eyebrow-spark">✦</span>
              AI FINANCE CONTROLLER
            </div>


            <h1>
              Your finances,
              <br />
              <span>finally intelligent.</span>
            </h1>


            <p className="hero-description">
              JUICE brings payment, settlement, bank and
              ledger data together to reconcile transactions,
              detect anomalies and surface financial risk.
            </p>


            <div className="hero-actions">

              <button
                className="primary-button"
                onClick={runReconciliation}
                disabled={loading}
              >

                <span className="button-icon">
                  {loading ? "◌" : "✦"}
                </span>

                <span>
                  {loading
                    ? "JUICE is working..."
                    : "Start Reconciliation"}
                </span>

                {!loading && (
                  <span className="button-arrow">
                    →
                  </span>
                )}

              </button>

            </div>


            {error && (
              <div className="error-box">
                <span className="error-icon">!</span>

                <span>
                  {error}
                </span>
              </div>
            )}


            {/* SMALL TRUST INDICATORS */}

            <div className="hero-trust">

              <div className="trust-item">
                <span className="trust-dot blue"></span>
                Multi-source reconciliation
              </div>

              <div className="trust-item">
                <span className="trust-dot purple"></span>
                AI-powered risk detection
              </div>

            </div>

          </div>


          {/* =====================================================
              AI ORB
          ===================================================== */}

          <div className="hero-visual">

            <div className="orb-grid"></div>

            <div className="orb-ring ring-one"></div>
            <div className="orb-ring ring-two"></div>
            <div className="orb-ring ring-three"></div>


            <div className="orb-glow"></div>


            {/* Hover information */}

            <div className="orb-hover-info">

              <div className="hover-icon">
                ✦
              </div>

              <div className="hover-title">
                JUICE Intelligence
              </div>

              <div className="hover-description">
                Detecting financial patterns,
                anomalies and reconciliation risk.
              </div>

              <div className="hover-status">
                <span></span>
                AI engine ready
              </div>

            </div>


            <div className="ai-orb">

              <div className="orb-inner"></div>

              <div className="orb-core">
                ✦
              </div>

              <div className="orb-particle particle-one"></div>
              <div className="orb-particle particle-two"></div>
              <div className="orb-particle particle-three"></div>

            </div>


            {/* Floating analytics cards */}

            <div className="floating-card card-one">

              <div className="floating-card-icon blue-icon">
                ↗
              </div>

              <div>
                <span>Transactions</span>

                <strong>
                  {result
                    ? result.total_transactions
                    : "1,000"}
                </strong>
              </div>

            </div>


            <div className="floating-card card-two">

              <div className="floating-card-icon purple-icon">
                %
              </div>

              <div>
                <span>Match rate</span>

                <strong>
                  {result
                    ? `${result.match_rate}%`
                    : "—"}
                </strong>
              </div>

            </div>


            <div className="floating-card card-three">

              <div className="floating-card-icon green-icon">
                ✦
              </div>

              <div>
                <span>AI status</span>

                <strong>
                  Ready
                </strong>
              </div>

              <span className="ready-dot"></span>

            </div>

          </div>

        </section>


        {/* =====================================================
            PROCESSING
        ===================================================== */}

        {loading && (

          <section className="processing-card">

            <div className="processing-left">

              <div className="processing-orb">
                <span>✦</span>
              </div>

              <div>

                <div className="processing-title">
                  JUICE is reconciling your financial data
                </div>

                <div className="processing-text">
                  Comparing Razorpay, bank and merchant
                  ledger records...
                </div>

              </div>

            </div>


            <div className="processing-progress">

              <div className="progress-label">
                Processing
              </div>

              <div className="progress-track">
                <div className="progress-fill"></div>
              </div>

            </div>


            <div className="processing-spinner"></div>

          </section>

        )}


        {/* =====================================================
            RESULTS
        ===================================================== */}

        {result && (

          <div className="results-container">


            {/* =================================================
                RESULT HEADER
            ================================================= */}

            <section className="section-header">

              <div>

                <div className="eyebrow">
                  RECONCILIATION COMPLETE ✦
                </div>

                <h2>
                  Financial control snapshot
                </h2>

                <p className="section-subtitle">
                  Here's what JUICE found in your financial data.
                </p>

              </div>


              <div className="success-pill">

                <span className="success-dot"></span>

                Reconciled

              </div>

            </section>


            {/* =================================================
                METRICS
            ================================================= */}

            <section className="metrics-grid">


              <div className="metric-card metric-blue">

                <div className="metric-top">

                  <div className="metric-icon">
                    ↗
                  </div>

                  <span className="metric-tag">
                    DATA
                  </span>

                </div>

                <div className="metric-label">
                  Total transactions
                </div>

                <div className="metric-value">
                  {result.total_transactions}
                </div>

                <div className="metric-description">
                  Records processed
                </div>

                <div className="metric-line">
                  <span></span>
                </div>

              </div>


              <div className="metric-card metric-green">

                <div className="metric-top">

                  <div className="metric-icon">
                    ✓
                  </div>

                  <span className="metric-tag">
                    MATCHED
                  </span>

                </div>

                <div className="metric-label">
                  Matched
                </div>

                <div className="metric-value">
                  {result.matched}
                </div>

                <div className="metric-description">
                  Successfully reconciled
                </div>

                <div className="metric-line">
                  <span></span>
                </div>

              </div>


              <div className="metric-card metric-orange">

                <div className="metric-top">

                  <div className="metric-icon">
                    !
                  </div>

                  <span className="metric-tag">
                    REVIEW
                  </span>

                </div>

                <div className="metric-label">
                  Exceptions
                </div>

                <div className="metric-value">
                  {result.exceptions}
                </div>

                <div className="metric-description">
                  Require attention
                </div>

                <div className="metric-line">
                  <span></span>
                </div>

              </div>


              <div className="metric-card metric-purple">

                <div className="metric-top">

                  <div className="metric-icon">
                    %
                  </div>

                  <span className="metric-tag">
                    PERFORMANCE
                  </span>

                </div>

                <div className="metric-label">
                  Match rate
                </div>

                <div className="metric-value">
                  {result.match_rate}%
                </div>

                <div className="metric-description">
                  Reconciliation performance
                </div>

                <div className="metric-line">
                  <span></span>
                </div>

              </div>

            </section>


            {/* =================================================
                EXPOSURE
            ================================================= */}

            <section className="exposure-section">

              <div className="exposure-background-shape"></div>

              <div className="exposure-content">

                <div className="exposure-label">
                  FINANCIAL EXPOSURE
                </div>

                <h2>
                  ₹{formatMoney(result.financial_exposure)}
                </h2>

                <p>
                  Total financial value associated with
                  detected exceptions.
                </p>

              </div>


              <div className="exposure-visual">

                <div className="exposure-ring ring-a"></div>
                <div className="exposure-ring ring-b"></div>

                <div className="exposure-orb">
                  ✦
                </div>

              </div>

            </section>


            {/* =================================================
                AI INSIGHT
            ================================================= */}

            <section className="ai-section">

              <div className="ai-section-header">

                <div>

                  <div className="eyebrow">
                    ✦ JUICE INTELLIGENCE
                  </div>

                  <h2>
                    Your financial AI has something to say.
                  </h2>

                  <p>
                    An intelligent interpretation of the
                    reconciliation results.
                  </p>

                </div>

                <div className="ai-badge">
                  AI
                </div>

              </div>


              <div className="ai-insight">

                <div className="mini-orb">
                  ✦
                </div>


                <div className="insight-content">

                  <div className="insight-title">

                    {result.exceptions === 0
                      ? "Everything looks healthy."
                      : `${result.exceptions} exception${
                          result.exceptions === 1
                            ? ""
                            : "s"
                        } need your attention.`}

                  </div>


                  <div className="insight-text">

                    JUICE has completed the first
                    reconciliation pass. Open an exception
                    to investigate its evidence, financial
                    impact and recommended action.

                  </div>

                </div>


                <div className="insight-spark">
                  ✦
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

                  <p className="section-subtitle">
                    Review unusual transactions identified by JUICE.
                  </p>

                </div>


                <div className="exception-count">
                  <span>{result.exceptions}</span>
                  detected
                </div>

              </div>


              {result.exception_details?.length === 0 ? (

                <div className="all-clear">

                  <div className="clear-orb">
                    ✓
                  </div>

                  <h3>
                    Your finances are looking fresh. 🍹
                  </h3>

                  <p>
                    JUICE couldn't find any unresolved
                    financial discrepancies.
                  </p>

                </div>

              ) : (

                <div className="exception-list">

                  {result.exception_details
                    .slice(0, 8)
                    .map((exception, index) => (

                      <div
                        className="exception-row"
                        key={`${exception.transaction_id}-${index}`}
                        onClick={() =>
                          setSelectedException(exception)
                        }
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
                              {exception.type
                                ?.replaceAll("_", " ")}
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

                          <span className="exception-arrow">
                            →
                          </span>

                        </div>

                      </div>

                    ))}

                </div>

              )}

            </section>

          </div>

        )}

      </main>


      {/* =====================================================
          INVESTIGATOR MODAL
      ===================================================== */}

      {selectedException && (

        <div
          className="investigator-overlay"
          onClick={(event) => {

            if (
              event.target.classList.contains(
                "investigator-overlay"
              )
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
                <span>Severity</span>

                <strong
                  className={`investigator-severity ${getSeverityClass(
                    selectedException.severity
                  )}`}
                >
                  {selectedException.severity}
                </strong>
              </div>


              <div className="investigator-stat">
                <span>Financial impact</span>

                <strong>
                  ₹
                  {formatMoney(
                    selectedException.financial_impact
                  )}
                </strong>
              </div>


              <div className="investigator-stat">
                <span>Confidence</span>

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
                        {key.replaceAll("_", " ")}
                      </span>

                      <strong>
                        {typeof value === "boolean"
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
                        selectedException.confidence || 0,
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
                  JUICE provides financial intelligence
                  and recommendations. It does not
                  automatically modify accounting records
                  or move money.
                </p>

              </div>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

export default App;