import csv
from src.domain.models import AttendanceReport
from src.generation.base_renderer import BaseGenerator

class CSVGenerator(BaseGenerator):
    """Generates structured CSV export files from AttendanceReport instances."""

    def generate(self, report: AttendanceReport, output_path: str) -> None:
        """Writes report rows and recalculated summary statistics into a CSV file."""
        with open(output_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            
            # Header metadata
            writer.writerow(["Report Type", report.report_type])
            writer.writerow(["Date", "Day", "Entry", "Exit", "Break", "Total Hours", "Location"])
            
            # Attendance rows
            for row in report.rows:
                writer.writerow([
                    row.date,
                    row.day_of_week,
                    row.entry_time,
                    row.exit_time,
                    row.break_time,
                    row.total_hours,
                    row.location or ""
                ])
            
            # Summary section
            writer.writerow([])
            writer.writerow(["Summary Statistics"])
            writer.writerow(["Total Days Worked", report.summary.total_days])
            writer.writerow(["Total Hours", report.summary.total_hours])
            if report.summary.hourly_rate is not None:
                writer.writerow(["Hourly Rate", report.summary.hourly_rate])
            if report.summary.total_payment is not None:
                writer.writerow(["Total Payment", report.summary.total_payment])