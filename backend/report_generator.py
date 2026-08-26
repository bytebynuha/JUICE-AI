from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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


def generate_finance_report(
    report_data: dict,
    output_path: Path,
):
    """
    Generate a JUICE finance and risk report
    from the current reconciliation result.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ========================================================
    # DATA
    # ========================================================

    total_transactions = report_data.get(
        "total_transactions",
        0,
    )

    matched = report_data.get(
        "matched",
        0,
    )

    exceptions = report_data.get(
        "exceptions",
        0,
    )

    match_rate = report_data.get(
        "match_rate",
        0,
    )

    financial_exposure = report_data.get(
        "financial_exposure",
        0,
    )

    exception_details = report_data.get(
        "exception_details",
        [],
    )

    preprocessing = report_data.get(
        "preprocessing",
        {},
    )

    # ========================================================
    # DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "JUICETitle",
        parent=styles["Title"],
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=6 * mm,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=10 * mm,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=15,
        leading=19,
        spaceBefore=6 * mm,
        spaceAfter=4 * mm,
        textColor=colors.HexColor("#123B66"),
    )

    normal_style = ParagraphStyle(
        "NormalJUICE",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        spaceAfter=2 * mm,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
    )

    # ========================================================
    # CONTENT
    # ========================================================

    story = []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "JUICE",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Joint Unified Intelligence of Commerce and Expenses",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            "Finance Reconciliation & Risk Report",
            section_style,
        )
    )

    generated_at = datetime.now().strftime(
        "%d %B %Y, %I:%M %p"
    )

    story.append(
        Paragraph(
            f"<b>Generated:</b> {generated_at}",
            normal_style,
        )
    )

    story.append(Spacer(1, 4 * mm))

    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "Executive Summary",
            section_style,
        )
    )

    summary_data = [
        [
            "Metric",
            "Result",
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
            f"{match_rate}%",
        ],
        [
            "Financial Exposure",
            f"₹{financial_exposure:,.2f}",
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[
            85 * mm,
            80 * mm,
        ],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#123B66"),
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
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.whitesmoke,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
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

    story.append(summary_table)

    # ========================================================
    # RISK OVERVIEW
    # ========================================================

    story.append(
        Paragraph(
            "Risk Overview",
            section_style,
        )
    )

    severity_counts = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for exception in exception_details:

        severity = str(
            exception.get(
                "severity",
                "LOW",
            )
        ).upper()

        if severity in severity_counts:
            severity_counts[severity] += 1

    risk_data = [
        [
            "Severity",
            "Number of Exceptions",
        ],
        [
            "HIGH",
            str(severity_counts["HIGH"]),
        ],
        [
            "MEDIUM",
            str(severity_counts["MEDIUM"]),
        ],
        [
            "LOW",
            str(severity_counts["LOW"]),
        ],
    ]

    risk_table = Table(
        risk_data,
        colWidths=[
            85 * mm,
            80 * mm,
        ],
    )

    risk_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#123B66"),
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
                    colors.lightgrey,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "CENTER",
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

    story.append(risk_table)

    # ========================================================
    # EXCEPTIONS
    # ========================================================

    story.append(
        Paragraph(
            "Exceptions & Financial Risks",
            section_style,
        )
    )

    if not exception_details:

        story.append(
            Paragraph(
                "No financial exceptions were detected.",
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
                "N/A",
            )

            exception_type = exception.get(
                "type",
                "UNKNOWN",
            )

            severity = exception.get(
                "severity",
                "UNKNOWN",
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
                "Review the transaction.",
            )

            exception_data = [
                [
                    "Exception",
                    f"#{index}",
                ],
                [
                    "Transaction ID",
                    str(transaction_id),
                ],
                [
                    "Type",
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
            ]

            exception_table = Table(
                exception_data,
                colWidths=[
                    45 * mm,
                    120 * mm,
                ],
            )

            exception_table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (0, -1),
                            colors.HexColor("#F2F5F8"),
                        ),
                        (
                            "FONTNAME",
                            (0, 0),
                            (0, -1),
                            "Helvetica-Bold",
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.4,
                            colors.lightgrey,
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
                            5,
                        ),
                        (
                            "BOTTOMPADDING",
                            (0, 0),
                            (-1, -1),
                            5,
                        ),
                    ]
                )
            )

            story.append(
                exception_table
            )

            story.append(
                Spacer(
                    1,
                    2 * mm,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Reason:</b> {reason}",
                    normal_style,
                )
            )

            story.append(
                Paragraph(
                    f"<b>Recommendation:</b> {recommendation}",
                    normal_style,
                )
            )

            story.append(
                Spacer(
                    1,
                    5 * mm,
                )
            )

    # ========================================================
    # PREPROCESSING
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        Paragraph(
            "Data Preprocessing Summary",
            section_style,
        )
    )

    if preprocessing:

        preprocessing_data = [
            [
                "File",
                "Original Rows",
                "Cleaned Rows",
                "Duplicates Removed",
                "Missing Values Removed",
            ]
        ]

        for name in [
            "razorpay",
            "bank",
            "ledger",
        ]:

            stats = preprocessing.get(
                name,
                {},
            )

            preprocessing_data.append(
                [
                    name.title(),
                    str(
                        stats.get(
                            "original_rows",
                            0,
                        )
                    ),
                    str(
                        stats.get(
                            "cleaned_rows",
                            0,
                        )
                    ),
                    str(
                        stats.get(
                            "duplicates_removed",
                            0,
                        )
                    ),
                    str(
                        stats.get(
                            "missing_values_before",
                            0,
                        )
                    ),
                ]
            )

        preprocessing_table = Table(
            preprocessing_data,
            colWidths=[
                30 * mm,
                30 * mm,
                30 * mm,
                35 * mm,
                40 * mm,
            ],
            repeatRows=1,
        )

        preprocessing_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#123B66"),
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
                        0.4,
                        colors.lightgrey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7,
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
                        5,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5,
                    ),
                ]
            )
        )

        story.append(
            preprocessing_table
        )

    else:

        story.append(
            Paragraph(
                "No preprocessing information was supplied.",
                normal_style,
            )
        )

    # ========================================================
    # FINAL RECOMMENDATION
    # ========================================================

    story.append(
        Paragraph(
            "Overall Assessment",
            section_style,
        )
    )

    if exceptions == 0:

        assessment = (
            "No reconciliation exceptions were "
            "identified. The uploaded financial "
            "records appear to be consistently "
            "matched."
        )

    elif severity_counts["HIGH"] > 0:

        assessment = (
            "High-severity financial exceptions "
            "were identified. These transactions "
            "should be reviewed as a priority "
            "before final accounting or settlement."
        )

    elif severity_counts["MEDIUM"] > 0:

        assessment = (
            "Medium-severity discrepancies were "
            "identified. Review the affected "
            "transactions and settlement details."
        )

    else:

        assessment = (
            "Low-severity reconciliation exceptions "
            "were identified. These should be reviewed "
            "as part of routine financial controls."
        )

    story.append(
        Paragraph(
            assessment,
            normal_style,
        )
    )

    story.append(
        Spacer(
            1,
            8 * mm,
        )
    )

    story.append(
        Paragraph(
            "Generated by JUICE — Joint Unified "
            "Intelligence of Commerce and Expenses.",
            small_style,
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )

    return output_path