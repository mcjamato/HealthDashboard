from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class PDFReportGenerator:
    def create(self, name, sections, correlations) -> bytes:
        output = BytesIO()
        styles = getSampleStyleSheet()
        story = [Paragraph("Health & Wellness Report", styles["Title"]), Paragraph(name, styles["Heading2"]), Spacer(1, 12)]
        for title, frame in sections:
            story.append(Paragraph(title, styles["Heading2"]))
            if frame.empty:
                story.append(Paragraph("No records available.", styles["BodyText"]))
            else:
                preview = frame.head(10).drop(columns=["is_active", "created_at"], errors="ignore")
                table = Table([list(preview.columns)] + preview.astype(str).values.tolist(), repeatRows=1)
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D8EFFF")),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 6),
                ]))
                story.append(table)
            story.append(Spacer(1, 8))
        story.append(Paragraph("Correlation Summary", styles["Heading2"]))
        story.append(Paragraph("Available in the application analytics page." if not correlations.empty else "Not enough data for correlations.", styles["BodyText"]))
        story.append(Paragraph("Informational only; not medical advice.", styles["Italic"]))
        SimpleDocTemplate(output, pagesize=letter).build(story)
        return output.getvalue()
