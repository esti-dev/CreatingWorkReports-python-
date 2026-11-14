from abc import ABC, abstractmethod
from src.domain.models import AttendanceReport

class BaseGenerator(ABC):
    """Abstract base class for report generators (exporting to files)."""

    @abstractmethod
    def generate(self, report: AttendanceReport, output_path: str) -> None:
        """Generates and saves the report to the specified file path."""
        pass