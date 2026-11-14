import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import unittest
from src.parsing.classifier import ReportClassifier
from src.parsing.parser_factory import ParserRegistry
from src.transformation.service import TransformationService

import src.parsing.type_a_parser
import src.parsing.type_b_parser


class TestSystemIntegration(unittest.TestCase):

    def test_pipeline_integration_flow(self):
        """בדיקת תהליך האינטגרציה המלא של רכיבי המערכת."""
        mock_raw_text = "דוח נוכחות - סוג A\n01/03/2026 08:00 16:00"

        report_type = ReportClassifier.classify(mock_raw_text)
        self.assertIn(report_type, ["type_a", "type_b"])

        parser = ParserRegistry.get_parser(report_type)
        report = parser.parse(mock_raw_text)
        self.assertIsNotNone(report)

        transformation_service = TransformationService()
        transformed_report = transformation_service.transform_report(report, seed_value=42)
        self.assertIsNotNone(transformed_report)


if __name__ == "__main__":
    unittest.main()