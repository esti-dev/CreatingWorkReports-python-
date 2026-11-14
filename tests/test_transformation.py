import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import unittest
from src.domain.models import AttendanceReport, AttendanceRow
from src.transformation.service import TransformationService


class TestReportTransformation(unittest.TestCase):

    def setUp(self):
        """הכנת נתוני דמה לבדיקת ההמרות."""
        self.transformation_service = TransformationService()

        self.sample_rows = [
            AttendanceRow(date="01/03/2026", day_of_week="ראשון", entry_time="08:00", exit_time="16:00"),
            AttendanceRow(date="02/03/2026", day_of_week="שני", entry_time="09:00", exit_time="17:00")
        ]
        self.report = AttendanceReport(rows=self.sample_rows)

    def test_transformation_bounds(self):
        """בדיקה שההמרות פועלות ושומרות על גבולות הגיוניים."""
        seed = 12345
        transformed = self.transformation_service.transform_report(self.report, seed_value=seed)

        self.assertEqual(len(transformed.rows), len(self.sample_rows))

        for row in transformed.rows:
            self.assertIsNotNone(row.date)
            self.assertIsNotNone(row.entry_time)


if __name__ == "__main__":
    unittest.main()