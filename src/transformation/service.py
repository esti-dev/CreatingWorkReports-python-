from typing import Dict, Type
from src.domain.models import AttendanceReport, ReportType
from src.transformation.base_strategy import BaseTransformationStrategy
from src.transformation.type_a_strategy import TypeATransformationStrategy
from src.transformation.type_b_strategy import TypeBTransformationStrategy

class TransformationService:
    """Service that manages and executes the appropriate transformation strategy."""

    def __init__(self):
        self._strategies: Dict[str, Type[BaseTransformationStrategy]] = {
            ReportType.TYPE_A: TypeATransformationStrategy,
            ReportType.TYPE_B: TypeBTransformationStrategy,
        }

    def register_strategy(self, report_type: str, strategy_cls: Type[BaseTransformationStrategy]) -> None:
        """Registers a new strategy for future report types dynamically."""
        self._strategies[report_type] = strategy_cls

    def transform_report(self, report: AttendanceReport, seed_value: int = 42) -> AttendanceReport:
        """Applies the strategy corresponding to the report type, returning a new immutable report."""
        strategy_cls = self._strategies.get(report.report_type)
        if not strategy_cls:
            raise ValueError(f"No transformation strategy found for report type: {report.report_type}")

        strategy = strategy_cls()
        
        # Transform each row independently
        new_rows = [strategy.transform_row(row, seed_value + idx) for idx, row in enumerate(report.rows)]
        
        # Recalculate summary statistics
        new_summary = strategy.recalculate_summary(new_rows, report.summary)

        # Return a brand new AttendanceReport instance, leaving the original intact
        return AttendanceReport(
            report_type=report.report_type,
            rows=new_rows,
            summary=new_summary,
            metadata=report.metadata
        )