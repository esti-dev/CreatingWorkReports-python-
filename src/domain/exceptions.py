class ReportProcessingError(Exception):
    """Base exception class for all errors in the report processing domain."""
    pass

class ParsingError(ReportProcessingError):
    """Raised when parsing a report file fails or structured data is invalid."""
    pass

class UnknownReportTypeError(ReportProcessingError):
    """Raised when the system encounters an unsupported or unclassifiable report type."""
    pass

class InvalidReportDataError(ReportProcessingError):
    """Raised when an attendance row or summary violates business invariants."""
    pass