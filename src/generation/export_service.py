from typing import Dict, Type
from src.domain.models import AttendanceReport
from src.generation.base_renderer import BaseGenerator
from src.generation.csv_renderer import CSVGenerator
from src.generation.pdf_renderer import PDFGenerator

class ExportService:
    """Manages and executes report export strategies (CSV, PDF, etc.)."""

    def __init__(self):
        self._generators: Dict[str, Type[BaseGenerator]] = {
            "csv": CSVGenerator,
            "pdf": PDFGenerator,
        }

    def register_generator(self, format_name: str, generator_cls: Type[BaseGenerator]) -> None:
        """Registers a new export format generator dynamically."""
        self._generators[format_name.lower()] = generator_cls

    def export(self, report: AttendanceReport, output_path: str, format_type: str = "csv") -> None:
        """Exports the attendance report using the specified format generator."""
        generator_cls = self._generators.get(format_type.lower())
        if not generator_cls:
            raise ValueError(f"Unsupported export format: {format_type}")

        generator = generator_cls()
        generator.generate(report, output_path)