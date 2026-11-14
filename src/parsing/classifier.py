from typing import Callable, Dict

from domain.models import ReportType


class UnknownReportTypeError(Exception):
    """Raised when the report type cannot be classified."""
    pass


class ReportClassifier:
    """Classifies raw text into a specific report type using a registered rules table."""
    
    # Dynamic rules registry mapping report types to predicate functions
    _rules: Dict[str, Callable[[str], bool]] = {
        ReportType.TYPE_A: lambda text: "נ.ע. הנשר כח אדם" in text and "הפסקה" in text,
        ReportType.TYPE_B: lambda text: "נ.ע. הנשר כח אדם" in text and "הפסקה" not in text,
    }

    @classmethod
    def register_rule(cls, report_type: str, condition_func: Callable[[str], bool]) -> None:
        """Registers a new classification rule dynamically (adhering to Open/Closed Principle)."""
        cls._rules[report_type] = condition_func

    @classmethod
    def classify(cls, raw_text: str) -> str:
        """Iterates through registered rules and returns the matching report type."""
        for report_type, condition in cls._rules.items():
            if condition(raw_text):
                return report_type
        
        raise UnknownReportTypeError("The provided report structure is unrecognized or unsupported.")