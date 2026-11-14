# Work Reports Mock Generator

A production-ready, modular Python engine designed to parse attendance report PDFs across multiple variations, apply deterministic and randomized domain-valid transformations, and produce styled mock output reports (PDF and Excel) without modifying original source files.

---

## Key Features

- **Multi-Format Parsing:** Dynamically classifies and parses different report structures (e.g., Type A and Type B) into unified, immutable domain models.
- **Smart Transformation Engine:** Applies randomized yet logically consistent adjustments to attendance hours while strictly enforcing core invariants (e.g., exit time > entry time, exact summary totals recalculation).
- **Extensible Architecture:** Built on SOLID principles and classic Design Patterns, allowing seamless addition of new report types without modifying existing code.
- **Dynamic File Generation:** Generates styled PDF and Excel (.xlsx) output files that dynamically adapt to any report column structure.
- **Full Docker Support:** Run the processing pipeline, interactive CLI sessions, or unit tests in an isolated environment without needing local Python setup.

---

## Architecture & Design Patterns

The project follows a clean **4-layer architecture**:
2. Process a Report File
Bash
docker compose run --rm app python main.py input_pdfs/a_r_9.pdf data/processed/
3. Run Automated Unit Tests
Bash
docker compose run --rm tests
Option B: Running Locally (Python 3.10+)
1. Install Dependencies
Bash
pip install -r requirements.txt
2. Execute the Pipeline
Bash
python main.py input_pdfs/a_r_9.pdf data/processed/
3. Run Tests
Bash
pytest tests/
Project Structure
.
├── domain/
│   ├── exceptions.py
│   └── models.py
├── parsing/
│   ├── base_parser.py
│   ├── parser_factory.py
│   ├── report_classifier.py
│   ├── type_a_parser.py
│   └── type_b_parser.py
├── transformation/
│   ├── base_strategy.py
│   ├── transformation_service.py
│   ├── type_a_strategy.py
│   └── type_b_strategy.py
├── generation/
│   ├── base_renderer.py
│   ├── excel_renderer.py
│   └── pdf_renderer.py
├── tests/
│   ├── test_parsers.py
│   └── test_transformation.py
├── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md