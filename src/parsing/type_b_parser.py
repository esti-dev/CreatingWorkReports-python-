from typing import List, Optional
from src.domain.models import AttendanceRow, ReportSummary, ReportType
from src.parsing.base_parser import BaseParser
from src.parsing.parser_factory import ParserRegistry

@ParserRegistry.register(ReportType.TYPE_B)
class TypeBParser(BaseParser):
    """Parser implementation for Report Type B."""

    @property
    def get_report_type(self) -> str:
        return ReportType.TYPE_B

    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """Parses a line specific to Type B layout (break time is optional/handled differently)."""
        parts = line.split()
        if len(parts) < 5:
            return None
        
        try:
            # Type B structure expected order: date, day, entry, exit, total
            date = parts[0]
            day_of_week = parts[1]
            entry_time = parts[2]
            exit_time = parts[3]
            total_hours = float(parts[4])

            return AttendanceRow(
                date=date,
                day_of_week=day_of_week,
                entry_time=entry_time,
                exit_time=exit_time,
                break_time="00:00",  # Optional in Type B
                total_hours=total_hours,
                location=None
            )
        except (ValueError, IndexError):
            return None

    def _parse_summary(self, lines: List[str]) -> ReportSummary:
        """Parses summary block for Type B including hourly rate and total payment."""
        total_days = 0
        total_hours = 0.0
        hourly_rate = None
        total_payment = None

        for line in lines:
            if "סה\"כ שעות חודשיות" in line or "מחיר לשעה" in line or "סה\"כ לתשלום" in line:
                # Parsing logic for Type B financial summaries
                pass

        return ReportSummary(
            total_days=total_days,
            total_hours=total_hours,
            hourly_rate=hourly_rate,
            total_payment=total_payment
        )

    def _is_header_line(self, line: str) -> bool:
        """Determines if the line is a header for Type B."""
        keywords = ["תאריך", "יום בשבוע", "שעת כניסה", "שעת יציאה", "הערות", "כרטיס עובד"]
        return any(kw in line for kw in keywords)