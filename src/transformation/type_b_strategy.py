import random
from datetime import datetime, timedelta
from src.domain.models import AttendanceRow, ReportSummary
from src.transformation.base_strategy import BaseTransformationStrategy
from src.config import (
    SHIFT_MIN_MINUTES,
    SHIFT_MAX_MINUTES,
    MIN_WORK_HOUR,
    MAX_WORK_HOUR,
    MAX_MONTHLY_DAYS
)


class TypeBTransformationStrategy(BaseTransformationStrategy):
    """Transformation strategy for Type B detailed reports featuring break deductions and percentage-based hour splitting."""

    def transform_row(self, row: AttendanceRow, seed_value: int) -> AttendanceRow:
        """Shifts entry and exit times, calculates net working hours including break deductions, and splits hours into percentage categories."""
        # בדיקת תקינות: האם יש נתונים או האם מדובר בשבת/חג (נשאר ללא שינוי)
        if (not row.entry_time or not row.exit_time or
            row.entry_time.strip() == "" or row.exit_time.strip() == "" or
            "שבת" in str(row.day_of_week) or "חג" in str(row.day_of_week)):
            return row

        rng = random.Random(seed_value)

        try:
            fmt = "%H:%M"
            entry_dt = datetime.strptime(row.entry_time.strip(), fmt)
            exit_dt = datetime.strptime(row.exit_time.strip(), fmt)

            # החלת היסט אקראי מתוך ערכי ה־Config
            shift_minutes = rng.randint(SHIFT_MIN_MINUTES, SHIFT_MAX_MINUTES)
            new_entry = entry_dt + timedelta(minutes=shift_minutes)
            new_exit = exit_dt + timedelta(minutes=shift_minutes)

            # אכיפת גבול תחתון לכניסה
            earliest_allowed = entry_dt.replace(hour=MIN_WORK_HOUR, minute=0)
            if new_entry < earliest_allowed:
                new_entry = earliest_allowed

            # אכיפת גבול עליון ליציאה
            latest_allowed = exit_dt.replace(hour=MAX_WORK_HOUR, minute=59)
            if new_exit > latest_allowed:
                new_exit = latest_allowed

            # וידוא משך זמן תקין
            if new_exit <= new_entry:
                new_exit = new_entry + timedelta(hours=4)

            # המרת זמן ההפסקה לשעות
            break_hours = 0.0
            if row.break_time:
                try:
                    break_hours = float(row.break_time)
                except ValueError:
                    break_hours = 0.0

            # חישוב סה"כ שעות נטו: יציאה פחות כניסה פחות הפסקה
            gross_hours = (new_exit - new_entry).total_seconds() / 3600.0
            total_hours = round(max(0.0, gross_hours - break_hours), 2)

            # חלוקת שעות לפי מדרגות אחוזים
            hours_100 = min(total_hours, 8.0)
            remaining_hours = max(0.0, total_hours - 8.0)
            hours_125 = min(remaining_hours, 2.0)
            hours_150 = max(0.0, remaining_hours - 2.0)

            extra_cols = {
                "p_100": round(hours_100, 2),
                "p_125": round(hours_125, 2),
                "p_150": round(hours_150, 2),
                "shabbat": 0.0
            }

            return AttendanceRow(
                date=row.date,
                day_of_week=row.day_of_week,
                entry_time=new_entry.strftime(fmt),
                exit_time=new_exit.strftime(fmt),
                break_time=row.break_time,
                total_hours=total_hours,
                location=row.location,
                extra_columns=extra_cols
            )
        except (ValueError, TypeError):
            return row

    def recalculate_summary(self, rows: list[AttendanceRow], original_summary: ReportSummary) -> ReportSummary:
        """Recalculates monthly totals, active working days (capped at max limit), and aggregated percentage distribution columns."""
        active_rows = [r for r in rows if r.total_hours > 0]
        total_days = min(len(active_rows), MAX_MONTHLY_DAYS)
        total_hours = round(sum(r.total_hours for r in active_rows), 2)

        # סיכום השעות לפי קטגוריות אחוזים
        sum_100 = round(sum(float(r.extra_columns.get("p_100", 0)) for r in active_rows), 2)
        sum_125 = round(sum(float(r.extra_columns.get("p_125", 0)) for r in active_rows), 2)
        sum_150 = round(sum(float(r.extra_columns.get("p_150", 0)) for r in active_rows), 2)

        extra_summaries = {
            "total_100": sum_100,
            "total_125": sum_125,
            "total_150": sum_150,
            "shabbat": original_summary.extra_summaries.get("shabbat", 0.0),
            "bonus": original_summary.extra_summaries.get("bonus", 0.0),
            "travel": original_summary.extra_summaries.get("travel", 0.0)
        }

        return ReportSummary(
            total_days=total_days,
            total_hours=total_hours,
            hourly_rate=original_summary.hourly_rate,
            total_payment=original_summary.total_payment,
            extra_summaries=extra_summaries
        )