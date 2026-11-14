from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models import AttendanceReport, AttendanceRow, ReportSummary

class BaseParser(ABC):
    """Abstract base parser implementing the Template Method pattern for report parsing."""

    def parse(self, raw_text: str) -> AttendanceReport:
        """Core parsing workflow shared across all report types."""
        cleaned_text = self._clean_text(raw_text)
        lines = cleaned_text.splitlines()
        
        summary = self._parse_summary(lines)
        rows = [
            self._parse_row(line) 
            for line in lines 
            if not self._is_header_line(line) and line.strip()
        ]
        
        # Filter out None values resulting from invalid lines
        valid_rows = [row for row in rows if row is not None]
        
        return AttendanceReport(
            report_type=self.get_report_type,
            rows=valid_rows,
            summary=summary
        )

    def _clean_text(self, raw_text: str) -> str:
        """Common text cleaning logic (fixing OCR artifacts, spacing, etc.)."""
        return raw_text.replace("|", "1")

    @property
    @abstractmethod
    def get_report_type(self) -> str:
        """Returns the specific report type identifier."""
        pass

    @abstractmethod
    def _parse_row(self, line: str) -> Optional[AttendanceRow]:
        """Parses a single text line into an AttendanceRow object."""
        pass

    @abstractmethod
    def _parse_summary(self, lines: List[str]) -> ReportSummary:
        """Parses report summary statistics."""
        pass

    @abstractmethod
    def _is_header_line(self, line: str) -> bool:
        """Determines if a line is part of the table header or metadata."""
        pass