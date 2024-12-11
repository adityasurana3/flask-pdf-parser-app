import pytest
from app.pdf_parser import parse_pdf

def test_parse_pdf(tmp_path):
    pdf_path = "tests/sample.pdf"
    output_csv = tmp_path / "output.csv"

    parse_pdf(pdf_path, output_csv)

    assert output_csv.exists()
