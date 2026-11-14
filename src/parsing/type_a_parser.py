from typing import List, Optional
from src.domain.models import AttendanceRow, ReportSummary, ReportType
from src.parsing.base_parser import BaseParser
from src.parsing.parser_factory import ParserRegistry
from datetime import datetime


@ParserRegistry.register(ReportType.TYPE_A)
class TypeAParser(BaseParser):
    """Parser implementation for Report Type A."""

    @property
    def get_report_type(self) -> str:
        return ReportType.TYPE_A

    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """Parses a line specific to Type A layout."""
        parts = line.split()
        if len(parts) < 8:
            return None
        
        try:
            # Type A structure expected order: date, day, location, entry, exit, break, total, etc.
            date = parts[0]
            day_of_week = parts[1]
            location = parts[2]
            entry_time = datetime.strptime(parts[3], "%H:%M").time() if parts[3] else None
            exit_time = datetime.strptime(parts[4], "%H:%M").time() if parts[4] else None
            break_time = parts[5]
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
            return None

    def _parse_summary(self, lines: List[str]) -> ReportSummary:
        """Parses summary block for Type A."""
        total_days = 0
        total_hours = 0.0
        
        for line in lines:
            if "סה\"כ שעות" in line or "ימים" in line:
                parts = line.split()
                for part in parts:
                    try:
                        val = float(part)
                        if val > total_hours:
                            total_hours = val
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