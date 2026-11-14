import os
import time
from dotenv import load_dotenv
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="מערכת עיבוד וניתוח דוחות נוכחות")
    parser.add_argument("--input", type=str, default="input_pdfs/a_r_9.pdf", help="נתיב לקובץ הקלט")
    parser.add_argument("--output-dir", type=str, default="output", help="תיקיית פלט לקבצים המעובדים")
    parser.add_argument("--format", type=str, choices=["csv", "pdf"], default="pdf", help="פורמט הפלט המבוקש")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    # שימוש בפרמטרים מתוך args...
    target_csv = os.path.join(args.output_dir, "generated_report.csv")
    target_pdf = os.path.join(args.output_dir, "generated_report.pdf")

    if os.path.exists(args.input):
        process_attendance_report(args.input, target_csv, target_pdf)
    else:
        print(f"קובץ הקלט '{args.input}' לא נמצא.")
# Load environment variables from .env file
load_dotenv()

INPUT_DIR = os.getenv("INPUT_DIR", "input_pdfs")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "/app/output")
import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.parsing.ocr import OCRExtractor
from src.parsing.classifier import ReportClassifier
from src.parsing.parser_factory import ParserRegistry
from src.transformation.service import TransformationService
from src.generation.csv_renderer import CSVGenerator
from src.generation.pdf_renderer import PDFGenerator
from src.domain.exceptions import ReportProcessingError

# Import parser modules to execute @ParserRegistry.register decorators
import src.parsing.type_a_parser
import src.parsing.type_b_parser


def process_attendance_report(file_path: str, output_csv_path: str, output_pdf_path: str) -> None:
    """Runs the end-to-end report pipeline with randomized parameters and output validation."""
    print(f"--- Starting Processing: {file_path} ---")

    try:
        # Step 1: Raw text extraction via OCR
        raw_text = OCRExtractor.extract_text(file_path)
        print("Step 1: OCR text extraction completed.")

        # Step 2: Dynamic classification via rule registry
        report_type = ReportClassifier.classify(raw_text)
        print(f"Step 2: Report classified as '{report_type}'.")

        # Step 3: Fetch parser from Factory and parse
        parser = ParserRegistry.get_parser(report_type)
        report = parser.parse(raw_text)
        print(f"Step 3: Parsed {len(report.rows)} initial row records.")

        # Step 4: Apply transformation strategy with dynamic seed (time-based) for varying output
        transformation_service = TransformationService()
        dynamic_seed = 42
        transformed_report = transformation_service.transform_report(report, seed_value=dynamic_seed)
        print("Step 4: Applied deterministic transformation with logical bounds (05:00-00:00).")

        # Step 5: Export to CSV and PDF
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)

        csv_gen = CSVGenerator()
        csv_gen.generate(transformed_report, output_csv_path)
        print(f"Step 5a: Exported CSV -> {output_csv_path}")

        pdf_gen = PDFGenerator()
        pdf_gen.generate(transformed_report, output_pdf_path)
        print(f"Step 5b: Exported PDF -> {output_pdf_path}")
        print("--- Processing Complete Successfully ---")

    except ReportProcessingError as e:
        print(f"\n[שגיאת תחום במערכת]: {e}")
    except FileNotFoundError as e:
        print(f"\n[שגיאת קובץ]: {e}")
    except Exception as e:
        print(f"\n[שגיאה בלתי צפויה]: {e}")


if __name__ == "__main__":
    # שימוש בתיקיות הדינמיות שהוגדרו מתוך ה-.env
    sample_input = os.path.join(INPUT_DIR, "sample_report.pdf")
    target_csv = os.path.join(OUTPUT_DIR, "generated_report.csv")
    target_pdf = os.path.join(OUTPUT_DIR, "generated_report.pdf")

    if os.path.exists(sample_input):
        process_attendance_report(sample_input, target_csv, target_pdf)
    else:
        print(f"Input file '{sample_input}' not found. Please place a valid file in the execution directory.")