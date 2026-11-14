from typing import Dict, Type
from src.parsing.base_parser import BaseParser
from src.parsing.classifier import UnknownReportTypeError

class ParserRegistry:
    """Registry pattern implementation for managing dynamic parser mappings."""
    
    _registry: Dict[str, Type[BaseParser]] = {}

    @classmethod
    def register(cls, report_type: str):
        """Decorator to automatically register a parser class for a specific report type."""
        def decorator(parser_class: Type[BaseParser]):
            cls._registry[report_type] = parser_class
            return parser_class
        return decorator

    @classmethod
    def get_parser(cls, report_type: str) -> BaseParser:
        """Factory method to instantiate and return the corresponding parser."""
        parser_class = cls._registry.get(report_type)
        if not parser_class:
            raise UnknownReportTypeError(f"No parser registered for report type: {report_type}")
        return parser_class()