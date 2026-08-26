from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


# ============================================================
# JUICE PDF REPORT GENERATOR
# ============================================================


def generate_finance_report(
    result,
    output_file,
):
    """
    Creates a PDF finance report from the reconciliation result.

    Parameters
    ----------
    result : dict
        Result returned by reconciliation.py

    output_file : Path
        Where the PDF should be saved
    """

    output_file = Path(output_file)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # GET DATA
    # ========================================================

    total_transactions = result.get(
        "total_transactions",
        0,
    )

    matched = result.get(
        "matched",
        0,
    )

    exceptions = result.get(
        "exceptions",
        0,
    )

    match_rate = result.get(
        "match_rate",
        0,
    )

    financial_exposure = result.get(
        "financial_exposure",
        0,
    )

    exception_details = result.get(
        "exception_details",
        [],
    )

    # ========================================================
    # DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(
        str(output_file),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="JUICE Finance Report",
        author="JUICE AI",
    )

    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "JUICETitle",
        parent=styles["Title"],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "JUICESubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor(
            "#667085"
        ),
        spaceAfter=20,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=15,
        leading=19,
        textColor=colors.HexColor(
            "#155EEF"
        ),
        spaceBefore=12,
        spaceAfter=10,
    )

    normal_style = ParagraphStyle(
        "JUICENormal",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor(
            "#344054"
        ),
    )

    small_style = ParagraphStyle(
        "JUICESmall",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor(
            "#667085"
        ),
    )

    # ========================================================
    # CONTENT
    # ========================================================

    story = []

    # ========================================================
    # HEADER
    # ========================================================

    story.append(
        Paragraph(
            "JUICE",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Joint Unified Intelligence for Commerce & Expenses",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            "FINANCE RECONCILIATION REPORT",
            section_style,
        )
    )

    generated_time = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    story.append(
        Paragraph(
            f"Generated: {generated_time}",
            small_style,
        )
    )

    story.append(
        Spacer(
            1,
            8,
        )
    )

    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "Executive Summary",
            section_style,
        )
    )

    summary_text = (
        "JUICE analysed the uploaded financial datasets "
        "and performed transaction reconciliation across "
        "payment, banking and ledger records. "
        "The report highlights matched transactions, "
        "exceptions and potential financial exposure."
    )

    story.append(
        Paragraph(
            summary_text,
            normal_style,
        )
    )

    story.append(
        Spacer(
            1,
            12,
        )
    )

    # ========================================================
    # KEY METRICS
    # ========================================================

    story.append(
        Paragraph(
            "Key Financial Metrics",
            section_style,
        )
    )

    metrics_data = [
        [
            "Metric",
            "Value",
        ],
        [
            "Total Transactions",
            str(total_transactions),
        ],
        [
            "Successfully Matched",
            str(matched),
        ],
        [
            "Exceptions",
            str(exceptions),
        ],
        [
            "Match Rate",
            f"{match_rate:.2f}%",
        ],
        [
            "Financial Exposure",
            f"₹{financial_exposure:,.2f}",
        ],
    ]

    metrics_table = Table(
        metrics_data,
        colWidths=[
            90 * mm,
            70 * mm,
        ],
    )

    metrics_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#155EEF"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor(
                        "#D0D5DD"
                    ),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor(
                        "#F8FAFC"
                    ),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        metrics_table
    )

    story.append(
        Spacer(
            1,
            15,
        )
    )

    # ========================================================
    # RISK OVERVIEW
    # ========================================================

    story.append(
        Paragraph(
            "Risk Overview",
            section_style,
        )
    )

    high_count = sum(
        1
        for exception in exception_details
        if str(
            exception.get(
                "severity",
                ""
            )
        ).upper()
        == "HIGH"
    )

    medium_count = sum(
        1
        for exception in exception_details
        if str(
            exception.get(
                "severity",
                ""
            )
        ).upper()
        == "MEDIUM"
    )

    low_count = sum(
        1
        for exception in exception_details
        if str(
            exception.get(
                "severity",
                ""
            )
        ).upper()
        == "LOW"
    )

    risk_data = [
        [
            "Risk Level",
            "Exceptions",
        ],
        [
            "HIGH",
            str(high_count),
        ],
        [
            "MEDIUM",
            str(medium_count),
        ],
        [
            "LOW",
            str(low_count),
        ],
    ]

    risk_table = Table(
        risk_data,
        colWidths=[
            90 * mm,
            70 * mm,
        ],
    )

    risk_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#F79009"
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor(
                        "#D0D5DD"
                    ),
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        risk_table
    )

    # ========================================================
    # EXCEPTIONS
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "Exception Details",
            section_style,
        )
    )

    if not exception_details:

        story.append(
            Paragraph(
                "No exceptions were detected.",
                normal_style,
            )
        )

    else:

        for index, exception in enumerate(
            exception_details,
            start=1,
        ):

            transaction_id = exception.get(
                "transaction_id",
                "Unknown",
            )

            exception_type = exception.get(
                "type",
                "Unknown",
            )

            severity = exception.get(
                "severity",
                "Unknown",
            )

            impact = exception.get(
                "financial_impact",
                0,
            )

            confidence = exception.get(
                "confidence",
                0,
            )

            reason = exception.get(
                "reason",
                "No reason provided.",
            )

            recommendation = exception.get(
                "recommendation",
                "No recommendation provided.",
            )

            exception_data = [
                [
                    "Transaction",
                    str(transaction_id),
                ],
                [
                    "Exception",
                    str(exception_type),
                ],
                [
                    "Severity",
                    str(severity),
                ],
                [
                    "Financial Impact",
                    f"₹{float(impact):,.2f}",
                ],
                [
                    "Confidence",
                    f"{confidence}%",
                ],
                [
                    "Reason",
                    str(reason),
                ],
                [
                    "Recommendation",
                    str(recommendation),
                ],
            ]

            exception_table = Table(
                exception_data,
                colWidths=[
                    45 * mm,
                    115 * mm,
            ])

            exception_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor(
                                "#F2F4F7"
                            ),
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (0, -1),
                            "Helvetica-Bold",
                        ),
                        (
                            "FONTNAME",
                            (1, 0),
                            (1, -1),
                            "Helvetica",
                        ),
                        (
                            "FONTSIZE",
                            (0, 0),
                            (-1, -1),
                            8,
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.5,
                            colors.HexColor(
                                "#D0D5DD"
                            ),
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP",
                        ),
                        (
                            "TOPPADDING",
                            (0, 0),
                            (-1, -1),
                            6,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            6,
                        ),
                    ]
                )
            )

            story.append(
                Paragraph(
                    f"Exception #{index}",
                    styles["Heading3"],
                )
            )

            story.append(
                exception_table
            )

            story.append(
                Spacer(
                    1,
                    10,
                )
            )

    # ========================================================
    # FINAL NOTE
    # ========================================================

    story.append(
        Spacer(
            1,
            15,
        )
    )

    story.append(
        Paragraph(
            "JUICE AI — Joint Unified Intelligence "
            "for Commerce & Expenses",
            small_style,
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )

    return output_file