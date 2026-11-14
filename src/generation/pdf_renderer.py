import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

from src.domain.models import AttendanceReport
from src.generation.base_renderer import BaseGenerator


class PDFGenerator(BaseGenerator):
    """Generates formatted PDF export documents from AttendanceReport instances with Hebrew RTL support using ReportLab."""

    def __init__(self):
        # רישום גופן תומך עברית (יש לוודא שקובץ ה-TrueType זמין בנתיב או במערכת)
        try:
            pdfmetrics.registerFont(TTFont('HebrewFont', 'arial.ttf'))
        except Exception:
            # גיבוי למקרה שהקובץ אינו נמצא בנתיב הישיר
            pass

    def _format_text(self, text: str) -> str:
        """Reshapes and applies Bidi algorithm for correct Hebrew RTL display."""
        if not text:
            return ""
        try:
            str_text = str(text)
            # בדיקה האם המחרוזת מכילה תווים עבריים
            if any('\u0590' <= c <= \u05FF for c in str_text):
                reshaped = arabic_reshaper.reshape(str_text)
                return get_display(reshaped)
            return str_text
        except Exception:
            return str(text)

    def generate(self, report: AttendanceReport, output_path: str) -> None:
        """Creates a PDF document with Hebrew support, validated hours, and summary statistics."""
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # שימוש בגופן העברי הרשום (או נפילה ל-Helvetica אם לא זמין)
        font_name = 'HebrewFont' if 'HebrewFont' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'

        # Header Section
        c.setFont(f"{font_name}-Bold" if font_name == 'HebrewFont' else "Helvetica-Bold", 14)
        header_title = self._format_text(f"דוח נוכחות - סוג: {report.report_type}")
        c.drawString(50, height - 50, header_title)

        c.setFont(font_name, 10)
        y_position = height - 80

        # Column Titles (בעברית מותאמת מימין לשמאל)
        c.drawString(50, y_position, self._format_text("תאריך"))
        c.drawString(120, y_position, self._format_text("יום"))
        c.drawString(180, y_position, self._format_text("כניסה"))
        c.drawString(240, y_position, self._format_text("יציאה"))
        c.drawString(300, y_position, self._format_text("הפסקה"))
        c.drawString(360, y_position, self._format_text("סה\"כ שעות"))
        c.drawString(430, y_position, self._format_text("מקום"))

        y_position -= 20
        c.line(50, y_position + 15, width - 50, y_position + 15)

        # Rows
        for row in report.rows:
            if y_position < 50:
                c.showPage()
                y_position = height - 50

            c.drawString(50, y_position, self._format_text(str(row.date)))
            c.drawString(120, y_position, self._format_text(str(row.day_of_week)))
            c.drawString(180, y_position, self._format_text(str(row.entry_time)))
            c.drawString(240, y_position, self._format_text(str(row.exit_time)))
            c.drawString(300, y_position, self._format_text(str(row.break_time)))
            c.drawString(360, y_position, self._format_text(str(row.total_hours)))
            c.drawString(430, y_position, self._format_text(str(row.location or "-")))

            y_position -= 18

        # Summary Section
        y_position -= 20
        c.line(50, y_position + 15, width - 50, y_position + 15)
        c.setFont(f"{font_name}-Bold" if font_name == 'HebrewFont' else "Helvetica-Bold", 11)

        summary_days = self._format_text(f"סה\"כ ימי עבודה: {report.summary.total_days}")
        summary_hours = self._format_text(f"סה\"כ שעות: {report.summary.total_hours}")

        c.drawString(50, y_position, summary_days)
        c.drawString(220, y_position, summary_hours)

        if report.summary.total_payment is not None:
            y_position -= 20
            summary_payment = self._format_text(f"סה\"כ לתשלום: {report.summary.total_payment}")
            c.drawString(50, y_position, summary_payment)

        c.save()