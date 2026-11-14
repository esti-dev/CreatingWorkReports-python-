from abc import ABC, abstractmethod
from src.domain.models import AttendanceRow, ReportSummary

class BaseTransformationStrategy(ABC):
    """Abstract base class for report transformation strategies (Strategy Pattern)."""

    @abstractmethod
    def transform_row(self, row: AttendanceRow, seed_value: int) -> AttendanceRow:
        """Transforms a single attendance row deterministically based on business rules."""
        pass

    @abstractmethod
    def recalculate_summary(self, rows: list[AttendanceRow], original_summary: ReportSummary) -> ReportSummary:
        """Recalculates the report summary statistics based on the transformed rows."""
        pass