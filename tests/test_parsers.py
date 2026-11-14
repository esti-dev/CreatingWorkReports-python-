import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import unittest
from src.parsing.classifier import ReportClassifier
from src.parsing.parser_factory import ParserRegistry
import src.parsing.type_a_parser
import src.parsing.type_b_parser


class TestReportParsers(unittest.TestCase):

    def test_classifier_type_a(self):
        """בדיקה שסיווג דוח מסוג A מתבצע נכון לפי מילות מפתח בטקסט."""
        sample_text_a = "דוח נוכחות - סוג A"
        report_type = ReportClassifier.classify(sample_text_a)
        self.assertEqual(report_type, "type_a")

    def test_classifier_type_b(self):
        """בדיקה שסיווג דוח מסוג B מתבצע נכון."""
        sample_text_b = "דוח נוכחות - סוג B"
        report_type = ReportClassifier.classify(sample_text_b)
        self.assertEqual(report_type, "type_b")

    def test_parser_factory_registration(self):
        """בדיקה שהמפרשים אכן נרשמו כראוי ב-ParserRegistry ושניתן לשלוף אותם."""
        parser_a = ParserRegistry.get_parser("type_a")
        self.assertIsNotNone(parser_a)

        parser_b = ParserRegistry.get_parser("type_b")
        self.assertIsNotNone(parser_b)


if __name__ == "__main__":
    unittest.main()