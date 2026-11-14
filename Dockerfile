FROM python:3.10-slim

# התקנת ספריות המערכת הנדרשות ל-OCR ו-PDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-heb \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# העתקת קבצי ההגדרה ותיקיית הקוד במפורש
COPY pyproject.toml ./
COPY src/ ./src/
COPY main.py ./

# התקנת החבילות תוך מעקף בעיות SSL ובידוד בנייה
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org --no-build-isolation .

# הגדרת נתיב הפייתון
ENV PYTHONPATH=/app

CMD ["python", "main.py"]