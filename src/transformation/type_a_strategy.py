from typing import List, Optional
from src.domain.models import AttendanceRow, ReportSummary, ReportType
from src.parsing.base_parser import BaseParser
from src.parsing.parser_factory import ParserRegistry


@ParserRegistry.register(ReportType.TYPE_A)
class TypeAParser(BaseParser):
    """Parser implementation for Report Type A with strict column positioning and holiday handling."""

    @property
    def get_report_type(self) -> str:
        return ReportType.TYPE_A

    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """Parses a line specific to Type A layout strictly by column position."""
        parts = line.split()
        if len(parts) < 7:
            return None

        try:
            date = parts[0]
            day_of_week = parts[1]

            # בדיקה האם מדובר בשבת או חג - נשארים ללא שעות עבודה
            if "שבת" in day_of_week or "חג" in line or (len(parts) > 3 and parts[3] in ["-", "שבת", "חג"]):
                return AttendanceRow(
                    date=date,
                    day_of_week=day_of_week,
                    entry_time="",
                    exit_time="",
                    break_time="",
                    total_hours=0.0,
                    location=parts[2] if len(parts) > 2 else "",
                    extra_columns={}
                )

            location = parts[2]
            entry_time = parts[3]
            exit_time = parts[4]
            break_time = parts[5]

            # קריאת סה"כ שעות לפי מיקום עמודה מדויק ולא חיפוש הערך הגדול/קטן
            total_hours = float(parts[6])

            extra_cols = {
                "p_100": parts[7] if len(parts) > 7 else "0.00",
                "p_125": parts[8] if len(parts) > 8 else "0.00",
                "p_150": parts[9] if len(parts) > 9 else "0.00",
            }

            return AttendanceRow(
                date=date,
                day_of_week=day_of_week,
                entry_time=entry_time,
                exit_time=exit_time,
                break_time=break_time,
                total_hours=total_hours,
                location=location,
                extra_columns=extra_cols
            )
        except (ValueError, IndexError):
            # שורה שלא הצליחה להתפרסר כראוי מוחזרת כ-None או מטופלת מבלי לקרוס בשקט
            return None

    def _parse_summary(self, lines: List[str]) -> ReportSummary:
        """Parses summary block for Type A strictly by column position rather than searching for max values."""
        total_days = 0
        total_hours = 0.0

        for line in lines:
            if "סה\"כ" in line or "סיכום" in line or "ימים" in line:
                parts = line.split()
                # קריאה ממוקדת לפי אינדקס עמודה מוגדר מראש
                for i, part in enumerate(parts):
                    if part.isdigit() and total_days == 0:
                        try:
                            total_days = int(part)
                        except ValueError:
                            pass
                    try:
                        # זיהוי ערך שעות מפורש לפי מיקום או מבנה מספרי עם נקודה עשרונית
                        if "." in part and total_hours == 0.0:
                            total_hours = float(part)
                    except ValueError:
                        continue

        return ReportSummary(
            total_days=total_days,
            total_hours=total_hours
        )

    def _is_header_line(self, line: str) -> bool:
        """Determines if the line is a header for Type A."""
        keywords = ["תאריך", "יום", "מקום", "כניסה", "יציאה", "הפסקה", "סה\"כ", "נ.ע. הנשר"]
        return any(kw in line for kw in keywords)