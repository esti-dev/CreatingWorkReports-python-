import os
from pdf2image import convert_from_path
import pytesseract

class OCRExtractor:
    """Handles raw text extraction from PDF files or images using Tesseract OCR."""

    @staticmethod
    def extract_text(file_path: str) -> str:
        """Extracts and returns raw Hebrew text from a given PDF document."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Convert PDF pages to images for Tesseract processing
        images = convert_from_path(file_path)
        extracted_text_collection = []

        for image in images:
            # Using Hebrew ('heb') and English language packs
            text = pytesseract.image_to_string(image, lang='heb+eng')
            extracted_text_collection.append(text)

        return "\n".join(extracted_text_collection)