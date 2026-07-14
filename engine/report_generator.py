# ---------------------------------------------------------
# report_generator.py (FINAL FULL VERSION)
# ---------------------------------------------------------

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import datetime
import io


# ----------------------------------------------------------------------
# HEADER & FOOTER
# ----------------------------------------------------------------------
def add_header_footer(canvas, doc):
    canvas.saveState()

    # Header
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(50, 770, "AI Debugging System Report")

    # Footer
    canvas.setFont("Helvetica", 9)
    canvas.drawString(50, 20, f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    canvas.drawRightString(550, 20, f"Page {doc.page}")

    canvas.restoreState()


# ----------------------------------------------------------------------
# SEVERITY COLORS
# ----------------------------------------------------------------------
SEVERITY_COLORS = {
    "Low": colors.green,
    "Medium": colors.orange,
    "High": colors.red,
    "Critical": colors.darkred
}


# ----------------------------------------------------------------------
# PDF REPORT GENERATOR
# ----------------------------------------------------------------------
def generate_pdf_report(report_text):
    """
    Creates a styled PDF report using reportlab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    # ---------------- COVER PAGE ----------------
    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Title"],
        alignment=1,
        fontSize=28,
        spaceAfter=30
    )
    story.append(Paragraph("AI Debugger Report", title_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph(
        f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        styles["Normal"]
    ))
    story.append(Spacer(1, 40))

    story.append(PageBreak())

    # ---------------- MAIN CONTENT ----------------
    story.append(Paragraph("<b>Debugging Report</b>", styles["Heading1"]))
    story.append(Spacer(1, 10))

    # Format report into paragraphs
    for line in report_text.split("\n"):
        story.append(Paragraph(line.replace("  ", "&nbsp;&nbsp;"), styles["Normal"]))
        story.append(Spacer(1, 4))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# ----------------------------------------------------------------------
# TEXT REPORT FOR JSON STORAGE
# ----------------------------------------------------------------------
def generate_report(result, suggestion, severity, static_issues, fixed_code):
    """
    Generates a plain text report (used in UI and saved JSON)
    """
    lines = []

    lines.append("=== AI Debugging Report ===")
    lines.append(f"Severity Level: {severity}")
    lines.append("\n------------------------------")
    lines.append("🔍 Analysis Result:")
    lines.append(str(result))

    lines.append("\n------------------------------")
    lines.append("📌 Suggestions:")
    lines.append(str(suggestion))

    lines.append("\n------------------------------")
    lines.append("🧪 Static Analysis Issues:")
    if static_issues:
        for issue in static_issues:
            lines.append(f"- {issue}")
    else:
        lines.append("No static issues detected.")

    lines.append("\n------------------------------")
    lines.append("✨ Auto-Fix Code:")
    if fixed_code:
        lines.append(fixed_code)
    else:
        lines.append("No fix available.")

    return "\n".join(lines)
