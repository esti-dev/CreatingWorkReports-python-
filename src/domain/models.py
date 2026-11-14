from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import time
from enum import Enum

@dataclass(frozen=True)
class AttendanceRow:
    """Represents a single attendance record row (immutable)."""
    date: str
    day_of_week: str
    entry_time: Optional[time]
    exit_time: Optional[time]
    break_time: str = ""
    total_hours: float = 0.0
    location: Optional[str] = None
    extra_columns: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ReportSummary:
    """Represents summary statistics for the attendance report."""
    total_days: int = 0
    total_hours: float = 0.0
    hourly_rate: Optional[float] = None
    total_payment: Optional[float] = None
    extra_summaries: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AttendanceReport:
    """Encapsulates the complete report including type, rows, and summary."""
    report_type: str
    rows: List[AttendanceRow]
    summary: ReportSummary
    metadata: Dict[str, Any] = field(default_factory=dict)


class ReportType(str, Enum):
        TYPE_A = "TYPE_A"
        TYPE_B = "TYPE_B"